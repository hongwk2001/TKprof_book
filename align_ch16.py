import json
import re

def split_korean(korean_text, english_chunks):
    sentences = re.split(r'(?<=[.!?])\s+', korean_text)
    if len(sentences) == 1 and not sentences[0]:
        sentences = []
    
    eng_lengths = [len(chunk) for chunk in english_chunks]
    total_eng = sum(eng_lengths)
    if total_eng == 0:
        ratios = [1.0 / len(english_chunks)] * len(english_chunks)
    else:
        ratios = [l / total_eng for l in eng_lengths]
    
    kor_length = len(korean_text)
    target_lengths = [int(r * kor_length) for r in ratios]
    
    kor_chunks = []
    current_chunk = []
    current_length = 0
    chunk_index = 0
    
    for i, sentence in enumerate(sentences):
        if chunk_index == len(target_lengths) - 1:
            current_chunk.append(sentence)
            continue
            
        sentence_len = len(sentence)
        if current_length + sentence_len > target_lengths[chunk_index] and current_length > 0:
            kor_chunks.append(" ".join(current_chunk))
            chunk_index += 1
            current_chunk = [sentence]
            current_length = sentence_len
        else:
            current_chunk.append(sentence)
            current_length += sentence_len + 1
            
    kor_chunks.append(" ".join(current_chunk))
    
    while len(kor_chunks) < len(english_chunks):
        kor_chunks.append("")
        
    if len(kor_chunks) > len(english_chunks):
        extra = kor_chunks[len(english_chunks)-1:]
        kor_chunks = kor_chunks[:len(english_chunks)-1]
        kor_chunks.append(" ".join(extra))
        
    return kor_chunks

with open('books/dracula/chunk_tasks/ch16_tasks.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

output_data = []
for item in data:
    kor_chunks = split_korean(item['korean_original'], item['english_chunks'])
    output_data.append({
        'paragraph_index': item['paragraph_index'],
        'korean_chunks': kor_chunks
    })

with open('books/dracula/chunk_tasks/ch16_aligned.json', 'w', encoding='utf-8') as f:
    json.dump(output_data, f, ensure_ascii=False, indent=2)
