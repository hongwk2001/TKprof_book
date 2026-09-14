"""
One command: fix, re-translate, audit twice, migrate, and report.

Run it and go to bed. Everything lands in audit/, with SUMMARY.md as the thing to read
first. Nothing here needs a key or a network -- it is all local Ollama.

Stages:
    1  translate  --en-only   Korean is re-split with the fixed splitter and kept as the
                              anchor; English is regenerated one paragraph at a time into
                              fixed slots, so a shifted card becomes impossible
    2  audit                  deterministic: ratio divergence, fragments, tail stubs,
                              glossary coverage, script leakage, register
    3  llm_audit              semantic: does EN paragraph N say what KO paragraph N says
    4  migrate                build the app assets, refusing any misaligned chapter
    5  summary                SUMMARY.md

A stage that fails does not stop the run -- a failed stage with a report is more useful
in the morning than a dead terminal.

Usage:  python overnight.py
        python overnight.py --model gemma4:12b
        python overnight.py --skip-translate      # audit what is already there
"""
import argparse
import json
import os
import subprocess
import sys
import time

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "audit")
LOGS = os.path.join(OUT, "logs")
MIGRATE = r"C:\git_repo\Book_apps\samguk_yusa\migrate_samguk_yusa.py"
ASSETS = r"C:\git_repo\Book_apps\samguk_yusa\src\main\assets\books"


def run(name, args, cwd=BASE):
    """Run one stage, tee its output to a log, and never raise."""
    os.makedirs(LOGS, exist_ok=True)
    log = os.path.join(LOGS, f"{name}.log")
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    print(f"\n{'=' * 62}\n[{time.strftime('%H:%M:%S')}] {name}\n{'=' * 62}", flush=True)
    t0 = time.time()
    with open(log, "w", encoding="utf-8") as fh:
        try:
            p = subprocess.Popen([sys.executable, "-u", *args], cwd=cwd, env=env,
                                 stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                 text=True, encoding="utf-8", errors="replace")
            for line in p.stdout:
                fh.write(line)
                if line.strip():
                    print("   " + line.rstrip(), flush=True)
            code = p.wait()
        except Exception as exc:  # noqa: BLE001
            fh.write(f"\nCRASHED: {exc}\n")
            code = -1
    mins = (time.time() - t0) / 60
    print(f"[{time.strftime('%H:%M:%S')}] {name}: exit {code}, {mins:.1f} min", flush=True)
    return {"stage": name, "exit": code, "minutes": round(mins, 1), "log": log}


def read_results():
    import glob
    aligned = total = 0
    for f in sorted(glob.glob(os.path.join(BASE, "batches", "result_ch_*.json"))):
        d = json.load(open(f, encoding="utf-8"))
        aligned += d["aligned"]
        total += d["total"]
    return aligned, total


def card_stats():
    import glob
    import statistics as st
    ko, en = [], []
    for f in sorted(glob.glob(os.path.join(ASSETS, "ch_*.json"))):
        for r in json.load(open(f, encoding="utf-8")):
            if r.get("is_header"):
                continue
            ko.append(len(r["ko"]))
            en.append(len(r["en"]))
    if not ko:
        return None
    return {"rows": len(ko), "ko_mean": round(st.mean(ko)), "ko_max": max(ko),
            "en_mean": round(st.mean(en)), "en_max": max(en),
            "en_over_300": sum(1 for e in en if e > 300)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="gemma4:12b")
    ap.add_argument("--skip-translate", action="store_true")
    ap.add_argument("--en-only", action="store_true",
                    help="reuse the existing Korean (only valid if the Korean style has "
                         "not changed)")
    ap.add_argument("--snapshot", default="pre-run",
                    help="name to save the current text under before touching it")
    a = ap.parse_args()

    os.makedirs(OUT, exist_ok=True)
    started = time.strftime("%Y-%m-%d %H:%M")
    stages = []

    # Always snapshot first. A style change rewrites every Korean paragraph, and the
    # model is stochastic, so re-running is not a way back.
    if not a.skip_translate:
        stages.append(run("0-snapshot", ["snapshot.py", "save", a.snapshot]))
        args = ["translate_local.py", "all", "--model", a.model]
        if a.en_only:
            args.insert(2, "--en-only")
        stages.append(run("1-translate", args))
    stages.append(run("2-audit", ["audit.py", "all"]))

    env_model = os.environ.get("AUDIT_MODEL")
    os.environ["AUDIT_MODEL"] = a.model
    stages.append(run("3-llm-audit", ["llm_audit.py", "all"]))
    if env_model:
        os.environ["AUDIT_MODEL"] = env_model

    stages.append(run("4-migrate", [MIGRATE], cwd=os.path.dirname(MIGRATE)))

    # ---- summary -------------------------------------------------------------
    aligned, total = read_results()
    cards = card_stats()
    det = ""
    dlog = os.path.join(LOGS, "2-audit.log")
    if os.path.exists(dlog):
        det = open(dlog, encoding="utf-8").read()
    det_high = det.count("[high]")
    det_med = det.count("[ med]")

    llm = {}
    ppath = os.path.join(OUT, "problems.json")
    if os.path.exists(ppath):
        pj = json.load(open(ppath, encoding="utf-8"))
        for p in pj["problems"]:
            llm[p["verdict"]] = llm.get(p["verdict"], 0) + 1

    lines = [
        f"# Overnight run — {started}", "",
        f"model: `{a.model}`", "",
        "## Stages", "",
        "| stage | exit | minutes |", "|---|---:|---:|",
    ]
    lines += [f"| {s['stage']} | {s['exit']} | {s['minutes']} |" for s in stages]
    lines += ["", "## Alignment", "", f"- {aligned}/{total} items aligned", ""]
    if cards:
        lines += ["## Cards (vs werther: ko mean 101 / max 186, en mean 197 / max 300, 0 over 300)", "",
                  f"- rows **{cards['rows']}**",
                  f"- ko mean {cards['ko_mean']}, max {cards['ko_max']}",
                  f"- en mean {cards['en_mean']}, max {cards['en_max']}",
                  f"- en over 300: **{cards['en_over_300']}**", ""]
    lines += ["## Findings", "",
              f"- deterministic (`audit/logs/2-audit.log`): **{det_high} high**, {det_med} med",
              f"- semantic (`audit/problems.md`): **{sum(llm.values())}** — {llm or 'none'}", "",
              "## Read in this order", "",
              "1. `audit/problems.md` — SHIFTED first, that is the defect you heard",
              "2. `audit/logs/2-audit.log` — every `[high]` line",
              "3. `audit/logs/4-migrate.log` — any chapter it REFUSED to write", ""]

    with open(os.path.join(OUT, "SUMMARY.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))

    print("\n" + "\n".join(lines))
    print(f"\nwrote {OUT}\\SUMMARY.md")


if __name__ == "__main__":
    main()
