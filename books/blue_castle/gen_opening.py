import os, sys, json, asyncio, edge_tts
from pydub import AudioSegment

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_FILE = os.path.join(SCRIPT_DIR, "audio_ar_mastered", "00_ar_opening.mp3")

async def generate():
    voice = "ko-KR-SunHiNeural"
    text = "블루 캐슬. 루시 모드 몽고메리 지음."
    communicate = edge_tts.Communicate(text, voice, rate="+0%")
    temp_mp3 = os.path.join(SCRIPT_DIR, "temp_opening.mp3")
    await communicate.save(temp_mp3)
    return temp_mp3

def master(src, dst):
    import subprocess
    p1 = 'loudnorm=I=-16.0:LRA=11:TP=-3.2:print_format=json'
    
    # Run pass 1 without -v error to safely capture json
    err_file = os.path.join(SCRIPT_DIR, 'err.txt')
    with open(err_file, 'w') as f_err:
        subprocess.run(['ffmpeg','-y','-i',src,'-af',p1,'-f','null','-'], stdout=subprocess.DEVNULL, stderr=f_err)
    
    with open(err_file, 'r') as f_err:
        s = f_err.read()
    
    m = json.loads(s[s.rfind('{'):s.rfind('}')+1])
    
    p2 = f"loudnorm=I=-16.0:LRA=11:TP=-3.2:measured_I={m['input_i']}:measured_LRA={m['input_lra']}:measured_TP={m['input_tp']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true"
    norm = os.path.join(SCRIPT_DIR, 'norm_opening.mp3')
    subprocess.run(['ffmpeg','-y','-v','error','-i',src,'-af',p2,'-ar','44100','-ac','2','-b:a','256k','-c:a','libmp3lame',norm], check=True)
    
    sil = os.path.join(SCRIPT_DIR, 'sil_opening.mp3')
    subprocess.run(['ffmpeg','-y','-v','error','-f','lavfi','-i','anullsrc=channel_layout=stereo:sample_rate=44100','-t','1.0','-b:a','256k','-c:a','libmp3lame',sil], check=True)
    
    list_txt = os.path.join(SCRIPT_DIR, 'list_opening.txt')
    with open(list_txt, 'w') as f:
        f.write(f"file '{sil.replace(chr(92), '/')}'\n")
        f.write(f"file '{norm.replace(chr(92), '/')}'\n")
        f.write(f"file '{sil.replace(chr(92), '/')}'\n")
        
    subprocess.run(['ffmpeg','-y','-v','error','-f','concat','-safe','0','-i',list_txt,'-c','copy',dst], check=True)
    
    os.remove(norm)
    os.remove(sil)
    os.remove(list_txt)
    os.remove(src)
    os.remove(err_file)

if __name__ == '__main__':
    temp_mp3 = asyncio.run(generate())
    master(temp_mp3, OUT_FILE)
    print("Created 00_ar_opening.mp3 successfully!")
