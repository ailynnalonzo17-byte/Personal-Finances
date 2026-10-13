#!/usr/bin/env python3
"""
VA Optional automation ID translator.

Two jobs, one dictionary (Airtable table + field NAMES, which survive a base
copy; IDs do not).

  extract  (owner side, run by the Flow Packager)
      Turn a real n8n workflow into a shareable TEMPLATE: every Airtable base/
      table/field ID, the Slack channel, and the owner's email(s) are replaced
      with named placeholders. Emits template.json + namemap.json.
      Validates: every app/tbl/fld ID in the workflow is found in the owner's
      base schema. An unknown ID means we cannot package it safely -> hard stop.

  apply    (member side, run by the Automation Installer)
      Fill a TEMPLATE for one member: look each placeholder's NAME up in the
      member's base schema, substitute THEIR id. Emits the member's workflow.
      Validates, in order:
        completeness  every table/field name the flow needs exists in the
                      member's base (missing/renamed -> plain-English stop)
        round-trip    each member id we chose maps back to the expected name
        no-remainder  zero {{...}} left, zero surviving owner ids

Placeholders:
  {{BASE_ID}}
  {{TBL::<Table Name>}}
  {{FLD::<Table Name>::<Field Name>}}
  {{SLACK_CHANNEL}}
  {{VAR::<KEY>}}          # free literals, e.g. an email address

A "schema" file is compact JSON: {"baseId": "...", "tables":[{"id","name",
"fields":[{"id","name"}]}]}.
"""
import json
import re
import sys
import argparse

# Table/field IDs have unambiguous prefixes — no English word starts with
# "tbl"/"fld" + 14 chars, so matching these is safe. Base IDs ("app" + 14) DO
# collide with code identifiers like "appendAttribution", so the base ID is
# never regex-scanned: only the one known base ID from the schema is replaced.
TBLFLD_RE = re.compile(r'(?:tbl|fld)[A-Za-z0-9]{14}')
# Our placeholders use a %%VAO::...%% sentinel, NOT {{...}}, because n8n
# expressions ({{ $json.x }}) and the Google Doc merge tags ({{Tenant}}) both
# use {{ }} and would collide. The remainder check scans only for our sentinel.
VAO_RE = re.compile(r'%%VAO::[^%]+%%')


def ph(inner):
    """Wrap a placeholder body in the collision-proof sentinel."""
    return f"%%VAO::{inner}%%"


def load(path):
    with open(path) as f:
        return json.load(f)


def build_indexes(schema):
    """From a base schema build id->name lookups and name->id lookups."""
    base_id = schema["baseId"]
    tbl_id_to_name, tbl_name_to_id = {}, {}
    fld_id_to_key, fld_key_to_id = {}, {}   # key = (table_name, field_name)
    for t in schema["tables"]:
        tbl_id_to_name[t["id"]] = t["name"]
        tbl_name_to_id[t["name"]] = t["id"]
        for fdef in t.get("fields", []):
            key = (t["name"], fdef["name"])
            fld_id_to_key[fdef["id"]] = key
            fld_key_to_id[key] = fdef["id"]
    return {
        "base_id": base_id,
        "tbl_id_to_name": tbl_id_to_name, "tbl_name_to_id": tbl_name_to_id,
        "fld_id_to_key": fld_id_to_key, "fld_key_to_id": fld_key_to_id,
    }


