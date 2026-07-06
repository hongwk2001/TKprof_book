#!/bin/bash
export CUDA_VISIBLE_DEVICES=""
source wsl_venv/bin/activate
python3 -u books/beowulf/generate_audio.py "$@"
