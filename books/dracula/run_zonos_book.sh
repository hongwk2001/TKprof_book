#!/bin/bash
# Render the whole Dracula English audiobook with Zonos, start to finish.
#
# Resumable. A chapter whose mp3 already exists is skipped, and every sentence
# is cached, so an interrupted run only loses the chapter it was inside.
# Safe to re-run as many times as needed -- it picks up where it stopped.
#
#   wsl -d Ubuntu -- bash /mnt/c/git_repo/TKprof_book/books/dracula/run_zonos_book.sh
#
# Watch progress from Windows:
#   tail -f /c/git_repo/TKprof_book/books/dracula/zonos_build.log
set -u

export PATH=/root/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
WINDIR=/mnt/c/git_repo/TKprof_book/books/dracula
DEST="$WINDIR/final_audio_en_zonos"
LOG="$WINDIR/zonos_build.log"

mkdir -p "$DEST"
cd /root/Zonos || exit 1
cp "$WINDIR/make_english_audiobook_zonos.py" ./ || exit 1

{
  echo "=========================================================="
  echo "Zonos book render started $(date)"
  echo "=========================================================="
} >> "$LOG"

# Strip the per-token tqdm bars; keep everything that matters.
# --line-buffered so the log updates as it goes; without it grep block-buffers
# and nothing appears until the whole run ends.
uv run python make_english_audiobook_zonos.py all 2>&1 \
  | grep --line-buffered -aE "^  ch[0-9]|\[done\]|\[skip\]|\[warn\]|\[ERROR\]|\[progress\]|\[ALL DONE\]|\[oom\]|\[vram|\[[0-9]+/|retry|resynth|Error|Traceback" \
  | tee -a "$LOG"

# Copy everything produced back to the Windows side.
cp /root/zonos_build/*.mp3 "$DEST/" 2>/dev/null
echo "copied $(ls -1 /root/zonos_build/*.mp3 2>/dev/null | wc -l) files to $DEST" | tee -a "$LOG"
echo "Finished $(date)" >> "$LOG"
