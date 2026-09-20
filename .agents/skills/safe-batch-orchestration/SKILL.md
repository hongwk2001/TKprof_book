---
name: safe-batch-orchestration
description: An ultra-resilient multi-agent architecture for transforming large JSON datasets safely using wave-based batching.
---

# Safe Batch Orchestration Pipeline

When tasked with processing or translating thousands of JSON blocks, standard subagents will often hallucinate, corrupt JSON structures, or attempt to write buggy Python scripts that crash. 

To process large datasets flawlessly, you MUST use the following wave-based orchestration loop:

## 1. The Queue Generation
Create a script (e.g., `generate_queue.py`) that scans the master JSON files and outputs a `work_queue.json` containing ONLY the pending/missing blocks. Run this script at the start of every wave to dynamically find the remaining work.
*(Note: Always scan the target field for anomalies like "TRANSLATION MISSING" or lingering English characters via regex, and add those to the pending queue).*

## 2. The Safe Subagent Definition
Do NOT allow subagents to run Python scripts or terminal commands (`run_command`), as they will inevitably break. 
Spawn a specialized subagent (e.g., `SafeTranslator`) with strict instructions:
- Provide the exact indices (e.g., 0-99).
- Provide the required glossary and strict formatting rules.
- Instruct them to use ONLY `write_to_file` to output a raw JSON array to a temporary `batches` directory (e.g., `batch_0_99.json`).

## 3. Wave Dispatch (The Orchestrator)
Use a script (e.g., `prepare_wave.py`) to calculate the boundaries for the next 1,000 pending items. 
Spawn a maximum of 10 subagents in parallel (Wave N), assigning exactly 100 blocks to each to prevent token truncation and hallucinations.

## 4. The Deterministic Patch
Wait for all 10 subagents to finish writing their batch JSON files.
Run a deterministic Python script (e.g., `apply_patch.py`) that reads the batches and merges them back into the master JSON files matching EXACTLY on `file_name` and `id`. 
*Never let LLMs edit the master JSON files directly.*

## 5. The Verification Loop
Commit the patched master files to git after every wave.
Rerun `generate_queue.py` to get the next wave of pending items.
Repeat until the pending queue is exactly 0. 
Run a final strict programmatic audit (e.g., `check_english.py`) across all files to guarantee 100% compliance.
