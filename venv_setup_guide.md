# Virtual Environment Setup Guide

This project relies on some libraries (like `kokoro` for TTS and `torch`) that may not be fully compatible with the absolute newest versions of Python (e.g., 3.14). It is highly recommended to use **Python 3.11**.

Additionally, it is crucial to use the correct virtual environment for your operating system. **A Windows virtual environment will not work in WSL (Linux), and vice versa.** If you switch between Windows and WSL, you must create and use separate virtual environments.

---

## 1. Windows (PowerShell or Git Bash)

If you are running scripts natively in Windows, follow these steps.

### Prerequisites
Make sure you have Python 3.11 installed on Windows. 

### Creating the Environment
1. Open PowerShell or Git Bash.
2. Navigate to the project root:
   ```bash
   cd d:\git_repo\TKprof_book
   ```
3. Create the Windows virtual environment (named `venv`):
   ```bash
   python -m venv venv
   ```

### Activating the Environment
* **PowerShell:**
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
  *(Note: If PowerShell blocks the script, run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` first).*

* **Git Bash:**
  ```bash
  source venv/Scripts/activate
  ```

---

## 2. Linux (WSL / Ubuntu)

If you are running scripts inside Windows Subsystem for Linux (WSL), you **must** create a separate Linux virtual environment. Do not try to activate the Windows `venv` from inside WSL.

*(Note: You can easily enter your WSL environment directly from your Windows folder by opening Command Prompt (`cmd`) or PowerShell and typing `wsl`)*

### Prerequisites (Installing Python 3.11)
Ubuntu's default Python might be too new. Install Python 3.11 using the deadsnakes PPA:
```bash
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.11 python3.11-venv
```

### Creating the Environment
1. Navigate to the project root (using the `/mnt` path):
   ```bash
   cd /mnt/d/git_repo/TKprof_book
   ```
2. Create the Linux virtual environment (named `wsl_venv` to distinguish it from Windows):
   ```bash
   python3.11 -m venv wsl_venv
   ```

### Activating the Environment
```bash
source wsl_venv/bin/activate
```
*(Verify it worked by running `python --version`, which should now say 3.11.x).*

---

## 3. Installing Dependencies

Once your respective virtual environment is activated (you should see `(venv)` or `(wsl_venv)` in your prompt), install the required project packages:

```bash
pip install kokoro soundfile numpy
```
