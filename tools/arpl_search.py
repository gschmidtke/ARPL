"""Reference implementation of an ARPL lookup tool for Revit AI bridges and MCP servers.

Loads index.json (from GitHub or a local copy) and ranks packs and project workflows
for a task description plus optional facet filters. Plain Python 3, no dependencies.

    python tools/arpl_search.py "place studs in a wall panel" --work-class W3 --revit 2025
    python tools/arpl_search.py "power connector on kitchen equipment" --discipline electrical

Expose search() as a tool (see docs/agent-setup.md) so agents don't fetch raw HTTP each time.
"""
import json, os, re, sys, argparse, urllib.request

INDEX_URL = "https://raw.githubusercontent.com/gschmidtke/ARPL/main/index.json"
STOP = set("a an the of to in on for and or with by from at is be as this that it into".split())

def load_index(source=None):
    source = source or os.environ.get("ARPL_INDEX") or INDEX_URL
    if source.startswith("http"):
        with urllib.request.urlopen(source, timeout=20) as r:
            return json.load(r)
    return json.load(open(source, encoding="utf-8"))

def words(text):
    return {w for w in re.findall(r"[a-z0-9]+", text.lower()) if w not in STOP and len(w) > 2}

def search(task, index=None, work_class=None, discipline=None, project_type=None, phase=None, revit=None, limit=5):
    """Return ranked matches: project workflows first, then packs. Each hit carries its rule and path."""
    index = index or load_index()
    q = words(task)
    def score(fields, weights):
        return sum(w * len(q & words(" ".join(f if isinstance(f, str) else " ".join(map(str, f)) for f in field)))
                   for field, w in zip(fields, weights))
    hits = []
    for p in index["packs"]:
        if work_class and p["work_class"] != work_class: continue
        if discipline and discipline not in p["disciplines"] and "generic" not in p["disciplines"]: continue
        if project_type and project_type not in p["project_types"] and "generic" not in p["project_types"]: continue
        if phase and phase not in p["phases"] and "generic" not in p["phases"]: continue
        s = score([[*p.get("use_when", [])], [p["title"]], [*p.get("api_terms", [])], [*p["workflows"]]], [3, 2, 2, 1])
        s -= 3 * len(q & words(" ".join(p.get("not_for", []))))
        if s > 0:
            hits.append({"kind": "pack", "score": s, "id": p["id"], "revision": p.get("revision"), "title": p["title"],
                         "status": p["status"], "rule": p["rule"], "validation": p.get("validation"), "path": p["path"],
                         "tested_in_your_version": (revit in p["revit_versions_tested"]) if revit else None})
    for w in index.get("project_workflows", []):
        s = 2 * len(q & words(w["title"] + " " + w["intent"] + " " + " ".join(st["do"] for st in w["steps"])))
        if s > 0:
            hits.append({"kind": "project_workflow", "score": s + 2, "id": w["id"], "revision": w.get("revision"),
                         "title": w["title"], "status": w["status"], "steps": w["steps"], "path": w["path"]})
    hits.sort(key=lambda h: (-h["score"], h["kind"] != "project_workflow"))
    return {"query": task, "raw_base": index["raw_base"], "results": hits[:limit],
            "note": "Read final/rule.json and the vNN iterations of each pack before acting. Record {arpl_pack, pack_revision, revit_version, result}."}

if __name__ == "__main__":
    a = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    a.add_argument("task"); a.add_argument("--work-class"); a.add_argument("--discipline"); a.add_argument("--project-type")
    a.add_argument("--phase"); a.add_argument("--revit"); a.add_argument("--index"); a.add_argument("--limit", type=int, default=5)
    o = a.parse_args()
    print(json.dumps(search(o.task, load_index(o.index), o.work_class, o.discipline, o.project_type, o.phase, o.revit, o.limit), indent=2))
