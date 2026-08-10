import os

en_file = 'c:/git_repo/TKprof_book/books/dracula/chapters/ch25_en.txt'
ko_file = 'c:/git_repo/TKprof_book/books/dracula/chapters/ch25_ko.txt'

with open(en_file, 'r', encoding='utf-8') as f:
    en_text = f.read()

with open(ko_file, 'r', encoding='utf-8') as f:
    ko_text = f.read()

# P061 EN
p061_en_orig = '''[P061] October 28.—When the telegram announcing the arrival at Galatz flew in, surprisingly, none of us seemed greatly shocked. Of course, nobody knew exactly when, where, or how that decisive blow would fall, but we were all inwardly expecting something terribly ominous to happen. As the arrival at Varna kept being delayed, we each instinctively sensed that things would not go exactly our way, and we were simply waiting with bated breath to see where that damn variable would pop up from. Even so, when it actually became reality, it was incredibly bewildering. Human nature tends to lean toward hope no matter what, so it seems that even when we clearly see how things are going, we ultimately want to believe they will work out the way we desire. Transcendent faith might be a lighthouse lighting the way for angels, but to mere mortals, it might be nothing more than a fickle will-o'-the-wisp. It was a truly bizarre experience, and we each absorbed the shock in our own way. Van Helsing threw both hands up over his head for a moment, as if protesting to almighty God, but he said nothing, and a few seconds later he stood up with a resolute expression. Lord Godalming's face turned as white as a sheet of paper, and he slumped down, breathing heavily. I, too, just stared at everyone in turn, half out of my mind with astonishment. Quincey Morris tightened his belt with a familiar and quick motion I knew very well. During our old wandering days, that motion always meant "Time for action." Mrs. Harker's face turned terrifyingly pale, making the scar on her forehead look remarkably fiery red, but she quietly folded her hands and looked up at the empty air as if praying. Jonathan Harker smiled. He truly smiled. It was the dark, bitter smile of a man who had lost all hope. But at the same time, his hand instinctively found the handle of his large kukri knife and gripped it tightly, an action entirely at odds with his eerie smile. Van Helsing spoke up to all of us. "When does the next train to Galatz leave?"'''

p061_en_split = '''[P061a] October 28.—When the telegram announcing the arrival at Galatz flew in, surprisingly, none of us seemed greatly shocked. Of course, nobody knew exactly when, where, or how that decisive blow would fall, but we were all inwardly expecting something terribly ominous to happen. As the arrival at Varna kept being delayed, we each instinctively sensed that things would not go exactly our way, and we were simply waiting with bated breath to see where that damn variable would pop up from. Even so, when it actually became reality, it was incredibly bewildering. Human nature tends to lean toward hope no matter what, so it seems that even when we clearly see how things are going, we ultimately want to believe they will work out the way we desire. Transcendent faith might be a lighthouse lighting the way for angels, but to mere mortals, it might be nothing more than a fickle will-o'-the-wisp. It was a truly bizarre experience, and we each absorbed the shock in our own way.

[P061b] Van Helsing threw both hands up over his head for a moment, as if protesting to almighty God, but he said nothing, and a few seconds later he stood up with a resolute expression. Lord Godalming's face turned as white as a sheet of paper, and he slumped down, breathing heavily. I, too, just stared at everyone in turn, half out of my mind with astonishment. Quincey Morris tightened his belt with a familiar and quick motion I knew very well. During our old wandering days, that motion always meant "Time for action." Mrs. Harker's face turned terrifyingly pale, making the scar on her forehead look remarkably fiery red, but she quietly folded her hands and looked up at the empty air as if praying. Jonathan Harker smiled. He truly smiled. It was the dark, bitter smile of a man who had lost all hope. But at the same time, his hand instinctively found the handle of his large kukri knife and gripped it tightly, an action entirely at odds with his eerie smile. Van Helsing spoke up to all of us. "When does the next train to Galatz leave?"'''

