import os, glob, soundfile as sf
folder = '/mnt/d/git_repo/TKprof_book/books/gilgamesh/audio_archive'
if not os.path.exists(folder):
    folder = '/mnt/d/git_repo/TKprof_book/books/gilgamesh/audio'
files = glob.glob(os.path.join(folder, '*_en*.mp3'))
valid_files = [f for f in files if 'ch_' in os.path.basename(f) or 'introduction' in os.path.basename(f) or 'copyright' in os.path.basename(f)]
total_seconds = 0
for f in valid_files:
    if 'bak' in f: continue
    try:
        f_info = sf.info(f)
        total_seconds += f_info.duration
    except Exception as e:
        pass

hours = int(total_seconds // 3600)
minutes = int((total_seconds % 3600) // 60)
seconds = int(total_seconds % 60)
print(f'Total Duration: {hours:02d}:{minutes:02d}:{seconds:02d}')
