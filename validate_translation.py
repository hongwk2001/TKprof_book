import os
import sys
import re

# Force UTF-8 stdout to prevent Windows encoding errors
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

class TranslationValidator:
    def __init__(self):
        # Hangul, numbers, spaces, and allowed punctuation
        self.allowed_pattern = re.compile(
            r'[^\uac00-\ud7a3\u1100-\u11ff\u3130-\u318f'  # Hangul
            r'0-9'                                        # Numbers
            r'\s'                                         # Whitespace
            r'.,\'\"?!~:;·\-–—‘’“”()\[\]{}<>「」『』\\/&+=%*…\u2026]' # Allowed punctuation/symbols including ellipses
        )
        
        # Pattern to detect English word blocks (3 or more consecutive English words)
        self.english_block_pattern = re.compile(r'\b[A-Za-z]+\b(?:\s+\b[A-Za-z]+\b){2,}')
        
        # Parenthesized text that is a common TTS issue (e.g. (Hindustani) or (약 8킬로미터))
        self.tts_parentheses_pattern = re.compile(r'\([^)]+\)')
        
        # Honorific mismatch triggers (fathers/mothers/parents calling their children 도련님 or 아가씨)
        # We search for combinations of family terms and honorifics on the same line
        self.honorific_mismatch_keywords = [
            (re.compile(r'(?:아버|어머|아빠|엄마|부모).*(?:도련님|아가씨)'), "Family term paired with servant-style honorific (도련님/아가씨)"),
            (re.compile(r'(?:도련님|아가씨).*(?:아버|어머|아빠|엄마|부모)'), "Family term paired with servant-style honorific (도련님/아가씨)")
        ]

    def validate_file(self, filepath):
        print(f"\nAuditing file: {os.path.basename(filepath)}")
        print("=" * 60)
        
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()
            
        if not lines:
            print("  [ERROR] File is empty.")
            return False
            
        errors_found = 0
        
        # 1. Check Chapter Header
        first_line = lines[0].strip()
        if not (first_line.startswith("제") and "장" in first_line):
            print(f"  [HEADER WARNING] First line does not seem to be a valid Korean chapter header.")
            print(f"    Line 1: '{first_line}'")
            errors_found += 1
            
        for idx, line in enumerate(lines, 1):
            cleaned_line = line.strip()
            if not cleaned_line:
                continue
                
            # 2. Check Untranslated English Blocks
            eng_blocks = self.english_block_pattern.findall(cleaned_line)
            if eng_blocks:
                print(f"  [UNTRANSLATED WARNING] Line {idx}: Found consecutive English word block(s): {eng_blocks}")
                print(f"    Content: {cleaned_line}")
                errors_found += 1
                
            # 3. Check Foreign / Unexpected Characters
            non_std_chars = self.allowed_pattern.findall(line)
            if non_std_chars:
                # Filter out standard English words if they were already flagged
                unique_chars = list(set(non_std_chars))
                # Let's filter out standard alphabetic characters if they belong to a flagged English word
                # to avoid duplicate logging, but keep Hanja, Thai, etc.
                foreign_chars = [c for c in unique_chars if not c.isalpha()]
                if foreign_chars:
                    print(f"  [FOREIGN CHAR WARNING] Line {idx}: Found unexpected non-Korean characters: {foreign_chars}")
                    print(f"    Content: {cleaned_line}")
                    errors_found += 1
                    
            # 4. Check TTS Compatibility (Parentheses)
            parens = self.tts_parentheses_pattern.findall(cleaned_line)
            if parens:
                print(f"  [TTS WARNING] Line {idx}: Found parentheses containing text (breaks audio flow): {parens}")
                print(f"    Content: {cleaned_line}")
                errors_found += 1
                
            # 5. Check Honorific Mismatch (호칭)
            for pattern, desc in self.honorific_mismatch_keywords:
                if pattern.search(cleaned_line):
                    # We exclude descriptive or servant speech context if Mrs. Medlock is the one speaking
                    # but if it's the narrator or the father, it's flagged.
                    # This is a heuristic check to highlight lines to double-check.
                    print(f"  [HONORIFIC WARNING] Line {idx}: Potential mismatch ({desc})")
                    print(f"    Content: {cleaned_line}")
                    errors_found += 1
                    break
                    
        if errors_found == 0:
            print("  [SUCCESS] No translation or formatting issues found. File is clean!")
            return True
        else:
            print(f"  [AUDIT COMPLETE] Found {errors_found} potential issues in this file.")
            return False

def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_translation.py <path_to_file_or_directory>")
        sys.exit(1)
        
    target_path = sys.argv[1]
    validator = TranslationValidator()
    
    if os.path.isdir(target_path):
        # Audit all txt files in directory
        txt_files = [os.path.join(target_path, f) for f in os.listdir(target_path) if f.endswith("_ko.txt")]
        txt_files.sort()
        
        if not txt_files:
            print(f"No Korean translation files (*_ko.txt) found in {target_path}")
            sys.exit(1)
            
        success_count = 0
        for filepath in txt_files:
            if validator.validate_file(filepath):
                success_count += 1
                
        print("\n" + "=" * 60)
        print(f"Folder Audit Summary: {success_count}/{len(txt_files)} files passed validation.")
    elif os.path.isfile(target_path):
        validator.validate_file(target_path)
    else:
        print(f"Error: Target path {target_path} does not exist.")
        sys.exit(1)

if __name__ == "__main__":
    main()
