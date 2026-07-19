import os
import sys
import json
import urllib.request
import urllib.error
import time

API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    with open("d:/git_repo/TKprof_book/.env", "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("GEMINI_API_KEY="):
                API_KEY = line.strip().split("=", 1)[1]
                break

def call_gemini_api(prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.2}
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"}, method="POST")
    
    for attempt in range(8):
        try:
            with urllib.request.urlopen(req, timeout=120) as response:
                res_json = json.loads(response.read().decode("utf-8"))
                candidates = res_json.get("candidates", [])
                if candidates:
                    return candidates[0].get("content", {}).get("parts", [])[0].get("text", "").strip()
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8", errors="ignore")
            if e.code == 429:
                print(f"      [429 Rate Limit] Waiting {10 * (attempt + 1)}s...")
                time.sleep(10 * (attempt + 1))
            else:
                print(f"      [HTTP {e.code}] Retrying... Details: {err_body}")
                time.sleep(5)
        except Exception as e:
            print(f"      [Error] {e}. Retrying in 5s...")
            time.sleep(5)
    print("      [Fatal Error] Could not get response after 8 attempts.")
    return ""

def process_chunk(idx, chunk_text):
    print(f"Chunk {idx}: Starting EN Draft...")
    
    en_draft_prompt = f"""You are an expert editor adapting Rafael Sabatini's "Scaramouche" for modern casual readers and TTS.
Translate/rewrite the following text into clear, engaging, modern English. Do NOT summarize or skip details.
Guidelines:
1. Subject-first word order. No poetic inversions.
2. No dashes or em-dashes.
3. Break down winding sentences into punchy ones.
4. Keep historical terms (Scaramouche, Pantaloon, etc.).
5. No markdown asterisks for emphasis.
6. Keep paragraph separations intact.

Text:
{chunk_text}"""
    en_draft = call_gemini_api(en_draft_prompt)
    if not en_draft: return "", ""
    
    print(f"Chunk {idx}: Starting EN Critique...")
    en_critique_prompt = f"""Critique the following modern English draft against these strict rules:
1. Subject-first word order
2. Clean punctuation (no dashes/hyphens)
3. Linear idea progression
4. No interrupted subjects or parenthetical inserts
Draft:
{en_draft}
Provide a brief list of corrections needed. If none, say 'Perfect'."""
    en_critique = call_gemini_api(en_critique_prompt)
    
    print(f"Chunk {idx}: Starting EN Refine...")
    en_refine_prompt = f"""Refine the following modern English draft based on the critique.
Draft: {en_draft}
Critique: {en_critique}
Output ONLY the final refined modern English text, keeping the exact paragraph separations as the original. No explanations."""
    en_refined = call_gemini_api(en_refine_prompt)

    print(f"Chunk {idx}: Starting KO Draft...")
    ko_draft_prompt = f"""You are translating Scaramouche into elegant, engaging, modern Korean.
Translate the following modern English text into Korean.
Rules:
1. Avoid literal translation (번역투). Use natural flowing Korean.
2. Break down complex sentences. No parentheses for explanations.
3. Names: André-Louis Moreau: 앙드레 루이 모로, Philippe de Vilmorin: 필립 드 빌모랭, Marquis de La Tour d'Azyr: 라 투르 다르지르侯, Aline de Kercadiou: 알린 드 케르카디우, Scaramouche: 스카라무슈, Pantaloon: 판탈룬.
4. Output ONLY the Korean translation. Keep paragraph separations intact.

English Text:
{en_refined}"""
    ko_draft = call_gemini_api(ko_draft_prompt)
    
    print(f"Chunk {idx}: Starting KO Critique...")
    ko_critique_prompt = f"""Critique this Korean translation for:
1. Awkward literal translations (번역투).
2. Proper honorifics and natural literary tone (하십시오체/해라체 mix if appropriate, but maintain standard novel narrative tone).
3. Consistent names.
Translation:
{ko_draft}
Provide a brief list of corrections needed."""
    ko_critique = call_gemini_api(ko_critique_prompt)
    
    print(f"Chunk {idx}: Starting KO Refine...")
    ko_refine_prompt = f"""Refine the Korean translation based on the critique.
Draft: {ko_draft}
Critique: {ko_critique}
Output ONLY the final refined Korean text, keeping exact paragraph separations. No explanations."""
    ko_refined = call_gemini_api(ko_refine_prompt)
    
    print(f"Chunk {idx}: Finished!")
    return en_refined, ko_refined

def main():
    raw_path = r"d:\git_repo\TKprof_book\books\scaramouche\chapters\raw_ch_15.txt"
    en_path = r"d:\git_repo\TKprof_book\books\scaramouche\chapters\ch_15_en.txt"
    ko_path = r"d:\git_repo\TKprof_book\books\scaramouche\chapters\ch_15_ko.txt"
    
    with open(raw_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
    
    chunk_size = 20
    chunks = []
    for i in range(0, len(paragraphs), chunk_size):
        chunks.append('\n\n'.join(paragraphs[i:i+chunk_size]))
        
    print(f"Total chunks: {len(chunks)}")
    
    en_final = []
    ko_final = []
    for i, chunk_text in enumerate(chunks):
        en, ko = process_chunk(i, chunk_text)
        en_final.append(en.strip())
        ko_final.append(ko.strip())
        # Brief pause between chunks to respect rate limit
        time.sleep(2)
        
    with open(en_path, "w", encoding="utf-8") as f:
        f.write('\n\n'.join(en_final))
        
    with open(ko_path, "w", encoding="utf-8") as f:
        f.write('\n\n'.join(ko_final))
        
    print("Workflow complete!")

if __name__ == "__main__":
    # Force unbuffered output
    sys.stdout.reconfigure(line_buffering=True)
    main()
