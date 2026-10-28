"""Validate every pack manifest against the schema and the controlled vocabularies.
Usage: python tools/validate.py   (needs: pip install jsonschema)"""
import json, re, glob, sys, os, re
try:
    import jsonschema
except ImportError:
    sys.exit("pip install jsonschema")
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
schema = json.load(open(os.path.join(root, "schema/manifest.schema.json")))
voc = json.load(open(os.path.join(root, "vocabularies/vocabularies.json")))
errors, ids = [], {}
for path in sorted(glob.glob(os.path.join(root, "library/*/*/manifest.json"))):
    m = json.load(open(path)); rel = os.path.relpath(path, root)
    try:
        jsonschema.validate(m, schema)
    except jsonschema.ValidationError as e:
        errors.append(f"{rel}: {e.message}")
    for facet, vocab in [("workflows", voc["workflows"]), ("disciplines", voc["disciplines"]), ("roles", voc["roles"]), ("project_types", voc["project_types"]), ("phases", voc["phases"])]:
        for v in m.get(facet, []):
            if v not in vocab: errors.append(f"{rel}: '{v}' is not in vocabularies.{facet}")
    if m.get("workflows") and rel.split(os.sep)[1] != m["workflows"][0]:
        errors.append(f"{rel}: folder does not match first workflow '{m['workflows'][0]}'")
    if m["id"] in ids: errors.append(f"{rel}: duplicate id {m['id']} (also {ids[m['id']]})")
    ids[m["id"]] = rel
    for v in sorted(glob.glob(os.path.join(os.path.dirname(path), "v*"))):
        for f in ("instruction.json", "result.json"):
            if not os.path.exists(os.path.join(v, f)): errors.append(f"{os.path.relpath(v, root)}: missing {f}")
# Failure patterns: unique ids and an evidence_kind from the vocabulary
fpdoc = json.load(open(os.path.join(root, "patterns/failure-patterns.json"), encoding="utf-8"))
fpids = set()
for fp in fpdoc["patterns"]:
    if fp["id"] in fpids: errors.append(f"patterns/failure-patterns.json: duplicate {fp['id']}")
    fpids.add(fp["id"])
    if fp.get("evidence_kind") not in voc.get("evidence_kinds", {}): errors.append(f"patterns/failure-patterns.json: {fp['id']} evidence_kind '{fp.get('evidence_kind')}' is not in vocabularies.evidence_kinds")
# Hidden characters can carry instructions humans can't see (context poisoning)
HIDDEN = re.compile("[\U000E0000-\U000E007F\u200B-\u200F\u202A-\u202E\u2060-\u2064\uFEFF]")
for folder in ["library", "domains", "patterns", "project-workflows", "vocabularies", "inbox", "templates", "standards", "docs"]:
    for path in glob.glob(os.path.join(root, folder, "**", "*"), recursive=True):
        if os.path.isfile(path) and path.endswith((".json", ".md", ".txt", ".cs", ".py")):
            text = open(path, encoding="utf-8", errors="replace").read()
            if HIDDEN.search(text): errors.append(f"{os.path.relpath(path, root)}: contains hidden Unicode characters")
for f in ["AGENTS.md", "llms.txt", "index.json", "README.md"]:
    path = os.path.join(root, f)
    if os.path.exists(path) and HIDDEN.search(open(path, encoding="utf-8").read()): errors.append(f"{f}: contains hidden Unicode characters")
# Executable checks must stay read-only: no transactions, no writes, no deletes, no sync/export, no file or network access
FORBIDDEN = re.compile(r"\b(Transaction|TransactionGroup|SubTransaction|Delete|\.Set\(|SynchronizeWithCentral|Export\(|SaveAs|Save\(|File\.|Directory\.|Process|WebClient|HttpClient|Assembly\.Load)")
for dp, dn, fn in os.walk(os.path.join(root, "library")):
    if os.path.basename(dp) == "checks":
        for f in fn:
            src = open(os.path.join(dp, f), encoding="utf-8").read()
            hit = FORBIDDEN.search(src)
            if hit: errors.append(f"{os.path.relpath(os.path.join(dp, f), root)}: check scripts must be read-only (found '{hit.group(0)}')")

print(f"{len(ids)} packs checked, {len(errors)} problems")
for e in errors: print(" -", e)
sys.exit(1 if errors else 0)
