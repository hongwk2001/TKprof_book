import os, subprocess, tempfile, json, glob
from multiprocessing import Pool

DIR = r'books\blue_castle\final_audio_ko_ready'
OUT_DIR = r'books\blue_castle\audio_ar_mastered'

def process(src):
    fname = os.path.basename(src)
    dst = os.path.join(OUT_DIR, fname)
    with tempfile.TemporaryDirectory() as tmp:
        p1 = 'loudnorm=I=-16.0:LRA=11:TP=-3.2:print_format=json'
        err_file = os.path.join(tmp, 'err.txt')
        with open(err_file, 'w') as f_err:
            subprocess.run(['ffmpeg','-y','-i',src,'-af',p1,'-f','null','-'], stdout=subprocess.DEVNULL, stderr=f_err)
        
        with open(err_file, 'r') as f_err:
            s = f_err.read()
            
        st = s.rfind('{')
        en = s.rfind('}')+1
        try:
            m = json.loads(s[st:en])
        except Exception as e:
            return
        
        norm = os.path.join(tmp, 'norm.mp3')
        p2 = f"loudnorm=I=-16.0:LRA=11:TP=-3.2:measured_I={m['input_i']}:measured_LRA={m['input_lra']}:measured_TP={m['input_tp']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true"
        subprocess.run(['ffmpeg','-y','-v','error','-i',src,'-af',p2,'-ar','44100','-ac','2','-b:a','256k','-c:a','libmp3lame',norm], check=True)
        
        sil = os.path.join(tmp, 'sil.mp3')
        subprocess.run(['ffmpeg','-y','-v','error','-f','lavfi','-i','anullsrc=channel_layout=stereo:sample_rate=44100','-t','1.0','-b:a','256k','-c:a','libmp3lame',sil], check=True)
        
        list_txt = os.path.join(tmp, 'list.txt')
        with open(list_txt, 'w') as f:
            f.write(f"file '{sil.replace(chr(92), '/')}'\n")
            f.write(f"file '{norm.replace(chr(92), '/')}'\n")
            f.write(f"file '{sil.replace(chr(92), '/')}'\n")
            
        subprocess.run(['ffmpeg','-y','-v','error','-f','concat','-safe','0','-i',list_txt,'-c','copy',dst], check=True)
        print(f"DONE: {fname}")

if __name__ == '__main__':
    mp3s = glob.glob(os.path.join(DIR, '*.mp3'))
    with Pool(8) as p:
        p.map(process, mp3s)
