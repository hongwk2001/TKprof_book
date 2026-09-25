"""
Stage 5: apply Claude's reviewed ACCEPT/REVISE fixes (audit/claude_review/ch_NN.md)
directly to the shipped Book_apps asset rows.

Per user decision: this patches ONLY
    C:\\git_repo\\Book_apps\\samguk_yusa\\src\\main\\assets\\books\\ch_NN.json
It does NOT touch batches/result_ch_NN.json -- the two are allowed to diverge from
this point on. batches/result_ch_NN.json is read-only here, used only to look up how
many paragraphs a batch tag has (so a fix keyed "tag P0005, paragraph 2" can be mapped
to the app's flat row tag "P0005_2", per migrate_samguk_yusa.py's own tagging rule:
single-paragraph items keep the bare tag, multi-paragraph items get a _N suffix).

Before writing, each patch's OLD text is checked against the app row's current text --
if it doesn't match, the patch is skipped and reported rather than applied blind, since
that means either the row was already changed or the tag mapping is wrong.

Usage: python apply_fixes.py ch_01 patches/ch_01.json
       python apply_fixes.py ch_01 patches/ch_01.json --dry-run
"""
import json
import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE = os.path.dirname(os.path.abspath(__file__))
BATCH = os.path.join(BASE, "batches")
APP_ASSETS = r"C:\git_repo\Book_apps\samguk_yusa\src\main\assets\books"


def paragraph_counts(cid):
    """tag -> number of paragraphs, from the (read-only) pipeline result file."""
    result = json.load(open(os.path.join(BATCH, f"result_{cid}.json"), encoding="utf-8"))["items"]
    return {v["tag"]: len(v["ko"]) for v in result.values() if not v.get("manual")}


def app_tag(tag, n, counts):
    """Map a (batch tag, 1-indexed paragraph n) pair to the app's flat row tag."""
    total = counts.get(tag)
    if total is None:
        return None
    return tag if total == 1 else f"{tag}_{n}"


def apply_chapter(cid, patch_path, dry_run=False):
    counts = paragraph_counts(cid)
    app_path = os.path.join(APP_ASSETS, f"{cid}.json")
    rows = json.load(open(app_path, encoding="utf-8"))
    by_tag = {r["tag"]: r for r in rows}

    patches = json.load(open(patch_path, encoding="utf-8"))
    applied, skipped = 0, 0
    for p in patches:
        tag, n = p["tag"], p["n"]
        at = app_tag(tag, n, counts)
        if at is None:
            print(f"  SKIP {tag} n={n}: tag not found in result_{cid}.json")
            skipped += 1
            continue
        row = by_tag.get(at)
        if row is None:
            print(f"  SKIP {tag} n={n} (app tag {at}): row not found in {cid}.json")
            skipped += 1
            continue

        old_ko_expected = p.get("old_ko")
        old_en_expected = p.get("old_en")
        if old_ko_expected is not None and row["ko"] != old_ko_expected:
            print(f"  SKIP {at}: current ko doesn't match expected old text (already changed?)")
            skipped += 1
            continue
        if old_en_expected is not None and row["en"] != old_en_expected:
            print(f"  SKIP {at}: current en doesn't match expected old text (already changed?)")
            skipped += 1
            continue

        new_ko = p.get("ko", row["ko"])
        new_en = p.get("en", row["en"])
        if new_ko == row["ko"] and new_en == row["en"]:
            skipped += 1
            continue
        print(f"  {at}")
        if new_ko != row["ko"]:
            print(f"    KO- {row['ko']}")
            print(f"    KO+ {new_ko}")
        if new_en != row["en"]:
            print(f"    EN- {row['en']}")
            print(f"    EN+ {new_en}")
        if not dry_run:
            row["ko"], row["en"] = new_ko, new_en
        applied += 1

    if not dry_run:
        with open(app_path, "w", encoding="utf-8") as fh:
            json.dump(rows, fh, ensure_ascii=False, indent=1)

    print(f"{cid}: {applied} applied, {skipped} skipped")
    return applied, skipped


def main():
    cid = sys.argv[1]
    patch_path = sys.argv[2]
    dry_run = "--dry-run" in sys.argv
    apply_chapter(cid, patch_path, dry_run)


if __name__ == "__main__":
    main()