def extract(args):
    raw = open(args.workflow).read()
    schema = load(args.schema)
    idx = build_indexes(schema)

    ids_in_flow = sorted(set(TBLFLD_RE.findall(raw)))
    unknown, namemap = [], {"base": None, "tables": [], "fields": [], "literals": []}

    text = raw
    # base — only the one known base ID, never a regex scan (avoids code words)
    if idx["base_id"] in text:
        text = text.replace(idx["base_id"], ph("BASE_ID"))
        # Record only THAT the flow uses a base id, never WHICH one. apply() reads the
        # base id from the member's own schema, so the owner's is pure leakage here.
        namemap["base"] = True
    # tables + fields — matched against the real schema
    seen_tbl, seen_fld = set(), set()
    for _id in ids_in_flow:
        if _id.startswith("tbl"):
            name = idx["tbl_id_to_name"].get(_id)
            if not name:
                unknown.append(_id); continue
            text = text.replace(_id, ph(f"TBL::{name}"))
            if name not in seen_tbl:
                seen_tbl.add(name)
                namemap["tables"].append({"placeholder": f"TBL::{name}", "table": name})
        elif _id.startswith("fld"):
            key = idx["fld_id_to_key"].get(_id)
            if not key:
                unknown.append(_id); continue
            tname, fname = key
            text = text.replace(_id, ph(f"FLD::{tname}::{fname}"))
            if (tname, fname) not in seen_fld:
                seen_fld.add((tname, fname))
                namemap["fields"].append({"placeholder": f"FLD::{tname}::{fname}",
                                           "table": tname, "field": fname})
    # literals (slack channel + emails) supplied on the command line
    for spec in args.literal or []:
        key, val = spec.split("=", 1)
        if val in text:
            text = text.replace(val, ph(f"VAR::{key}"))
            namemap["literals"].append({"placeholder": f"VAR::{key}", "key": key})

    # validation: unknown ids
    if unknown:
        print("EXTRACT FAILED — these IDs are not in the base schema, cannot "
              "package safely:", file=sys.stderr)
        for u in unknown:
            print("   ", u, file=sys.stderr)
        sys.exit(2)
    # validation: no owner ids survived
    survivors = TBLFLD_RE.findall(text)
    if idx["base_id"] in text:
        survivors.append(idx["base_id"])
    if survivors:
        print("EXTRACT FAILED — owner IDs still present after templating:",
              sorted(set(survivors)), file=sys.stderr)
        sys.exit(2)

    json.loads(text)  # must still be valid JSON

    # A card that leaks is never written. --forbid carries owner-specific words
    # (her name, brand, n8n hostname) that no generic pattern would catch.
    forbid = list(args.forbid or []) + [idx["base_id"]]
    found = [f for f in scan_text(text, forbid)
             if not any(re.search(a, f[1], re.I) for a in (args.allow or []))]
    if not report_leaks(found, args.out):
        print("Nothing was written.", file=sys.stderr)
        sys.exit(4)

    with open(args.out, "w") as f:
        f.write(text)
    with open(args.namemap, "w") as f:
        json.dump(namemap, f, indent=2)
    print(f"EXTRACT OK — {len(namemap['tables'])} tables, "
          f"{len(namemap['fields'])} fields, {len(namemap['literals'])} literals "
          f"templated. Wrote {args.out} and {args.namemap}.")