# P061 KO
p061_ko_orig = '''[P061] 10월 28일.—갈라츠 도착을 알리는 전보가 날아들었을 때, 놀랍게도 우리 중 누구도 크게 충격을 받은 것 같지는 않았다. 물론 언제, 어디서, 어떻게 그 결정적인 타격이 가해질지 정확히 아는 사람은 아무도 없었지만, 우리 모두는 내심 뭔가 몹시 불길한 일이 일어날 것이라고 예상하고 있었기 때문이다. 바르나 도착이 계속 지연되면서 우리는 각자 직감적으로 일이 우리 뜻대로만은 흘러가지 않을 것이라 느꼈고, 그저 숨죽인 채 그 빌어먹을 변수가 어디서 튀어나올지만 기다리고 있었다. 그럼에도 불구하고 막상 그것이 현실이 되자, 그 당혹감은 이루 말할 수 없었다. 인간의 본성은 어찌되었든 희망 쪽으로 기울기 마련이라, 일이 어떻게 돌아가는지 뻔히 보이면서도 결국에는 우리가 바라는 대로 잘 풀릴 것이라 믿고 싶어 하는 것 같다. 초월적인 믿음은 천사들에게는 길을 밝혀주는 등대일지 몰라도, 한낱 필멸의 존재들에게는 그저 변덕스러운 도깨비불에 불과할지도 모른다. 그것은 실로 기이한 경험이었고, 우리는 각자 나름의 방식대로 그 충격을 흡수했다. 반 헬싱 교수는 전능하신 신에게 항의라도 하듯 두 손을 머리 위로 번쩍 치켜들었지만 아무 말도 하지 않았고, 몇 초 뒤 단호한 표정으로 일어섰다. 고달밍 경의 얼굴은 백지장처럼 하얗게 질렸고, 그는 거칠게 숨을 몰아쉬며 털썩 주저앉았다. 나 역시 놀라움에 반쯤 넋이 나간 채 모두를 번갈아 쳐다보기만 했다. 퀸시 모리스는 내가 아주 잘 아는, 익숙하고 재빠른 동작으로 허리띠를 바짝 조였다. 우리의 옛 방랑 시절, 그 동작은 늘 "행동 개시"를 의미했다. 하커 부인의 얼굴은 무섭도록 창백해져서 이마의 흉터가 유난히 붉게 타오르는 듯 보였지만, 그녀는 조용히 두 손을 모으고 기도하듯 허공을 올려다보았다. 조나단 하커는 미소를 지었다. 그는 진심으로 미소를 지었다. 그것은 모든 희망을 잃은 자의 어둡고 씁쓸한 미소였다. 하지만 동시에 그의 손은 본능적으로 자신의 커다란 쿠크리 칼자루를 찾아 꽉 움켜쥐었는데, 그것은 그의 기괴한 미소와는 전혀 어울리지 않는 행동이었다. 반 헬싱 교수가 우리 모두를 향해 입을 열었다. "갈라츠로 가는 다음 기차는 언제 출발합니까?"'''

p061_ko_split = '''[P061a] 10월 28일.—갈라츠 도착을 알리는 전보가 날아들었을 때, 놀랍게도 우리 중 누구도 크게 충격을 받은 것 같지는 않았다. 물론 언제, 어디서, 어떻게 그 결정적인 타격이 가해질지 정확히 아는 사람은 아무도 없었지만, 우리 모두는 내심 뭔가 몹시 불길한 일이 일어날 것이라고 예상하고 있었기 때문이다. 바르나 도착이 계속 지연되면서 우리는 각자 직감적으로 일이 우리 뜻대로만은 흘러가지 않을 것이라 느꼈고, 그저 숨죽인 채 그 빌어먹을 변수가 어디서 튀어나올지만 기다리고 있었다. 그럼에도 불구하고 막상 그것이 현실이 되자, 그 당혹감은 이루 말할 수 없었다. 인간의 본성은 어찌되었든 희망 쪽으로 기울기 마련이라, 일이 어떻게 돌아가는지 뻔히 보이면서도 결국에는 우리가 바라는 대로 잘 풀릴 것이라 믿고 싶어 하는 것 같다. 초월적인 믿음은 천사들에게는 길을 밝혀주는 등대일지 몰라도, 한낱 필멸의 존재들에게는 그저 변덕스러운 도깨비불에 불과할지도 모른다. 그것은 실로 기이한 경험이었고, 우리는 각자 나름의 방식대로 그 충격을 흡수했다.

[P061b] 반 헬싱 교수는 전능하신 신에게 항의라도 하듯 두 손을 머리 위로 번쩍 치켜들었지만 아무 말도 하지 않았고, 몇 초 뒤 단호한 표정으로 일어섰다. 고달밍 경의 얼굴은 백지장처럼 하얗게 질렸고, 그는 거칠게 숨을 몰아쉬며 털썩 주저앉았다. 나 역시 놀라움에 반쯤 넋이 나간 채 모두를 번갈아 쳐다보기만 했다. 퀸시 모리스는 내가 아주 잘 아는, 익숙하고 재빠른 동작으로 허리띠를 바짝 조였다. 우리의 옛 방랑 시절, 그 동작은 늘 "행동 개시"를 의미했다. 하커 부인의 얼굴은 무섭도록 창백해져서 이마의 흉터가 유난히 붉게 타오르는 듯 보였지만, 그녀는 조용히 두 손을 모으고 기도하듯 허공을 올려다보았다. 조나단 하커는 미소를 지었다. 그는 진심으로 미소를 지었다. 그것은 모든 희망을 잃은 자의 어둡고 씁쓸한 미소였다. 하지만 동시에 그의 손은 본능적으로 자신의 커다란 쿠크리 칼자루를 찾아 꽉 움켜쥐었는데, 그것은 그의 기괴한 미소와는 전혀 어울리지 않는 행동이었다. 반 헬싱 교수가 우리 모두를 향해 입을 열었다. "갈라츠로 가는 다음 기차는 언제 출발합니까?"'''


en_text = en_text.replace(p061_en_orig, p061_en_split)
ko_text = ko_text.replace(p061_ko_orig, p061_ko_split)


with open(en_file, 'w', encoding='utf-8') as f:
    f.write(en_text)

with open(ko_file, 'w', encoding='utf-8') as f:
    f.write(ko_text)

print("P061 replaced!")
