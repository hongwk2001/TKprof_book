# 🏁 TKPROF AI Project Operational Parameters (CLAUDE.md)

This document outlines the strict operational constraints, commands, and architectural guardrails for AI agents executing tasks in this codebase.

## 🛠️ Core Commands & Workflows

### 1. Developer Agent Daemon
The file-backed mailbox daemon polls for tasks and executes them inside the WSL sandbox:
* **Run once (Polling):** `node .swarm/agent_daemon.js`
* **Continuous Loop:** `node .swarm/agent_daemon.js --continuous`

### 2. QA Test Runner (Automated Interception)
Run any test or command through the QA harness to automatically catch failures and pipe them back to the developer mailbox:
* **Syntax:** `node .swarm/test_runner.js <command_to_test> [args...]`
* **Example:** `node .swarm/test_runner.js node test.js`
* **Failure Output:** Generates a typed `error_<timestamp>.json` inside `.swarm/mailboxes/developer/inbox/` upon non-zero exit codes.

### 3. Triage Cockpit Manual Clearance Gate
Before writing files, executing builds, or deploying changes that affect the host machine or external state:
* **Handshake command:** `node .swarm/triage_cockpit.js "<action_name>" "<impact_summary>"`
* Must receive manual console keyboard input `APPROVE` to proceed (exit code 0).

---

## 📐 Codebase Directory Map

* `.swarm/` — All autonomous agent orchestration mechanisms.
  * `mailboxes/developer/inbox/` — Active tasks, incoming failure logs (`error_*.json`).
  * `mailboxes/developer/processed/` — History of completed task payloads and outputs.
  * `triage_cockpit.js` — The manual clearance gateway CLI.
  * `approve_gate.js` — JS module containing `requestClearance(...)` for programmatic gates.
  * `agent_daemon.js` — Polling mechanism for executing mailbox JSON tasks.
  * `test_runner.js` — Spawns child processes and logs typed errors back to the mailbox upon crash.
  * `progress.md` — The global ledger tracking active and finished milestones.
  * `mcp-filesystem/` — Sandboxed MCP file server for secure LLM file actions.
* `reels/` — Media automation pipeline (images, audio, FFmpeg stitches).
* `todo.md` — Active development goals and roadmap checklists.
* `retro_setup_summary.html` — Main interactive developer retro document.

---

## 🎯 Surgical Edit & Trace-Driven Rules
1. **Ban Speculative Rewrites:** Never rewrite code files from scratch unless explicitly requested. Every change must be a minimal, surgical diff patch.
2. **Trace-Driven Debugging:** Only modify the specific functional lines that are throwing exceptions, failing tests, or directly causing runtime errors as flagged in the `error_*.json` report.
3. **Branch Guardrail:** All modifications, testing, and script trials must strictly happen on the local Git `dev` branch.
4. **Read-Only Default:** Workflows default to read-only operation unless explicitly authorized by the physical developer via the triage cockpit console.
5. **Rule Synchronization:** These guidelines are paired with `/mnt/d/git_repo/thefirstaicompany/.cursorrules` which governs real-time Cursor Agent execution. Under no circumstances should an AI override or delete these instruction sets.