# --------------------------------------------------------------------------
# Leak scan. Runs automatically at the end of every extract; a card that fails
# it is never written. Also available on its own: `translate.py scan --path ...`
# --------------------------------------------------------------------------
LEAK_PATTERNS = [
    ("private key",            r"-----BEGIN [A-Z ]*PRIVATE KEY"),
    ("Airtable table id",      r"tbl[A-Za-z0-9]{14}"),
    ("Airtable field id",      r"fld[A-Za-z0-9]{14}"),
    ("Airtable record id",     r"rec[A-Za-z0-9]{14}"),
    ("Airtable PAT",           r"pat[A-Za-z0-9]{14,}"),
    ("Slack channel id",       r"\bC0[A-Z0-9]{8,}\b"),
    ("Slack/xox token",        r"xox[abprs]-[A-Za-z0-9-]+"),
    ("n8n API key",            r"n8n_api_[A-Za-z0-9]+"),
    ("email address",          r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"),
    ("bearer token literal",   r"Bearer\s+[A-Za-z0-9._-]{20,}"),
]


def scan_text(text, forbid=None):
    """Return a list of (label, sample) for anything that must not ship."""
    found = []
    for label, pat in LEAK_PATTERNS:
        for m in re.finditer(pat, text):
            found.append((label, m.group(0)[:60]))
    for word in (forbid or []):
        if not word:
            continue
        for m in re.finditer(re.escape(word), text, re.I):
            ctx = text[max(0, m.start() - 45):m.start() + 55].replace("\n", " ")
            found.append((f"forbidden word '{word}'", f"...{ctx}..."))
    return found


def report_leaks(found, where):
    if not found:
        print(f"LEAK SCAN OK — {where} carries nothing owner-specific.")
        return True
    print(f"LEAK SCAN FAILED — {where} still contains:", file=sys.stderr)
    seen = set()
    for label, sample in found:
        if (label, sample) in seen:
            continue
        seen.add((label, sample))
        print(f"    {label}: {sample}", file=sys.stderr)
    return False


def readable_text(path):
    """Text of a file, or None if we cannot read it honestly.

    A PDF's raw bytes are compressed, so scanning them both misses real text AND
    invents matches out of binary. Extract the page text instead, and if that is
    not possible, say so rather than reporting a clean pass over nothing.
    """
    if path.lower().endswith(".pdf"):
        try:
            try:
                from pypdf import PdfReader
            except ImportError:
                from PyPDF2 import PdfReader
            txt = "\n".join(pg.extract_text() or "" for pg in PdfReader(path).pages)
        except Exception:
            return None
        return txt if txt.strip() else None
    try:
        return open(path, encoding="utf-8", errors="ignore").read()
    except Exception:
        return None


def scan(args):
    import os
    bad = 0
    targets = []
    if os.path.isdir(args.path):
        for f in sorted(os.listdir(args.path)):
            targets.append(os.path.join(args.path, f))
    else:
        targets.append(args.path)
    for t in targets:
        name = os.path.basename(t)
        text = readable_text(t)
        if text is None:
            print(f"LEAK SCAN COULD NOT READ {name} — check it by hand before "
                  f"committing. A file we cannot read is not a file we cleared.",
                  file=sys.stderr)
            bad += 1
            continue
        found = [f for f in scan_text(text, args.forbid)
                 if not any(re.search(a, f[1], re.I) for a in (args.allow or []))]
        if not report_leaks(found, name):
            bad += 1
    if bad:
        print(f"\n{bad} file(s) failed. This card must NOT be committed.", file=sys.stderr)
        sys.exit(4)
    print("\nAll files clean.")


def apply_(args):
    template = open(args.template).read()
    namemap = load(args.namemap)
    schema = load(args.schema)
    idx = build_indexes(schema)
    literals = {}
    for spec in args.value or []:
        k, v = spec.split("=", 1)
        literals[k] = v

    missing = []
    # completeness — every needed name exists in member base
    for t in namemap["tables"]:
        if t["table"] not in idx["tbl_name_to_id"]:
            missing.append(f'table "{t["table"]}"')
    for fl in namemap["fields"]:
        if (fl["table"], fl["field"]) not in idx["fld_key_to_id"]:
            missing.append(f'field "{fl["table"]} :: {fl["field"]}"')
    for lit in namemap["literals"]:
        if lit["key"] not in literals:
            missing.append(f'value "{lit["key"]}" (pass --value {lit["key"]}=...)')
    if missing:
        print("APPLY STOPPED — the member's base is missing things this "
              "automation needs:", file=sys.stderr)
        for m in missing:
            print("   -", m, file=sys.stderr)
        sys.exit(3)

    text = template
    text = text.replace(ph("BASE_ID"), idx["base_id"])
    chosen = {}  # placeholder -> member id, for round-trip check
    for t in namemap["tables"]:
        mid = idx["tbl_name_to_id"][t["table"]]
        chosen[("tbl", t["table"])] = mid
        text = text.replace(ph(t["placeholder"]), mid)
    for fl in namemap["fields"]:
        mid = idx["fld_key_to_id"][(fl["table"], fl["field"])]
        chosen[("fld", fl["table"], fl["field"])] = mid
        text = text.replace(ph(fl["placeholder"]), mid)
    for lit in namemap["literals"]:
        text = text.replace(ph(lit["placeholder"]), literals[lit["key"]])

    # round-trip — every id we chose maps back to the expected name
    rt_fail = []
    for key, mid in chosen.items():
        if key[0] == "tbl":
            if idx["tbl_id_to_name"].get(mid) != key[1]:
                rt_fail.append(f'table {key[1]}')
        else:
            got = idx["fld_id_to_key"].get(mid)
            if got != (key[1], key[2]):
                rt_fail.append(f'field {key[1]} :: {key[2]}')
    if rt_fail:
        print("APPLY FAILED — round-trip mismatch:", rt_fail, file=sys.stderr)
        sys.exit(3)

    # no-remainder (our sentinel only — never n8n's own {{ }} expressions)
    left = VAO_RE.findall(text)
    if left:
        print("APPLY FAILED — unsubstituted placeholders remain:",
              sorted(set(left)), file=sys.stderr)
        sys.exit(3)

    json.loads(text)
    with open(args.out, "w") as f:
        f.write(text)
    print(f"APPLY OK — rendered {args.out} for base {idx['base_id']}: "
          f"{len(namemap['tables'])} tables, {len(namemap['fields'])} fields "
          f"translated, all round-tripped, no placeholders left.")


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    e = sub.add_parser("extract", help="owner: workflow -> template + namemap")
    e.add_argument("--workflow", required=True)
    e.add_argument("--schema", required=True, help="owner's base schema (compact)")
    e.add_argument("--out", required=True, help="template.json to write")
    e.add_argument("--namemap", required=True, help="namemap.json to write")
    e.add_argument("--allow", action="append", default=[],
                   help="regex for a deliberate placeholder that is not a leak")
    e.add_argument("--forbid", action="append", default=[],
                   help="owner-specific word that must not survive, e.g. --forbid Sunrise")
    e.add_argument("--literal", action="append",
                   help="KEY=value literal to templatize, e.g. SLACK_CHANNEL=C0...")
    e.set_defaults(func=extract)

    a = sub.add_parser("apply", help="member: template + namemap -> member workflow")
    a.add_argument("--template", required=True)
    a.add_argument("--namemap", required=True)
    a.add_argument("--schema", required=True, help="member's base schema (compact)")
    a.add_argument("--out", required=True)
    a.add_argument("--value", action="append",
                   help="KEY=value for each literal, e.g. AGENT_EMAIL=me@x.com")
    a.set_defaults(func=apply_)

    sc = sub.add_parser("scan", help="check a file or a whole card folder for leaks")
    sc.add_argument("--path", required=True)
    sc.add_argument("--forbid", action="append", default=[],
                    help="owner-specific word that must not survive")
    sc.add_argument("--allow", action="append", default=[],
                    help="regex for a deliberate placeholder, e.g. --allow 'you@yourcompany'")
    sc.set_defaults(func=scan)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
