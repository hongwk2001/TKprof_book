import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHAPTERS_DIR = os.path.join(BASE_DIR, "books", "scaramouche", "chapters")

INTRO_EN = """[About the Author & Book]

Rafael Sabatini's 1921 classic "Scaramouche" is a masterpiece of historical adventure, romance, and theatrical swashbuckling set against the dramatic backdrop of the French Revolution.

The story follows André-Louis Moreau, a young lawyer who is indifferent to political struggles until his friend, a passionate young priest named Philippe de Vilmorin, is brutally murdered in a staged duel by the arrogant nobleman Marquis de La Tour d'Azyr. Vowing to avenge his friend, André-Louis embarks on a journey that leads him from a revolutionary orator to a member of a Commedia dell'arte acting troupe as the character Scaramouche, and finally to a fencing master.

This modernized edition is optimized for contemporary readers, language learners, and Text-to-Speech listeners, prioritizing natural pacing, subject-first sentence structures, and fluid spoken rhythm while preserving Sabatini's brilliant theatrical atmosphere and historical accuracy.
"""

INTRO_KO = """[작가 및 작품 소개]

라파엘 사바티니의 1921년 고전 명작 《스카라무슈》는 프랑스 혁명이라는 격동의 시기를 배경으로 연극적 상상력과 흥미진진한 검술 활극을 융합한 역사 모험 소설의 걸작입니다.

주인공 앙드레 루이 모로는 본래 혁명의 열기에는 무관심한 차가운 법률가였으나, 절친한 친구이자 이상주의 사제였던 필립 드 빌모랭이 오만한 귀족 라 투르 다르지르侯에게 결투로 무참히 살해당하는 사건을 목격하며 복수를 맹세하게 됩니다. 그는 수배를 피하는 과정에서 유랑 극단의 광대 '스카라무슈'로 변신해 무대 위에서 세상을 조롱하고, 마침내 전설적인 검술가로 성장하며 혁명의 거대한 소용돌이에 휩쓸려 갑니다.

본 편역본은 가독성을 향상시킨 현대적이고 세련된 어휘를 사용하고, 인물 간의 관계와 극적인 대화의 긴장감을 살려 오디오북 청취와 현대 독자들의 독서 흐름에 완벽히 부합하도록 구성되었습니다.
"""

COPY_EN = """[Copyright & Editorial Notes]

Thank you for reading this modernized edition of "Scaramouche".

If you enjoyed the historical adventure and theatrical wit of André-Louis, please consider leaving a review on your preferred eBook store. Your feedback supports our continuous effort to modernize classic literature.

Editorial Notes:
- Obsolete syntax and archaic structures have been modernized for clear and accessible reading.
- Long, winding multi-clause sentences have been split to ensure smooth Text-to-Speech listening flow.
- Historical terms of the French Revolution (such as Tiers État, States-General) and Commedia dell'arte names have been carefully retained to preserve the original period setting.

This work is based on the original 1921 text by Rafael Sabatini, which is in the public domain. This modernized edition and adaptation is copyright TKPROF LLC.

For support, inquiries, or feedback: tkprof.ai@gmail.com
"""

COPY_KO = """[저작권 및 편집자 노트]

《스카라무슈》 현대 한국어 판을 읽어주셔서 대단히 감사합니다.

앙드레 루이의 날카로운 기지와 혁명기의 격동적인 활극을 재미있게 읽으셨다면, 독자 리뷰를 작성해 주시길 부탁드립니다. 독자 여러분의 소중한 평가는 세계적인 고전 작품들을 더 가깝고 읽기 쉽게 현대화하는 작업에 큰 힘이 됩니다.

편집자 노트:
- 18세기 프랑스 혁명기의 시대상과 혁명 관련 용어(제3신분, 삼부회 등) 및 이탈리아 가면극(코메디아 델라르테) 용어를 충실하게 보존하여 작품 특유의 분위기를 살렸습니다.
- 긴 호흡의 긴 문장들은 오디오북 청취와 자연스러운 말소리 흐름에 최적화되도록 간결하게 윤문하였습니다.

이 번역본은 라파엘 사바티니의 1921년 원작(퍼블릭 도메인)을 바탕으로 새롭게 현대화한 편역본입니다. 이 현대화 버전의 모든 텍스트 편집본에 대한 저작권은 TKPROF LLC에 있습니다.

문의 및 피드백: tkprof.ai@gmail.com
"""

def main():
    os.makedirs(CHAPTERS_DIR, exist_ok=True)
    
    files = {
        "introduction_en.txt": INTRO_EN,
        "introduction_ko.txt": INTRO_KO,
        "copyright_en.txt": COPY_EN,
        "copyright_ko.txt": COPY_KO
    }
    
    for filename, content in files.items():
        filepath = os.path.join(CHAPTERS_DIR, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content.strip() + "\n")
        print(f"Created: {filename}")

if __name__ == "__main__":
    main()
