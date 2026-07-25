# Virtual Environment Setup Guide

This project relies on Python libraries e.g., `kokoro`, `pydub`, `edge-tts`, `soundfile`, `numpy`) and requires **Python 3.11**.

All scripts in this project are run natively on Windows using **Git Bash** or **PowerShell** with the local `./venv` environment.

---

## 1. Quick Setup (Git Bash)

### Prerequisites
1. Make sure you have **Python 3.11** installed on Windows.
2. Make sure **FFmpeg** is installed on Windows and added to your system `PATH`.

### Creating & Activating the Environment
1. Open Git Bash terminal.
2. Navigate to the project root:
   ```bash
   cd /d/git_repo/TKprof_book
   ```
3. Create the virtual environment (named `venv`):
   ```bash
   python -m venv venv
   ```
4. Activate the virtual environment:
   ```bash
   source venv/Scripts/activate
   ```
   *(PowerShell alternative: `.\venv\Scripts\Activate.ps1`)*

---

## 2. Installing Dependencies

Once `(venv)` is activated, install the required project packages:

```bash
pip install kokoro soundfile pydub edge-tts numpy
```

Verify your Python version:
```bash
python --version  # Should output Python 3.11.x
```

