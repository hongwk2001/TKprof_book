import json
import os

data = []

with open(r'c:\git_repo\TKprof_book\books\dracula\chunk_tasks\ch13_tasks.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Hardcode the boundaries for exact matches
boundaries = {
    19: [
        "그는 내일 아버지의 장례식을 마치고 나서야 겨우 짬이 날 테고, 틀림없이 그녀를, 아니 시신을 한 번 더 보고 싶어 할 테니까요. ",
    ],
    22: [
        "끔찍한 위기가 닥쳤을 때 자네가 다급히 나를 부른 것도 바로 그런 믿음 때문이 아니었나? 그랬지! "
    ],
    34: [
        "열에 아홉은 저희의 판단이 정확했다는 게 훗날 증명되었을 겁니다. ",
        "어머니가 딸보다 먼저 세상을 떴으니 자연스레 딸이 재산을 물려받았을 테고, 딸이 어머니보다 단 5분만 더 숨을 붙어 있었더라도 유언장 하나 없이—그 경황에 유언장을 남길 턱이 없었으니—세상을 떠난 셈이 되어, 그 재산은 주인을 잃고 허공에 뜰 뻔했으니까요. "
    ],
    36: [
        "장의사는 제 직업병을 버리지 못하고 장례용품들을 한껏 과시하듯 진열해 두었는데, 그 특유의 음산한 분위기는 방에 들어서자마자 우리 마음을 한없이 무겁게 짓눌렀다. "
    ],
    73: [
        "조나단은 내가 학교에 가기 전 까마득한 옛날에 그러했듯 내 팔에 다정히 팔짱을 껴왔다. ",
        "게다가 우리를 유심히 지켜볼 아는 얼굴도 없었고, 설령 누가 알아본들 어떠하랴 싶어 우리는 팔짱을 낀 채 유유히 걸음을 옮겼다. "
    ],
    85: [
        "본인이 직접 챙겨야 할 준비물 몇 가지가 있어서 다녀오는 것뿐이라고 덧붙였다. ",
        "나는 반 헬싱 교수의 낯빛이 하얗게 질렸다가 일순간 붉으락푸르락 달아오르는 것을 지켜보았다. ",
        "나중에 본인은 한사코 히스테리가 아니었다며, 그저 끔찍한 상황 속에서 얄궂게도 엉뚱한 유머 감각이 발동했을 뿐이라고 둘러댔지만 말이다. "
    ],
    86: [
        "그는 그 누구에게도 허락을 구하지 않고 때를 가리지도 않지요. ",
        "머리카락과 눈동자 색마저 똑 닮은 그 사랑스러운 아이 때문에 말입니다. ",
        "내 핏줄이 다시 고동치며 그가 머금고 온 햇살을 내 창백한 뺨에 가져다줄 때까지 말입니다. ",
        "우리 인간이란 양쪽에서 팽팽하게 잡아당기는 밧줄과도 같소. "
    ],
    102: [
        "불과 2, 3일 사이 어린아이들이 집을 잃고 헤매거나 히스(Heath)에서 뛰놀다 감쪽같이 사라지는 일이 연거푸 발생했다. ",
        "첫 번째로 실종되었던 아이가 \"아름다운 숙녀가 산책을 가자고 꼬드겨서 따라갔다\"고 진술한 까닭에, 동네 사람들은 다른 아이들 역시 그 그럴싸한 변명을 주워듣고 고스란히 흉내 내는 것이라 지레짐작하고 있다. ",
        "꼬마들의 즉흥적인 야외 연극에서 '아름다운 숙녀'가 단연 인기 배역으로 떠오른 건 그저 유행을 좇는 인간의 얄팍한 본성 때문일지도 모른다. "
    ]
}

result = []
for item in data:
    p_idx = item['paragraph_index']
    kor = item['korean_original']
    chunks = []
    
    bounds = boundaries[p_idx]
    
    current_text = kor
    for b in bounds:
        # find exact boundary string
        idx = current_text.find(b)
        if idx != -1:
            split_point = idx + len(b)
            chunks.append(current_text[:split_point].strip())
            current_text = current_text[split_point:].strip()
        else:
            print(f"Boundary not found for {p_idx}: {b}")
    chunks.append(current_text.strip())
    
    if len(chunks) != len(item['english_chunks']):
        print(f"Length mismatch for {p_idx}: {len(chunks)} vs {len(item['english_chunks'])}")
    
    result.append({
        "paragraph_index": p_idx,
        "korean_chunks": chunks
    })

output_path = r'c:\git_repo\TKprof_book\books\dracula\chunk_tasks\ch13_aligned.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"Successfully wrote {len(result)} items to {output_path}")
