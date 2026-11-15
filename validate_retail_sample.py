import subprocess, sys, re, os, json

def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True).stderr

def probe(f, keys, stream=True):
    sel = ["-select_streams","a:0","-show_entries",f"stream={keys}"] if stream \
          else ["-show_entries", f"format={keys}"]
    r = subprocess.run(["ffprobe","-v","error",*sel,"-of","default=noprint_wrappers=1",f],
                       capture_output=True, text=True).stdout
    return dict(l.split("=",1) for l in r.strip().splitlines() if "=" in l)

def levels(f, extra=None):
    cmd = ["ffmpeg","-hide_banner"]
    if extra: cmd += extra
    cmd += ["-i",f,"-af","volumedetect","-f","null","-"]
    e = run(cmd)
    mx = re.search(r"max_volume:\s*(-?[\d.]+)", e)
    mn = re.search(r"mean_volume:\s*(-?[\d.]+)", e)
    return (float(mx.group(1)) if mx else None, float(mn.group(1)) if mn else None)

def edge_silence(f, dur, thresh):
    e = run(["ffmpeg","-hide_banner","-i",f,"-af",
             f"silencedetect=noise={thresh}dB:d=0.2","-f","null","-"])
    spans=[]; start=None
    for line in e.splitlines():
        s=re.search(r"silence_start:\s*(-?[\d.]+)",line)
        en=re.search(r"silence_end:\s*([\d.]+)\s*\|\s*silence_duration:\s*([\d.]+)",line)
        if s: start=float(s.group(1))
        if en and start is not None:
            spans.append((start,float(en.group(1)))); start=None
    if start is not None: spans.append((start,dur))
    lead = spans[0][1]-spans[0][0] if spans and spans[0][0]<=0.15 else 0.0
    trail= spans[-1][1]-spans[-1][0] if spans and abs(spans[-1][1]-dur)<=0.25 else 0.0
    return lead, trail

f = sys.argv[1]
st = probe(f,"codec_name,sample_rate,channels,bit_rate")
fm = probe(f,"duration,bit_rate",stream=False)
dur = float(fm["duration"]); br = int(st.get("bit_rate") or fm["bit_rate"])//1000
peak, rms = levels(f)

print(f"FILE: {f}")
print(f"  codec={st['codec_name']}  {st['sample_rate']}Hz  {st['channels']}ch  {br}kbps  {dur:.2f}s ({dur/60:.2f} min)")
print(f"  peak={peak} dB   rms={rms} dB\n")

checks=[]
checks.append(("RMS between -23 and -18 dB", rms is not None and -23.0<=rms<=-18.0, f"{rms} dB"))
checks.append(("Peak <= -1.0 dB (AR message)", peak is not None and peak<=-1.0, f"{peak} dB"))
checks.append(("Peak <= -3.0 dB (ACX stricter)", peak is not None and peak<=-3.0, f"{peak} dB"))
checks.append(("Sample rate == 44100", st['sample_rate']=="44100", st['sample_rate']))
checks.append(("Bitrate >= 192 kbps", br>=192, f"{br} kbps"))
checks.append(("Duration 1-5 min (retail sample)", 60<=dur<=300, f"{dur/60:.2f} min"))

for th in (-40,-50,-60,-70):
    lead,trail = edge_silence(f,dur,th)
    checks.append((f"Leading silence 1-5s @ {th}dB", 1.0<=lead<=5.0, f"{lead:.2f}s"))
    checks.append((f"Trailing silence 1-5s @ {th}dB", 1.0<=trail<=5.0, f"{trail:.2f}s"))

# is the padding digital zero?
_, tail_mean = levels(f, ["-sseof","-1.0"])
_, head_mean = levels(f, ["-t","1.0"])
digital_zero = (tail_mean is not None and tail_mean <= -90.0)
checks.append(("Pad carries room tone (not digital zero)", not digital_zero,
               f"head {head_mean} dB / tail {tail_mean} dB"))

bad=0
for name,ok,val in checks:
    print(f"  [{'PASS' if ok else 'FAIL'}] {name:42} {val}")
    if not ok: bad+=1
print(f"\n  => {len(checks)-bad}/{len(checks)} checks passed")
sys.exit(1 if bad else 0)
