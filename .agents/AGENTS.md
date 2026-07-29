# Agent Rules

- **Package Installation Reminder**: Whenever the user asks to install a package or whenever you provide instructions that involve installing a package, you must remind the user to:
  1. Open the Git Bash terminal.
  2. Navigate to the project directory (`cd /d/git_repo/TKprof_book`).
  3. Activate the Python 3.11 environment (`source venv/Scripts/activate`).
  *(As documented in `venv_setup_guide.md`)*

- **Audio Quality Requirements**: Before writing, modifying, or generating ANY audio-related code or files, you MUST read `authors_republic_requirements.md` in the project root and verify your work satisfies ALL of the following:
  - RMS between **-23 dB and -18 dB** (target: -19 dB)
  - Peak amplitude no higher than **-3.0 dB**
  - **1–5 seconds of clean silence** at both the start AND end of every track
  - Sample rate exactly **44,100 Hz**, CBR at **192 kbps or higher** (all files in the project must match the exact same bitrate)
  - After generating any audio file, run `check_audio_quality.py` on the output to confirm it passes before considering the task done.

- **Literary Translation Workflow**: Before undertaking any translation, editing, or text refinement tasks, you MUST read [translation_workflow_guide.md](file:///d:/git_repo/TKprof_book/translation_workflow_guide.md) in the project root and ensure you use high-tier reasoning models, apply the multi-step critique loop, respect contextual kinship rules, and perform human-in-the-loop validation using proposal files.

- **Tagging Integrity Validation**: Before generating audio for any book chapters, you MUST verify that the text inside the tagged version (e.g., `tagged_ch_*.txt`) matches the source chapter text (e.g., `ch_*.txt`) exactly (ignoring tags, whitespace, and punctuation) to prevent hallucinations, text omissions, or duplications introduced by LLM tagging steps. Run `check_tagging_integrity.py` to automate this verification.

- **Quotation Mark Removal in JSON Scripts**: When writing or updating dialogue script preparers (e.g. `prepare_scripts.py`), always strip leading and trailing double/single quotation marks (including curly quotes `“`, `”`) from the dialogue segment text fields (e.g. `speech.strip().strip('"\'“”')`) so that JSON files contain clean direct speech values and avoid escaping redundancy (`\"`).

- **Subagents for Translation & Modernization**: Avoid calling external APIs directly via scripts (such as `modernize_book.py` or `translate_book.py` using Gemini API keys) to avoid quota and key limits. Instead, define and spawn a specialized subagent to process chapters or text segments. You MUST run translation, editing, and text refinement tasks using the latest high-tier reasoning/pro model (`pro`) to ensure literary quality.

- **Clarifying Modernization Prompts**: When modernizing texts for ESL or easy-listening (TTS) purposes, avoid pairing conflicting directives like "preserve historical/gothic tone" with "simplify vocabulary." Directives must prioritize contemporary clarity and clear English as the primary constraint to ensure the model successfully simplifies archaic structures.
- **KDP Publishing Forms**: When advising the user on publishing or preparing metadata for the Amazon Kindle Store, always consult and use the form structure and high-converting title formula defined in [kdp_publishing_form.md](file:///d:/git_repo/TKprof_book/notes/kdp_publishing_form.md).

- **Explanatory Translation Loop (English -> Korean -> English)**: For high-context historical or philosophical texts, enhance accessibility for ESL/young readers by performing a double-translation loop:
  1. Translate the modernized English to Korean using the polite style (`하십시오체`), simplifying phrasing and weaving in natural, inline contextual explanations for historical figures, objects, and concepts.
  2. Translate the resulting Korean version back into English. This naturally captures the simplified sentence structure and inline definitions in contemporary English, producing a fully self-explanatory English edition.

