#!/usr/bin/env bash

# Exit immediately if a command exits with a non-zero status
set -e

# Get the script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo "============================================="
echo "🎧 TKPROF Audiobook Creation Helper (Windows/Git Bash) 🎧"
echo "============================================="

# 1. Check virtual environment
if [ -d "venv" ]; then
    echo "✔ Found Windows virtual environment (venv)."
else
    echo "❌ Windows virtual environment 'venv' not found."
    echo "Creating virtual environment using Python 3.11..."
    python -m venv venv
    echo "✔ Virtual environment created."
fi

# 2. Activate the virtual environment
echo "Activating Windows virtual environment..."
# In Git Bash, we source the bash activator
source venv/Scripts/activate
echo "✔ Activated environment: $(python -c 'import sys; print(sys.prefix)')"

# 3. Check/Install packages
echo "Checking dependencies..."
python -c "
import sys
required = ['kokoro', 'soundfile', 'numpy', 'pydub', 'edge_tts']
missing = []
for package in required:
    try:
        __import__(package if package != 'edge_tts' else 'edge_tts')
    except ImportError:
        missing.append(package)
if missing:
    print('missing:' + ','.join(missing))
else:
    print('all_ok')
" > temp_dep_check.txt

DEP_STATUS=$(cat temp_dep_check.txt)
rm temp_dep_check.txt

if [[ "$DEP_STATUS" == missing:* ]]; then
    MISSING_PKGS=$(echo "$DEP_STATUS" | cut -d':' -f2 | tr ',' ' ')
    echo "Installing missing dependencies: $MISSING_PKGS"
    pip install $MISSING_PKGS
    echo "✔ Dependencies installed successfully."
else
    echo "✔ All dependencies are already installed."
fi

echo ""
echo "Please select a book to generate audio for:"
echo "1) The Enchanted April (English)"
echo "2) The Enchanted April (Korean)"
echo "3) Scaramouche (English/Korean)"
echo "4) Exit"
read -rp "Enter choice [1-4]: " book_choice

case $book_choice in
    1)
        echo "Starting generation for The Enchanted April (English)..."
        python books/the_enchanted_april/generate_audio.py
        ;;
    2)
        echo "Starting generation for The Enchanted April (Korean)..."
        python books/the_enchanted_april/generate_audio_ko.py
        ;;
    3)
        echo "Scaramouche Audiobook Generation:"
        read -rp "Enter language (en/ko): " lang
        read -rp "Enter chapter number (or 'all'): " chap
        
        if [ "$chap" = "all" ]; then
            echo "Generating all chapters for Scaramouche ($lang)..."
            # Loop through available script files
            for f in books/scaramouche/chapters/ch_*_${lang}.json; do
                if [ -f "$f" ]; then
                    # Extract chapter number from ch_XX_lang.json
                    ch_num=$(basename "$f" | cut -d'_' -f2 | sed 's/^0*//')
                    python books/scaramouche/generate_audio.py "$lang" "$ch_num"
                fi
            done
        else
            python books/scaramouche/generate_audio.py "$lang" "$chap"
        fi
        ;;
    *)
        echo "Exiting."
        exit 0
        ;;
esac

echo "============================================="
echo "🎉 Audiobook Generation process completed!"
echo "============================================="
