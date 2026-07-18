import json

def format_review():
    with open("scratch/guessed_quotes.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        
    with open("scratch/review_quotes.txt", "w", encoding="utf-8") as out:
        for ch, quotes in data.items():
            out.write(f"==================== {ch.upper()} ====================\n")
            for q in quotes:
                out.write(f"Index: {q['index']}\n")
                out.write(f"Guess: {q['guessed']}\n")
                out.write(f"Context: {q['context_preview']}\n")
                out.write(f"Quote: {q['quote']}\n")
                out.write("-" * 40 + "\n")

if __name__ == "__main__":
    format_review()
