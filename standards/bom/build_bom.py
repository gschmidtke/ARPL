"""Reference builder for the ARPL BOM standard (ARPL-BOM-0001).

Reads the INSTANCE PARAMETERS exports of a federation and the category rule table,
writes the model-quantity BOM, its trace to every model element, and the exceptions.
Read-only on the inputs; writes only to the output folder. Standard library only.

Usage:
  python build_bom.py --rules category-rules.csv --out OUTDIR [--phases "New Construction"] EXPORT.csv [EXPORT.csv ...]

The discipline of each row is the first letter of its instance key (SNOW_InstElemId,
e.g. 'P-PP-101-004' -> P). Rename the SNOW_ prefix with --prefix for other projects.
"""
import argparse, csv, hashlib, os, re
from collections import defaultdict, OrderedDict

FT_IN = re.compile(r"^\s*(-?\d+)'\s*-?\s*(?:(\d+(?:\.\d+)?)\s*)?(?:(\d+)/(\d+))?\s*\"?\s*$")
NUM_UNIT = re.compile(r"^\s*(-?[\d,]*\.?\d+)\s*([A-Za-z]*)\s*$")


def length_ft(text):
    """Feet from Revit's formatted length ('1' - 5 31/32"', '7'-10"') or a plain number in feet."""
    m = FT_IN.match(text or "")
    if m:
        inches = float(m.group(2) or 0) + (float(m.group(3)) / float(m.group(4)) if m.group(3) else 0)
        return float(m.group(1)) + inches / 12
    m = NUM_UNIT.match(text or "")
    return float(m.group(1).replace(",", "")) if m and m.group(2) in ("", "ft") else None


def number_unit(text):
    m = NUM_UNIT.match(text or "")
    return (float(m.group(1).replace(",", "")), m.group(2).upper()) if m else (None, None)


def quantity(rule, row):
    basis, field = rule["quantity_basis"], rule["quantity_field"]
    if basis == "count":
        return 1.0
    raw = row.get(field, "")
    if basis == "length":
        return length_ft(raw)
    value, unit = number_unit(raw)
    if value is None:
        return None
    if basis == "area":
        return value if unit in ("SF", "") else None
    if basis == "volume":
        return value / 27.0 if unit in ("CF", "") else (value if unit == "CY" else None)
    return None


