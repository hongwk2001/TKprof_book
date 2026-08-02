import os
import re

BASE_DIR = r"c:\git_repo\TKprof_book\books\tono_bungay\chapters"

CHAPTER_TITLES = {
    (1, 1): "[1부 1장: 블레이즈오버 저택과 어머니, 그리고 사회의 구조]",
    (1, 2): "[1부 2장: 세상으로의 진출, 그리고 블레이즈오버에서의 마지막 기억]",
    (1, 3): "[1부 3장: 윔블허스트에서의 나날과 폰데레보 삼촌]",
    (2, 1): "[2부 1장: 런던의 학생이 되어 길을 잃다]",
    (2, 2): "[2부 2장: 오폰톤의 환상]",
    (2, 3): "[2부 3장: 매리온과의 약혼과 새로운 모색]",
    (2, 4): "[2부 4장: 결혼생활과 토노 번게이의 탄생]",
    (3, 1): "[3부 1장: 하딩엄 호텔과 사업의 거대한 부상]",
    (3, 2): "[3부 2장: 로맨스와 막대한 부의 영광]",
    (3, 3): "[3부 3장: 크레스트힐 전당과 비행 기계]",
    (3, 4): "[3부 4장: 쿼포드 탐사와 어두운 모험]",
    (4, 1): "[4부 1장: 토노 번게이의 대몰락]",
    (4, 2): "[4부 2장: 잔해 속에서 피어난 사랑]",
    (4, 3): "[4부 3장: 밤과 탁 트인 바다]",
}

def clean_content(text, b_num, c_num):
    lines = text.split("\n")
    
    # 1. Fix line 1 header if it's English or raw
    if lines and (lines[0].startswith("Book ") or lines[0].startswith("제") or lines[0].startswith("#")):
        # If line 1 is English header like 'Book 1 Chapter 1...' replace it with clean title
        if lines[0].startswith("Book "):
            lines[0] = CHAPTER_TITLES.get((b_num, c_num), f"[{b_num}부 {c_num}장]")
    
    content = "\n".join(lines)
    
    # 2. Remove English in parentheses: e.g. 베오(Beow) -> 베오, 토노-번게이(Tono-Bungay) -> 토노-번게이
    # Match Korean word immediately followed by (English text)
    content = re.sub(r'([가-힣]+)\s*\([A-Za-z0-9\s\'\-\._]+\)', r'\1', content)
    
    # 3. Remove inline English glossary parens: e.g. (Tono-Bungay), (John Bull)
    content = re.sub(r'\s*\([A-Za-z0-9\s\'\-\._]+\)', '', content)
    
    # 4. Remove Hanja in commas/parens: e.g. , 多産, or (多産)
    content = re.sub(r',\s*[\u4e00-\u9fff]+\s*,', '', content)
    content = re.sub(r'\s*\([\u4e00-\u9fff]+\)', '', content)
    
    # 5. Remove comma-bracketed English terms & inline glossary notes:
    # e.g. , urban style of dressing,
    # e.g. , frock-coat, 19세기 및 에드워드 시대 남성들이 입던 무릎 길이의 예복,
    # e.g. , John Bull,
    # e.g. , Sloper,
    # e.g. , gin bottle,
    # e.g. , Gnostic, 고대 종교 및 철학적 사상,
    content = re.sub(r',\s*[A-Za-z0-9\s\'\-\._]+(?:\s*,\s*[^,\n]+)?\s*,', '', content)
    
    # 6. Remove redundant explanatory commas for Korean words:
    # e.g. 프랩, 빅토리아 시대 중간 계급에서는 사촌도 예의상 '삼촌/당숙'이라 불렀습니다, -> 프랩
    content = re.sub(r',\s*빅토리아 시대 [^,\n]+,', '', content)
    content = re.sub(r',\s*영국 켄트주에 있는 [^,\n]+,', '', content)
    content = re.sub(r',\s*19세기 [^,\n]+,', '', content)
    content = re.sub(r',\s*고대 종교 [^,\n]+,', '', content)
    content = re.sub(r',\s*앙고라염소의 [^,\n]+,', '', content)
    content = re.sub(r',\s*셜록 홈즈가 [^,\n]+,', '', content)
    content = re.sub(r',\s*런던의 부유층 [^,\n]+,', '', content)
    content = re.sub(r',\s*지중해 동부 [^,\n]+,', '', content)
    content = re.sub(r',\s*경찰 소식,', '', content)

    # Clean double spaces or broken punctuation
    content = re.sub(r'[ \t]{2,}', ' ', content)
    content = re.sub(r' ,', ',', content)
    
    return content

def main():
    cleaned_count = 0
    for b_num in range(1, 5):
        book_dir = os.path.join(BASE_DIR, f"book{b_num}")
        if not os.path.exists(book_dir):
            continue
        for fname in os.listdir(book_dir):
            if fname.endswith("_ko.txt"):
                c_num_match = re.search(r'ch(\d+)', fname)
                if not c_num_match:
                    continue
                c_num = int(c_num_match.group(1))
                filepath = os.path.join(book_dir, fname)
                with open(filepath, "r", encoding="utf-8") as f:
                    text = f.read()
                cleaned = clean_content(text, b_num, c_num)
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(cleaned)
                cleaned_count += 1
                print(f"Cleaned: book{b_num}_ch{c_num:02d}_ko.txt")
    print(f"\nDone! Cleaned {cleaned_count} Korean chapter files for Tono-Bungay.")

if __name__ == "__main__":
    main()
