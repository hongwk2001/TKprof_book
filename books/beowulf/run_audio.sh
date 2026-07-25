#!/bin/bash
export CUDA_VISIBLE_DEVICES=""
source venv/Scripts/activate
python -u books/beowulf/generate_audio.py "$@"
