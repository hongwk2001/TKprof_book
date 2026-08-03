import re

def refine_korean_text(text):
    # 1. Eliminate unnecessary parenthetical English names or inline comma glossaries.
    text = re.sub(r"'아너러블\(명예로운\)'", "명예로운", text)
    text = re.sub(r"\'아너러블\'", "고귀한", text)
    text = re.sub(r"칼리지 오브 프리셉터스\(사립학교 교사 협회\)", "사립학교 교사 협회", text)
    text = re.sub(r"아담 아이트\(Adamites, 나체주의자\)들", "나체주의자들", text)
    text = re.sub(r"'1만의 퇴각\(Retreat of the Ten Thousand, 고대 그리스 용병들의 퇴각로\)'", "고대 그리스 용병들의 '1만의 퇴각'", text)
    text = re.sub(r"휘터커 연감\(Whitaker’s Almanack\)", "휘터커 연감", text)
    text = re.sub(r"올드 무어 연감\(Old Moore’s Almanack\)", "올드 무어 연감", text)
    text = re.sub(r"주노\(그리스 신화의 여신 헤라\)", "헤라 여신", text)
    text = re.sub(r"'조지 워싱턴 님\(George Washington, Esquire\)'", "조지 워싱턴", text)
    text = re.sub(r"플루타르코스\(영웅전\)", "플루타르코스 영웅전", text)
    text = re.sub(r"교회\(성공회\)", "성공회", text)
    text = re.sub(r"분수\(자리\)", "분수", text)
    text = re.sub(r"분수\(신분\)", "신분", text)
    text = re.sub(r"올림포스의 신들\(상류층\)", "상류층", text)
    text = re.sub(r"올림포스의 신들\(최상류층\)", "최상류층", text)
    text = re.sub(r"식료품 저장실\(하인들의 공간\)", "하인들의 공간인 식료품 저장실", text)
    text = re.sub(r"스카이 테리어\(개\)", "스카이 테리어", text)
    text = re.sub(r"바가텔\(당구와 비슷한 게임\)", "바가텔", text)
    text = re.sub(r"퍼블릭 스쿨\(영국의 명문 사립학교\)", "명문 사립학교", text)
    text = re.sub(r"오\(ō\)", "오", text)
    text = re.sub(r"\'배역\'", "배역", text)
    text = re.sub(r"\([A-Za-z\s,]+\)", "", text) # General English parentheses catch-all if any remain

    # 2 & 3. Smooth out translations
    text = text.replace("영광의 구름을 끌며", "빛나는 후광을 두르고")
    text = text.replace("가장 큰 먹음직스러운 고깃덩어리로 한가운데 띄워놓은 채", "가장 맛깔스러운 요리로 한가운데 떡하니 올려놓은 채")
    text = text.replace("큰 교훈을 얻은 채", "뼈저린 교훈을 얻고서")
    text = text.replace("말하자면 저는 그의 로켓 막대기였습니다.", "비유하자면 저는 그 로켓의 꼬리 날개였습니다.")
    text = text.replace("마침내 그들의 묘비 크기가 그들이 그 역할을 얼마나 훌륭하게 수행했는지를 말해줍니다.", "마침내는 묘비의 크기만이 그들이 제 역할을 얼마나 훌륭히 수행했는지 증명할 따름입니다.")
    text = text.replace("어떤 흔치 않은 횡적인 힘에 부딪혀", "어떤 기이한 횡압력에 떠밀려")
    text = text.replace("저는 매우 시급히 이야기하고 싶은 흔치 않은 일련의 강렬한 인상들을 가지고 있습니다.", "제 안에는 당장이라도 털어놓지 않고는 배길 수 없는 강렬하고도 기이한 기억들이 소용돌이치고 있습니다.")
    text = text.replace("저는 아주 다른 여러 계층에서 삶을 경험했고", "저는 실로 다양한 계층의 삶을 전전했고")
    text = text.replace("나중에 채텀 빈민 병원에서 사망한 제 사촌인 제빵 노동자의 집에서 불청객으로 지낸 적도 있습니다.", "훗날 채텀의 빈민 병원에서 생을 마감한 제빵 노동자 사촌의 집에 불청객으로 얹혀살기도 했습니다.")
    text = text.replace("저택의 식료품 보관실에서 하인들이 부당하게 빼돌려준 간식을 몰래 먹기도 했고", "대저택의 식료품 보관실에서 하인들이 몰래 빼돌려준 간식으로 주린 배를 채우기도 했고")

    return text

with open(r"c:\git_repo\TKprof_book\books\tono_bungay\chapters\book1\book1_ch01_ko.txt", "r", encoding="utf-8") as f:
    text = f.read()

refined_text = refine_korean_text(text)

with open(r"c:\git_repo\TKprof_book\scratch\tagged_book1_ch01_ko_proposal.txt", "w", encoding="utf-8") as f:
    f.write(refined_text)
