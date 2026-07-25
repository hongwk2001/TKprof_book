import os
import glob
import re
import time
import difflib
from dotenv import load_dotenv
import google.genai as genai

def load_api_key():
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

def clean_text(text):
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'\s+', '', text)
    text = re.sub(r'[^\w]', '', text)
    return text.lower()

def align_tags_with_difflib(original, tagged_output):
    tag_pattern = re.compile(r'<(odysseus|telemachus|others)>(.*?)</\1>', re.DOTALL)
    stripped_text = ""
    tagged_ranges = []
    
    last_idx = 0
    for match in tag_pattern.finditer(tagged_output):
        start, end = match.span()
        stripped_text += tagged_output[last_idx:start]
        
        tag_name = match.group(1)
        content = match.group(2)
        
        tag_start_in_stripped = len(stripped_text)
        stripped_text += content
        tag_end_in_stripped = len(stripped_text)
        
        tagged_ranges.append((tag_start_in_stripped, tag_end_in_stripped, tag_name))
        last_idx = end
        
    stripped_text += tagged_output[last_idx:]
    
    matcher = difflib.SequenceMatcher(None, stripped_text, original)
    matching_blocks = matcher.get_matching_blocks()
    
    index_map = {}
    for block in matching_blocks:
        a_start, b_start, size = block
        for offset in range(size):
            index_map[a_start + offset] = b_start + offset
            
    original_replacements = []
    for start, end, tag_name in tagged_ranges:
        mapped_indices = [index_map[i] for i in range(start, end) if i in index_map]
        if not mapped_indices:
            continue
        orig_start = min(mapped_indices)
        orig_end = max(mapped_indices) + 1
        original_replacements.append((orig_start, orig_end, tag_name))
        
    original_replacements.sort(key=lambda x: x[0], reverse=True)
    reconstructed = original
    for orig_start, orig_end, tag_name in original_replacements:
        reconstructed = (
            reconstructed[:orig_start] +
            f"<{tag_name}>{reconstructed[orig_start:orig_end]}</{tag_name}>" +
            reconstructed[orig_end:]
        )
        
    return reconstructed

