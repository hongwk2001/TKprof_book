import os
import glob
import re
import time
from dotenv import load_dotenv
import google.generativeai as genai

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

def tag_dialogue_with_gemini(chapter_text, chapter_name):
    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        generation_config={
            "temperature": 0.0,
        },
        system_instruction=(
            "당신은 베오울프 한국어판의 대화를 태깅하는 전문 문학 어시스턴트입니다.\n"
            "각 챕터에서 실제 발화된 대사를 찾아 XML 스타일 화자 태그로 감쌉니다.\n"
            "모든 나레이션 텍스트는 절대 수정하지 않습니다.\n\n"
            "사용 가능한 태그:\n"
            "- <베오울프>...</베오울프>    : 베오울프의 대사\n"
            "- <흐로스가르>...</흐로스가르> : 흐로스가르 왕의 대사\n"
            "- <위글라프>...</위글라프>   : 위글라프의 대사\n"
            "- <기타>...</기타>           : 그 외 모든 화자 (경비병, 전령, 운페르스, 여왕 등)\n\n"
            "규칙:\n"
            "1. 실제 발화된 대사(큰따옴표 내부)만 태그로 감쌉니다.\n"
            "2. 나레이션, 묘사 문장은 절대 수정하지 않습니다.\n"
            "3. 원문의 단 한 글자도 추가/삭제/수정하지 않습니다. 마침표, 쉼표, 공백 모두 그대로 유지합니다.\n"
            "4. 마크다운 블록(예: ```xml) 없이 전체 챕터를 그대로 반환합니다."
        )
    )
    
    prompt = f"다음 챕터의 대화를 태깅해 주세요:\n\n{chapter_text}"
    
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
            cleaned_result = re.sub(r'</?(?:베오울프|흐로스가르|위글라프|기타)>', '', result)
            
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
                if not any(tag in result for tag in ["<베오울프>", "<흐로스가르>", "<위글라프>", "<기타>"]):
                    print(f"[{chapter_name}] Attempt {attempt + 1}: No tags generated. Falling back to original text.")
                    return chapter_text
                
                # Dynamic mapping fallback
                print(f"[{chapter_name}] Attempt {attempt + 1}: Attempting dynamic tag alignment mapping...")
                try:
                    pattern = r'(<(베오울프|흐로스가르|위글라프|기타)>)(.*?)(</\2>)'
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
    input_dir = os.path.join(script_dir, "chapters_kr_v2")
    output_dir = os.path.join(input_dir, "tagged")
    os.makedirs(output_dir, exist_ok=True)
    
    chapter_files = sorted(glob.glob(os.path.join(input_dir, "ch_*_ko.txt")))
    print(f"Found {len(chapter_files)} files to process.")
    
    for file_path in chapter_files:
        file_name = os.path.basename(file_path)
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
        time.sleep(0.5)

if __name__ == "__main__":
    main()
