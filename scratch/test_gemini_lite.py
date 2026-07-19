import os
from dotenv import load_dotenv
import google.generativeai as genai

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    env_path = os.path.join(base_dir, ".env")
    load_dotenv(dotenv_path=env_path)
    api_key = os.getenv("GEMINI_API_KEY")
    genai.configure(api_key=api_key)
    
    print("Testing gemini-flash-lite-latest...")
    model = genai.GenerativeModel("models/gemini-flash-lite-latest")
    try:
        response = model.generate_content("Hello! Say hi.")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