def read_export(path, prefix):
    with open(path, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.reader(f))
    head_at = next(i for i, r in enumerate(rows) if r and r[0] == "Category")
    header = rows[head_at]
    model = os.path.basename(path).rsplit("_", 1)[0]
    for r in rows[head_at + 1:]:
        row = dict(zip(header, r))
        if row.get(f"{prefix}UniqueId", "").strip() or row.get(f"{prefix}InstElemId", "").strip():
            yield model, row


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rules", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--prefix", default="SNOW_")
    ap.add_argument("--phases", default="New Construction", help="phases whose elements are bought, separated by '|'")
    ap.add_argument("exports", nargs="+")
    a = ap.parse_args()
    P = a.prefix
    buy_phases = {x.strip() for x in a.phases.split("|") if x.strip()}
    with open(a.rules, encoding="utf-8", newline="") as f:
        rules = list(csv.DictReader(f))
    by_cat = defaultdict(list)
    for r in rules:
        by_cat[r["category"]].append(r)

    items = OrderedDict()            # bom_item_key -> aggregate
    trace, exceptions, seen = [], [], set()
    key_owners = defaultdict(set)    # instance key -> {(unique id, nested_parts)}
    rows_in = 0
    for path in a.exports:
        for model, row in read_export(path, P):
            uid = row.get(f"{P}UniqueId", "").strip()
            key_id = row.get(f"{P}InstElemId", "").strip()
            cat = row.get("Category", "")
            if not uid:              # nested part: carries its parent's key, no id of its own (ARPL-PAR-0003)
                rows_in += 1
                own = any(r["nested_parts"] == "own_item" for r in by_cat.get(cat, []))
                reason = (f"nested {cat} under {key_id} is its own item but has no unique id: fill its ids (ARPL-PAR-0003)" if own
                          else f"part of {key_id}: bought with its parent")
                exceptions.append([model, "", cat, reason]); continue
            if uid in seen:          # one element can be exported on several rows (FP55)
                continue
            seen.add(uid); rows_in += 1
            disc = key_id[:1]
            phase = row.get(f"{P}PhaseCreated", "").strip()
            if phase and phase not in buy_phases:
                exceptions.append([model, uid, cat, f"phase {phase}: not bought"]); continue
            candidates = [r for r in by_cat.get(cat, []) if r["source_discipline"] == disc]
            if not candidates:
                reason = "category counted from another discipline's model" if by_cat.get(cat) else "no rule for this category"
                exceptions.append([model, uid, cat, reason]); continue
            material = (row.get(f"{P}StructuralMaterial", "") + " " + row.get(f"{P}PipeMaterial", "")).lower()
            rule = next((r for r in candidates if r["when_material_contains"] and r["when_material_contains"].lower() in material), None) \
                or next((r for r in candidates if not r["when_material_contains"]), None)
            if rule is None:
                exceptions.append([model, uid, cat, "no rule for this material"]); continue
            q = quantity(rule, row)
            if q is None:
                exceptions.append([model, uid, cat, f"quantity field {rule['quantity_field']} empty or unreadable"]); continue
            fields = [g for g in rule["grouping_fields"].split("|") if g]
            signature = " | ".join(f"{g}={row.get(g, '').strip()}" for g in fields)
            bom_key = f"{disc}-{rule['code']}-" + hashlib.sha1(f"{rule['rule_id']}|{signature}".encode()).hexdigest()[:6].upper()
            missing = [f for f in rule["required_fields"].split("|") if f and not row.get(f, "").strip()]
            it = items.setdefault(bom_key, {"discipline": disc, "category": cat, "rule_id": rule["rule_id"], "signature": signature,
                                            "unit": rule["unit"], "qty": 0.0, "n": 0, "missing": 0, "levels": defaultdict(float)})
            it["qty"] += q; it["n"] += 1; it["missing"] += 1 if missing else 0
            level = row.get("Level", "").strip() or "(no level)"
            it["levels"][level] += q
            room = (row.get("Room: Number", "") or row.get("Space: Number", "")).strip()
            trace.append([bom_key, model, uid, key_id, level, room, round(q, 3)])
            key_owners[key_id].add((uid, rule["nested_parts"]))

    os.makedirs(a.out, exist_ok=True)
    rnd = lambda u, v: round(v) if u == "EA" else round(v, 1)
    with open(os.path.join(a.out, "bom.csv"), "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["bom_item_key", "discipline", "category", "rule_id", "item_signature", "unit", "model_quantity", "instance_count", "missing_required", "by_level"])
        for k, it in sorted(items.items(), key=lambda x: (x[1]["discipline"], x[1]["category"], -x[1]["qty"])):
            w.writerow([k, it["discipline"], it["category"], it["rule_id"], it["signature"], it["unit"], rnd(it["unit"], it["qty"]), it["n"], it["missing"],
                        "; ".join(f"{lv}: {rnd(it['unit'], v)}" for lv, v in sorted(it["levels"].items()))])
    with open(os.path.join(a.out, "bom_trace.csv"), "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f); w.writerow(["bom_item_key", "source_model", "snow_uniqueid", "snow_instelemid", "level", "room_or_space", "quantity"]); w.writerows(trace)
    with open(os.path.join(a.out, "bom_exceptions.csv"), "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f); w.writerow(["source_model", "snow_uniqueid", "category", "reason"]); w.writerows(exceptions)
    # Several elements under one key is expected only where nested parts are own items (chairs under a table)
    odd = [k for k, v in key_owners.items() if len(v) > 1 and any(np != "own_item" for _, np in v) and sum(1 for _, np in v if np != "own_item") > 1]
    if odd:
        print(f"warning: {len(odd)} instance keys carry several unique elements outside own_item categories, e.g. {odd[:3]}")
    # Reconciliation: every input row is either traced to exactly one BOM line or listed as an exception
    assert rows_in == len(trace) + len(exceptions), "reconciliation failed"
    print(f"elements {rows_in}: traced {len(trace)} into {len(items)} BOM lines, exceptions {len(exceptions)}")


if __name__ == "__main__":
    main()
