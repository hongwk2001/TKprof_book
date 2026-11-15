import re

def fix_ch08_exact():
    filepath = 'chapters/ch08_ko.txt'
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    paras = [p.strip() for p in text.split('\n\n') if p.strip()]

    # Re-build Ch 08 KO so P043, P044a, P044b, P044c, P045a, P045b, P046 match EN 1:1
    new_paras = []
    
    for p in paras:
        m = re.match(r'^\[(P[a-zA-Z0-9_]+)\]', p)
        if not m:
            continue
        pid = m.group(1)

        if pid == 'P043':
            # This is the merged P043
            new_paras.append(p)
            # Right after P043, insert exact P044a, P044b, P044c, P045a, P045b, P046
            new_paras.append('[P044a] "꿈이라기엔 모든 게 너무 생생했어. 난 그저 이 자리에 있고 싶었어. 왜인지는 몰라. 무언가 두려웠거든. 그게 뭔지도 모르면서. 잠든 와중에도 거리를 지나 다리를 건너던 기억이 나.')
            new_paras.append('[P044b] 물고기 한 마리가 펄쩍 뛰어올라 몸을 숙여 바라봤고, 계단을 오를 땐 온 동네 개들이 짖어대는 소리가 들렸어. 그러다 해 질 녘에 보았던 것처럼 붉은 눈을 번뜩이는 길고 검은 무언가가 어렴풋이 떠올랐고, 달콤하면서도 씁쓸한 기운이 나를 확 감싸 안았어. 그다음엔 짙푸른 물속으로 깊이 가라앉는 기분이 들었고 물에 빠진 사람들이 듣는다는 그 윙윙거리는 소리가 귓가를 맴돌았지.')
            new_paras.append('[P044c] 그러고는 모든 게 멀어지는 것 같았어. 내 영혼이 몸을 빠져나가 허공을 떠도는 기분이었지. 발밑으로 서쪽 등대가 보였던 것도 같아. 그러다 마치 지진이라도 난 듯 고통이 밀려왔고, 다시 정신을 차려보니 네가 내 몸을 흔들고 있더라. 몸에 닿는 느낌보다 날 흔드는 네 모습이 먼저 보였어."')
            new_paras.append('[P045a] 그러고서 루시는 웃음을 터뜨렸습니다. 저는 어딘지 모르게 섬뜩해서 숨죽인 채 그녀의 말을 들었죠. 마음이 썩 내키지 않아 그 주제에 계속 붙들려 있는 건 좋지 않다 싶어 화제를 돌렸고, 루시는 다시 예전의 밝은 모습으로 돌아왔습니다. 집에 도착했을 무렵 신선한 바람을 맞은 덕분에 그녀는 한결 기운을 차렸고, 창백하던 뺨도 장밋빛으로 물들었죠.')
            new_paras.append('[P045b] 어머니도 그런 루시의 모습에 크게 기뻐하셨고 우리는 모두 함께 아주 행복한 저녁을 보냈습니다.')
            new_paras.append('[P046] *       *       *       *       *')
        elif pid in ['P044a', 'P044b', 'P044c', 'P045a', 'P045b', 'P046']:
            # Skip old P044-P046 since we inserted the correct exact ones above
            continue
        else:
            new_paras.append(p)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(new_paras) + '\n')

    print("Re-built Ch 08 P043-P046 block perfectly.")

if __name__ == '__main__':
    fix_ch08_exact()
