import os
import glob
import re
import time
from dotenv import load_dotenv
import google.generativeai as genai

def load_api_key():
    # Load environment variables from .env file (handle both Windows and Linux paths)
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    env_path = os.path.join(base_dir, ".env")
    load_dotenv(dotenv_path=env_path)
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError(f"GEMINI_API_KEY not found in {env_path}")
    return api_key

def setup_gemini():
    api_key = load_api_key()
    genai.configure(api_key=api_key)

def tag_dialogue_with_gemini(chapter_text, chapter_name):
    # We will use gemini-2.5-flash for speed and reliability.
    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        generation_config={
            "temperature": 0.0,
        },
        system_instruction=(
            "You are an expert literary assistant specializing in tagging dialogue. "
            "Your task is to read the provided chapter of Beowulf, identify all spoken dialogue, and wrap the spoken text in XML-style speaker tags, WHILE KEEPING all non-spoken narration text exactly as is. "
            "Available speaker tags:\n"
            "- <beowulf>...</beowulf> for Beowulf\n"
            "- <hrothgar>...</hrothgar> for Hrothgar\n"
            "- <unferth>...</unferth> for Unferth\n"
            "- <wealhtheow>...</wealhtheow> for Wealhtheow\n"
            "- <wiglaf>...</wiglaf> for Wiglaf\n"
            "- <rest>...</rest> for any other speakers (e.g. guard, herald, Wulfgar, coast-guard, Grendel's mother, messenger, etc.)\n\n"
            "CRITICAL RULES:\n"
            "1. ONLY wrap the actual spoken dialogue (usually inside quotation marks) in the tags. Keep all narration and non-spoken text completely intact and unchanged. Do NOT omit any narrative paragraphs or sentences.\n"
            "2. Keep the quotation marks inside or outside the speaker tags as they are, but make sure the exact spoken words are wrapped.\n"
            "3. DO NOT modify, omit, or add a single character, word, punctuation, spacing, or paragraph from the original chapter text. The final output must be identical to the input chapter, word-for-word, character-for-character, with only the opening and closing speaker tags added around the spoken dialogue.\n"
            "4. Return the entire chapter with the speaker tags. Do not include any summary, introductory remarks, or markdown block formatting (do NOT wrap the output in ``` or ```xml)."
        )
    )
    
    prompt = f"Please tag the dialogue in the following chapter:\n\n{chapter_text}"
    
    # Try with retry logic in case of rate limits or transient errors
    for attempt in range(5):
        try:
            response = model.generate_content(prompt)
            result = response.text.strip()
            
            # Clean up potential markdown formatting
            if result.startswith("```"):
                lines = result.splitlines()
                if lines[0].startswith("```"):
                    lines = lines[1:]
                if lines and lines[-1].startswith("```"):
                    lines = lines[:-1]
                result = "\n".join(lines).strip()
            
            # Remove all valid speaker tags to check if the remaining text matches the original
            cleaned_result = re.sub(r'</?(?:beowulf|hrothgar|unferth|wealhtheow|wiglaf|rest)>', '', result)
            
            # Compare normalized whitespace versions
            orig_normalized = " ".join(chapter_text.split())
            cleaned_normalized = " ".join(cleaned_result.split())
            
            if orig_normalized == cleaned_normalized:
                return result
            else:
                # Check if they have the exact same non-whitespace characters
                orig_no_ws = "".join(chapter_text.split())
                cleaned_no_ws = "".join(cleaned_result.split())
                if orig_no_ws == cleaned_no_ws:
                    print(f"[{chapter_name}] Attempt {attempt + 1}: Whitespace difference only. Proceeding.")
                    return result
                
                # Check if the model simply returned the text without tagging any dialogue (perhaps none exists)
                if not any(tag in result for tag in ["<beowulf>", "<hrothgar>", "<unferth>", "<wealhtheow>", "<wiglaf>", "<rest>"]):
                    print(f"[{chapter_name}] Attempt {attempt + 1}: No tags generated. Falling back to original text.")
                    return chapter_text
                
                # Dynamic mapping fallback
                print(f"[{chapter_name}] Attempt {attempt + 1}: Attempting dynamic tag alignment mapping...")
                try:
                    pattern = r'(<(beowulf|hrothgar|unferth|wealhtheow|wiglaf|rest)>)(.*?)(</\2>)'
                    matches = list(re.finditer(pattern, result, re.DOTALL))
                    if matches:
                        current_text = chapter_text
                        success_all = True
                        replacements = []
                        for m in matches:
                            tag_open = m.group(1)
                            tag_name = m.group(2)
                            tagged_content = m.group(3)
                            tag_close = m.group(4)
                            
                            content_words = tagged_content.strip().split()
                            if not content_words:
                                continue
                            
                            content_regex = r"\s*".join(re.escape(w) for w in content_words)
                            content_regex = content_regex.replace(r'\"', r'["“”]')
                            content_regex = content_regex.replace(r'\'', r'[\'’]')
                            content_regex = content_regex.replace(r'\-', r'[—\-–]')
                            
                            orig_match = list(re.finditer(content_regex, current_text))
                            if len(orig_match) == 1:
                                start, end = orig_match[0].span()
                                replacements.append((start, end, f"{tag_open}{orig_match[0].group(0)}{tag_close}"))
                            else:
                                success_all = False
                                break
                                
                        if success_all and replacements:
                            replacements.sort(key=lambda x: x[0], reverse=True)
                            for start, end, rep_str in replacements:
                                current_text = current_text[:start] + rep_str + current_text[end:]
                            print(f"[{chapter_name}] Dynamic alignment succeeded!")
                            return current_text
                except Exception as map_err:
                    print(f"[{chapter_name}] Dynamic alignment failed: {map_err}")
                
                print(f"[{chapter_name}] Attempt {attempt + 1}: Content mismatch! Original len: {len(orig_normalized)}, Cleaned len: {len(cleaned_normalized)}")
                time.sleep(2)
        except Exception as e:
            # Handle rate limit / quota exceeded
            if "Quota exceeded" in str(e) or "429" in str(e):
                print(f"[{chapter_name}] Quota exceeded, sleeping 30s...")
                time.sleep(30)
            else:
                print(f"[{chapter_name}] Attempt {attempt + 1} failed: {e}. Retrying...")
                time.sleep(3)
            
    raise RuntimeError(f"Failed to process {chapter_name} after 5 attempts.")

