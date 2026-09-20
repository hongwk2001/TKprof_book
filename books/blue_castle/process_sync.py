import os, subprocess, tempfile, json, glob

DIR = r'books\blue_castle\final_audio_ko_ready'
OUT_DIR = r'books\blue_castle\audio_ar_mastered'

if not os.path.exists(OUT_DIR):
    os.makedirs(OUT_DIR)

mp3s = glob.glob(os.path.join(DIR, '*.mp3'))

for i, src in enumerate(mp3s):
    fname = os.path.basename(src)
    dst = os.path.join(OUT_DIR, fname)
    if os.path.exists(dst): 
        print(f"Skipping {fname}...")
        continue
        
    print(f"[{i+1}/{len(mp3s)}] Processing {fname}...", flush=True)
    with tempfile.TemporaryDirectory() as tmp:
        p1 = 'loudnorm=I=-20.0:LRA=11:TP=-3.2:print_format=json'
        r1 = subprocess.run(['ffmpeg','-y','-v','error','-i',src,'-af',p1,'-f','null','-'], capture_output=True, text=True)
        s = r1.stderr
        st = s.rfind('{')
        en = s.rfind('}')+1
        try:
            m = json.loads(s[st:en])
        except Exception as e:
            print(f"Error parsing JSON for {fname}: {e}")
            continue
        
        norm = os.path.join(tmp, 'norm.mp3')
        p2 = f"loudnorm=I=-20.0:LRA=11:TP=-3.2:measured_I={m['input_i']}:measured_LRA={m['input_lra']}:measured_TP={m['input_tp']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true"
        subprocess.run(['ffmpeg','-y','-v','error','-i',src,'-af',p2,'-ar','44100','-ac','2','-b:a','256k','-c:a','libmp3lame',norm], check=True)
        
        sil = os.path.join(tmp, 'sil.mp3')
        subprocess.run(['ffmpeg','-y','-v','error','-f','lavfi','-i','anullsrc=channel_layout=stereo:sample_rate=44100','-t','3.0','-b:a','256k','-c:a','libmp3lame',sil], check=True)
        
        list_txt = os.path.join(tmp, 'list.txt')
        with open(list_txt, 'w') as f:
            f.write(f"file '{sil.replace(chr(92), '/')}'\n")
            f.write(f"file '{norm.replace(chr(92), '/')}'\n")
            f.write(f"file '{sil.replace(chr(92), '/')}'\n")
            
        subprocess.run(['ffmpeg','-y','-v','error','-f','concat','-safe','0','-i',list_txt,'-c','copy',dst], check=True)

print("ALL DONE")