def tag_dialogue_with_gemini(chapter_text, chapter_name):
    model_name = "gemini-2.5-flash"
    
    system_instruction = (
        "You are an expert literary assistant specializing in tagging dialogue. "
        "Your task is to read the provided chapter of The Odyssey in Korean, identify all spoken dialogue, and wrap the spoken text in XML-style speaker tags, WHILE KEEPING all non-spoken narration text exactly as is. "
        "Available speaker tags:\n"
        "- <odysseus>...</odysseus> for Odysseus (오디세우스)\n"
        "- <telemachus>...</telemachus> for Telemachus (텔레마코스)\n"
        "- <others>...</others> for any other speakers (e.g. Penelope/페넬로페, Athena/아테나, suitors/구혼자들, Eumaeus/에우마이오스, Nestor, Calypso, Circe, etc.)\n\n"
        "CRITICAL RULES:\n"
        "1. ONLY wrap the actual spoken dialogue (usually inside Korean double quotation marks “...” or \"...\") in the tags. Keep all narration and non-spoken text completely intact and unchanged. Do NOT omit any narrative paragraphs or sentences.\n"
        "2. Keep the quotation marks inside or outside the speaker tags as they are, but make sure the exact spoken words are wrapped.\n"
        "3. DO NOT modify, translate, paraphrase, omit, or add a single character, word, punctuation, spacing, or paragraph from the original chapter text. The final output must be identical to the input chapter, word-for-word, character-for-character, with only the opening and closing speaker tags added around the spoken dialogue.\n"
        "4. Return the entire chapter with the speaker tags. Do not include any summary, introductory remarks, or markdown block formatting (do NOT wrap the output in ``` or ```xml)."
    )
    
    prompt = f"Please tag the dialogue in the following Korean chapter:\n\n{chapter_text}"
    
    print(f"[{chapter_name}] Tagging with model: {model_name}")
    model = genai.GenerativeModel(
        model_name=model_name,
        generation_config={"temperature": 0.0},
        system_instruction=system_instruction
    )
    
    attempt = 0
    quota_retries = 0
    
    while attempt < 5:
        try:
            response = model.generate_content(prompt)
            result = response.text.strip()
            
            if result.startswith("```"):
                lines = result.splitlines()
                if lines[0].startswith("```"):
                    lines = lines[1:]
                if lines and lines[-1].startswith("```"):
                    lines = lines[:-1]
                result = "\n".join(lines).strip()
            
            cleaned_result = re.sub(r'</?(?:odysseus|telemachus|others)>', '', result)
            
            orig_normalized = "".join(chapter_text.split())
            cleaned_normalized = "".join(result.split())
            cleaned_normalized = re.sub(r'</?(?:odysseus|telemachus|others)>', '', cleaned_normalized)
            
            if orig_normalized == cleaned_normalized:
                return result
            else:
                if not any(tag in result for tag in ["<odysseus>", "<telemachus>", "<others>"]):
                    print(f"[{chapter_name}] Attempt {attempt + 1}: No tags generated. Falling back to original text.")
                    return chapter_text
                
                print(f"[{chapter_name}] Attempt {attempt + 1}: Attempting difflib sequence tag alignment...")
                try:
                    reconstructed = align_tags_with_difflib(chapter_text, result)
                    cleaned = re.sub(r'</?(?:odysseus|telemachus|others)>', '', reconstructed)
                    
                    orig_no_ws = "".join(chapter_text.split())
                    cleaned_no_ws = "".join(cleaned.split())
                    
                    if orig_no_ws == cleaned_no_ws:
                        print(f"[{chapter_name}] difflib sequence alignment succeeded!")
                        return reconstructed
                except Exception as map_err:
                    print(f"[{chapter_name}] difflib sequence alignment failed: {map_err}")
                
                print(f"[{chapter_name}] Attempt {attempt + 1}: Content mismatch! Original len: {len(orig_normalized)}, Cleaned len: {len(cleaned_normalized)}")
                attempt += 1
                time.sleep(2)
        except Exception as e:
            err_str = str(e)
            if "Quota exceeded" in err_str or "429" in err_str or "RESOURCE_EXHAUSTED" in err_str:
                quota_retries += 1
                if quota_retries > 10:
                    raise RuntimeError(f"Rate limits hit 10 times consecutively on {chapter_name}. Exiting.")
                print(f"[{chapter_name}] Quota exceeded (consecutive={quota_retries}), sleeping 65s for window reset...")
                time.sleep(65)
            else:
                print(f"[{chapter_name}] Attempt {attempt + 1} failed: {e}. Retrying...")
                attempt += 1
                time.sleep(3)
                
    raise RuntimeError(f"Failed to process {chapter_name} due to quota/errors after retries.")

def main():
    import sys
    setup_gemini()
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_dir = os.path.join(script_dir, "chapters")
    output_dir = os.path.join(input_dir, "tagged")
    os.makedirs(output_dir, exist_ok=True)
    
    if len(sys.argv) > 1:
        ch_num = sys.argv[1].zfill(2)
        chapter_files = glob.glob(os.path.join(input_dir, f"ch_{ch_num}_ko.txt"))
    else:
        chapter_files = sorted(glob.glob(os.path.join(input_dir, "ch_*_ko.txt")))
    
    print(f"Found {len(chapter_files)} files to process.")
    
    for file_path in chapter_files:
        file_name = os.path.basename(file_path)
        out_file_name = f"tagged_{file_name}"
        out_file_path = os.path.join(output_dir, out_file_name)
        
        # Load source text
        with open(file_path, "r", encoding="utf-8") as f:
            chapter_text = f.read()
            
        # Check if already tagged and valid
        if os.path.exists(out_file_path):
            with open(out_file_path, "r", encoding="utf-8") as f_tagged:
                existing_tagged = f_tagged.read()
            if clean_text(chapter_text) == clean_text(existing_tagged):
                print(f"Skipping {file_name} (already tagged and matches source exactly)")
                continue
        
        print(f"Processing {file_name} -> {out_file_name}...")
        tagged_text = tag_dialogue_with_gemini(chapter_text, file_name)
        
        with open(out_file_path, "w", encoding="utf-8") as f:
            f.write(tagged_text)
            
        print(f"Saved {out_file_name}")
        time.sleep(2.0)

if __name__ == "__main__":
    main()
