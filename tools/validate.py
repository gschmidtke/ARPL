"""Validate every pack manifest against the schema and the controlled vocabularies.
Usage: python tools/validate.py   (needs: pip install jsonschema)"""
import json, glob, sys, os
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
print(f"{len(ids)} packs checked, {len(errors)} problems")
for e in errors: print(" -", e)
sys.exit(1 if errors else 0)
