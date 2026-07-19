import os
from dotenv import load_dotenv
import google.generativeai as genai

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    env_path = os.path.join(base_dir, ".env")
    load_dotenv(dotenv_path=env_path)
    api_key = os.getenv("GEMINI_API_KEY")
    genai.configure(api_key=api_key)
    
    print("Listing models:")
    for m in genai.list_models():
        print(f"Name: {m.name}, Supported operations: {m.supported_generation_methods}")

if __name__ == "__main__":
    main()
