# Agent Rules

- **Package Installation Reminder**: Whenever the user asks to install a package or whenever you provide instructions that involve installing a package, you must remind the user to:
  1. Open the WSL terminal.
  2. Navigate to the project directory (`cd /mnt/d/git_repo/TKprof_book`).
  3. Activate the Linux Python 3.11 environment (`source wsl_venv/bin/activate`).
  *(As documented in `venv_setup_guide.md`)*

- **Audio Quality Requirements**: Before writing, modifying, or generating ANY audio-related code or files, you MUST read `authors_republic_requirements.md` in the project root and verify your work satisfies ALL of the following:
  - RMS between **-23 dB and -18 dB** (target: -19 dB)
  - Peak amplitude no higher than **-3.0 dB**
  - **1–5 seconds of clean silence** at both the start AND end of every track
  - Sample rate exactly **44,100 Hz**, CBR at **192 kbps or higher**
  - After generating any audio file, run `check_audio_quality.py` on the output to confirm it passes before considering the task done.
