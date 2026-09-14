"""
Snapshot and restore the translation, so a style change can be undone.

Voice D rewrites every Korean paragraph in the book. If it reads worse than the formal
version -- or reads better but loses accuracy -- there has to be a way back that does not
involve regenerating 271 items and hoping they come out the same. They would not: the
model is stochastic, so "just run it again" is not a restore.

    python snapshot.py save formal      # before the change
    python snapshot.py list
    python snapshot.py restore formal   # put it all back

Copies both the translation output and the built app assets, because the two must agree.
"""
import json
import os
import shutil
import sys
import time

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE = os.path.dirname(os.path.abspath(__file__))
BATCH = os.path.join(BASE, "batches")
SNAP = os.path.join(BASE, "snapshots")
ASSETS = r"C:\git_repo\Book_apps\samguk_yusa\src\main\assets\books"


def save(name):
    dest = os.path.join(SNAP, name)
    if os.path.exists(dest):
        stamp = time.strftime("%Y%m%d-%H%M%S")
        os.rename(dest, f"{dest}.replaced-{stamp}")
        print(f"  existing snapshot moved aside -> {os.path.basename(dest)}.replaced-{stamp}")
    os.makedirs(os.path.join(dest, "batches"), exist_ok=True)
    os.makedirs(os.path.join(dest, "assets"), exist_ok=True)

    n = 0
    for f in sorted(os.listdir(BATCH)):
        if f.startswith("result_") and f.endswith(".json"):
            shutil.copy2(os.path.join(BATCH, f), os.path.join(dest, "batches", f))
            n += 1
    m = 0
    if os.path.isdir(ASSETS):
        for f in sorted(os.listdir(ASSETS)):
            if f.endswith(".json"):
                shutil.copy2(os.path.join(ASSETS, f), os.path.join(dest, "assets", f))
                m += 1
    for extra in ("glossary.json", "manual.json", "translate_local.py"):
        p = os.path.join(BASE, extra)
        if os.path.exists(p):
            shutil.copy2(p, os.path.join(dest, extra))

    meta = {"name": name, "saved": time.strftime("%Y-%m-%d %H:%M:%S"),
            "results": n, "assets": m}
    json.dump(meta, open(os.path.join(dest, "snapshot.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print(f"saved '{name}': {n} result files, {m} asset files -> {dest}")


def restore(name):
    src = os.path.join(SNAP, name)
    if not os.path.isdir(src):
        raise SystemExit(f"no snapshot named '{name}' in {SNAP}")
    n = m = 0
    for f in sorted(os.listdir(os.path.join(src, "batches"))):
        shutil.copy2(os.path.join(src, "batches", f), os.path.join(BATCH, f))
        n += 1
    adir = os.path.join(src, "assets")
    if os.path.isdir(adir) and os.path.isdir(ASSETS):
        for f in sorted(os.listdir(adir)):
            shutil.copy2(os.path.join(adir, f), os.path.join(ASSETS, f))
            m += 1
    for extra in ("glossary.json", "manual.json"):
        p = os.path.join(src, extra)
        if os.path.exists(p):
            shutil.copy2(p, os.path.join(BASE, extra))
    print(f"restored '{name}': {n} result files, {m} asset files")
    print("  glossary.json and manual.json restored too; translate_local.py was NOT "
          "overwritten (compare it against the snapshot copy by hand if needed)")


def listing():
    if not os.path.isdir(SNAP):
        print("no snapshots yet")
        return
    for d in sorted(os.listdir(SNAP)):
        meta = os.path.join(SNAP, d, "snapshot.json")
        if os.path.exists(meta):
            j = json.load(open(meta, encoding="utf-8"))
            print(f"  {j['name']:<20} {j['saved']}  {j['results']} results, {j['assets']} assets")
        else:
            print(f"  {d:<20} (no metadata)")


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ("save", "restore", "list"):
        raise SystemExit(__doc__)
    cmd = sys.argv[1]
    if cmd == "list":
        listing()
        return
    if len(sys.argv) < 3:
        raise SystemExit(f"usage: python snapshot.py {cmd} <name>")
    (save if cmd == "save" else restore)(sys.argv[2])


if __name__ == "__main__":
    main()
