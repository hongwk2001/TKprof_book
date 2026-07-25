#!/bin/bash
# Rebuild the 8 affected audiobook tracks that had quote-placement corrections.
# Run this inside the WSL terminal with the python environment activated.

set -e

# 1. Activate venv if not already done (optional reminder)
if [ -z "$VIRTUAL_ENV" ]; then
    if [ -f "venv/Scripts/activate" ]; then
        echo "Activating virtual environment..."
        source venv/Scripts/activate
    else
        echo "WARNING: Virtual environment not active. Please activate venv first."
    fi
fi

echo "=========================================================="
echo "Step 1: Deleting existing audio files for affected tracks..."
echo "=========================================================="
# English files
rm -f books/secret_garden/final_audio/final_track_21.mp3
rm -f books/secret_garden/final_audio/final_track_25.mp3

# Korean files
rm -f books/secret_garden/final_audio_ko/final_track_18.mp3
rm -f books/secret_garden/final_audio_ko/final_track_21.mp3
rm -f books/secret_garden/final_audio_ko/final_track_22.mp3
rm -f books/secret_garden/final_audio_ko/final_track_23.mp3
rm -f books/secret_garden/final_audio_ko/final_track_25.mp3
rm -f books/secret_garden/final_audio_ko/final_track_27.mp3

echo "=========================================================="
echo "Step 2: Regenerating English audiobook tracks..."
echo "=========================================================="
python books/secret_garden/generate_audio.py 20
python books/secret_garden/generate_audio.py 24

echo "=========================================================="
echo "Step 3: Regenerating Korean audiobook tracks..."
echo "=========================================================="
python books/secret_garden/generate_audio_ko.py 17
python books/secret_garden/generate_audio_ko.py 20
python books/secret_garden/generate_audio_ko.py 21
python books/secret_garden/generate_audio_ko.py 22
python books/secret_garden/generate_audio_ko.py 24
python books/secret_garden/generate_audio_ko.py 26

echo "=========================================================="
echo "Step 4: Post-processing and normalizing quality..."
echo "=========================================================="
python fix_audio_quality.py books/secret_garden/final_audio/ --overwrite
python fix_audio_quality.py books/secret_garden/final_audio_ko/ --overwrite

echo "=========================================================="
echo "Step 5: Verifying quality of all tracks..."
echo "=========================================================="
python check_audio_quality.py books/secret_garden/final_audio/
python check_audio_quality.py books/secret_garden/final_audio_ko/

echo "=========================================================="
echo "SUCCESS: Rebuild and validation complete!"
echo "=========================================================="