def main():
    setup_gemini()
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_dir = os.path.join(script_dir, "chapters_en_v2")
    output_dir = os.path.join(input_dir, "tagged")
    os.makedirs(output_dir, exist_ok=True)
    
    # Get all chapters ch_00_en.txt to ch_43_en.txt
    chapter_files = sorted(glob.glob(os.path.join(input_dir, "ch_*_en.txt")))
    
    print(f"Found {len(chapter_files)} files to process.")
    
    for file_path in chapter_files:
        file_name = os.path.basename(file_path)
        # e.g., ch_00_en.txt -> tagged_ch_00_en.txt
        out_file_name = f"tagged_{file_name}"
        out_file_path = os.path.join(output_dir, out_file_name)
        
        if os.path.exists(out_file_path):
            print(f"Skipping {file_name} (already tagged)")
            continue
            
        print(f"Processing {file_name} -> {out_file_name}...")
        
        with open(file_path, "r", encoding="utf-8") as f:
            chapter_text = f.read()
            
        tagged_text = tag_dialogue_with_gemini(chapter_text, file_name)
        
        with open(out_file_path, "w", encoding="utf-8") as f:
            f.write(tagged_text)
            
        print(f"Saved {out_file_name}")
        # Be nice to API rate limits (Paid key has high limits, 0.5s is safe)
        time.sleep(0.5)

if __name__ == "__main__":
    main()
