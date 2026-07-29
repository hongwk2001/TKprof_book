import os
import glob
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
api_key = os.environ.get('GEMINI_API_KEY')
genai.configure(api_key=api_key)

with open('books/seneca_emotional_resilience/prompt_ko.txt', 'r', encoding='utf-8') as f:
    system_instruction = f.read()

system_instruction += "\n\nAdditional Rules:\n1. Make the Korean translation simple, direct, and easy to understand, using the polite 하십시오체.\n2. Add natural inline explanations for Roman cultural terms, historical figures, and complex concepts directly into the prose (avoiding parentheses) to ensure the reader understands immediately.\n3. Keep the flow readable and natural for TTS.\n"

base_dir = "books/seneca_emotional_resilience/chapters/1.on_anger"

model = genai.GenerativeModel('gemini-2.5-pro', system_instruction=system_instruction)

for i in range(23, 44):
    in_file = os.path.join(base_dir, f"on_anger_book3_ch{i:02d}_en_backup.txt")
    out_file = os.path.join(base_dir, f"on_anger_book3_ch{i:02d}_ko.txt")
    
    if os.path.exists(in_file):
        print(f"Translating {in_file}...")
        with open(in_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        try:
            response = model.generate_content(
                content,
                generation_config=genai.types.GenerationConfig(temperature=0.3)
            )
            
            with open(out_file, 'w', encoding='utf-8') as f:
                f.write(response.text.strip())
            print(f"Saved to {out_file}")
        except Exception as e:
            print(f"Failed to translate {in_file}: {e}")
    else:
        print(f"File {in_file} not found.")

print("All translations finished.")
