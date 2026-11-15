import sys

ko_chunk = """
61. "아가씨에게 할 말이 있소." 저는 그가 편치 않아 보인다는 것을 알고, 그의 주름진 불쌍한 늙은 손을 제 두 손으로 감싸 쥐며 편하게 다 말씀하시라고 했습니다. 그러자 그는 제 손에 자신의 손을 맡긴 채 이렇게 말했습니다.

62. "예쁜 아가씨, 지난 몇 주 동안 내가 죽은 자들에 대해 했던 그 끔찍한 말들 때문에 아가씨가 충격을 받았을까 봐 걱정이라오. 하지만 내 본심은 그게 아니었소. 내가 죽고 나면 그 사실을 꼭 기억해 주길 바라오. 한쪽 발을 무덤에 걸친 우리 늙은이들은 죽음에 대해 생각하는 걸 영 좋아하지 않지. 그리고 죽음을 두려워하고 싶어 하지도 않고 말이오. 내가 그동안 죽음을 가볍게 여겼던 건 다 그래서였소. 내 스스로 위안을 삼으려고 한 거란 말이오. 하지만 아가씨, 하나님의 사랑으로 맹세컨대, 난 죽는 게 조금도 두렵지 않소. 그저 피할 수만 있다면 죽고 싶지 않을 뿐이지. 내 시간도 이제 다 된 게 틀림없소. 난 늙었고, 백 년이란 세월은 사람이 살기에 너무 긴 시간이지 않소. 그리고 죽음이 너무 가까이 와 있어서, 저승사자가 벌써 낫을 갈고 있는 게 느껴질 정도라오. 아가씨도 알다시피, 나는 죽음에 대해 함부로 말하던 그 버릇을 한 번에 끊어낼 수가 없었소. 턱은 익숙한 대로 움직이기 마련이니까. 머지않아 죽음의 천사가 나를 위해 나팔을 불 거요. 하지만 아가씨, 부디 슬퍼하거나 울지 마시오!"—그는 제가 울고 있는 것을 보았기 때문입니다—"당장 오늘 밤에 그가 온다 해도, 나는 기꺼이 부름에 응할 거요. 결국 삶이라는 건 우리가 지금 하고 있는 일보다 더 중요한 무언가를 기다리는 것에 불과하니까. 그리고 죽음이야말로 우리가 진정으로 의지할 수 있는 유일한 것이지. 하지만 나는 만족하오. 예쁜 아가씨, 죽음이 내게 오고 있으니 말이오. 그것도 아주 빨리. 우리가 이렇게 바라보고 궁금해하는 사이에도 다가오고 있을지 모르오. 어쩌면 상실과 파멸, 크나큰 고통, 그리고 슬픈 마음을 몰고 오는 저 바다 너머의 바람 속에 있을지도 모르지. 저기 보시오! 저길 보시오!" 그가 갑자기 소리쳤습니다. "저 바람 속에, 그리고 저 너머 기침 소리 같은 파도 속에 죽음처럼 들리고, 보이고, 맛이 나고, 냄새가 나는 뭔가가 있소. 공기 중에 말이오. 나는 그게 오고 있는 걸 느낀다오. 주여, 부름이 올 때 기꺼이 대답하게 하소서!" 그는 경건하게 두 팔을 들어 올리고 모자를 벗었습니다. 그의 입은 마치 기도하듯 움직였습니다. 몇 분 동안 침묵한 후, 그는 일어나서 저와 악수를 하고, 제게 축복을 빌어주고는 작별 인사를 하고 절뚝거리며 떠났습니다. 이 모든 일이 제 마음에 닿아 저를 몹시 슬프게 했습니다.

63. 해안경비대원이 망원경을 팔에 끼고 다가왔을 때 저는 기뻤습니다. 그는 늘 그렇듯 저와 이야기하려고 걸음을 멈췄지만, 말하는 내내 시선은 낯선 배 한 척에 고정되어 있었습니다.

64. "도무지 알 수가 없군요." 그가 말했습니다. "겉보기엔 러시아 배 같은데, 아주 이상하게 흔들리고 있습니다. 갈피를 못 잡고 있는 것 같아요. 폭풍이 다가오는 걸 본 것 같긴 한데, 이대로 먼 바다로 나가 북쪽으로 달릴지 아니면 이쪽 항구로 들어올지 결정을 못 내리는 것 같습니다. 저기 다시 한번 보세요! 조종하는 모양이 엄청나게 이상합니다. 키를 잡은 사람의 의도대로 움직이지 않고 있어요. 돌풍이 불 때마다 이리저리 방향이 바뀝니다. 내일 이맘때쯤이면 저 배에 대해 더 많은 소식을 듣게 될 겁니다."
"""

en_chunk = """
61. "I have something I need to tell you, miss." I could see he was uneasy, so I gently held his poor, wrinkled old hand in mine and encouraged him to speak his mind. Leaving his hand resting in mine, he said:

62. "My dear, I'm afraid I must have shocked you these past few weeks with all the wicked things I've said about the dead and everything else. But I didn't truly mean them, and I want you to remember that when I'm gone. Us old folks, with one foot already in the grave, don't much like thinking about death, and we certainly don't want to feel terrified of it. That's why I made a habit of making light of it—just to cheer my own heart up a bit. But God knows, miss, I am not afraid of dying. Not one bit. It's just that I don't want to die if I can avoid it. But my time must be near now. I am very old, and a hundred years is more than any man has a right to expect. I am so close to the end that I can almost hear the Grim Reaper sharpening his scythe. You see, I couldn't just drop the habit of joking about it all at once; my jaw just kept moving the way it was used to. Someday soon, the Angel of Death will blow his trumpet for me. But please, my dear, don't weep or mourn for me!"—he said this because he saw that I had started crying—"If he comes for me this very night, I will answer his call without hesitation. Because, after all, life is really just a waiting room for whatever comes next. Death is the only thing we can truly rely on. And I am at peace, my dear, because it is coming for me, and coming quickly. It might be coming right now, while we sit here wondering. Maybe it's hidden in that wind blowing in off the sea—the one that brings loss, shipwrecks, terrible distress, and broken hearts. Look! Look!" he cried suddenly. "There is something in that wind, and in the cough of the waves out there, that sounds, looks, tastes, and smells like death. It is in the air. I can feel it coming. Lord, let me answer cheerfully when my time comes!" He devoutly raised his arms and tipped his hat. His lips moved silently, as if in prayer. After a few minutes of silence, he stood up, shook my hand, gave me his blessing, said goodbye, and hobbled away. The whole encounter moved me deeply and left me very upset.

63. I was relieved when the coastguard came walking by with his spyglass tucked under his arm. He stopped to chat with me, just as he always does, but he kept his eyes fixed on a strange-looking ship the entire time.

64. "I can't figure her out," he said. "She looks like a Russian vessel, but she's tossing about in the strangest way. She can't seem to make up her mind. It looks like they see the storm coming, but they can't decide whether to head out into the open sea and run north, or try to seek shelter here. Look at her again! She's being steered terribly erratically; the ship isn't responding to the wheel at all. She just spins around with every gust of wind. I guarantee we'll hear more about that ship before this time tomorrow."
"""

with open(r'c:\git_repo\TKprof_book\books\dracula\chapters\ch06_ko_modern.txt', 'a', encoding='utf-8') as f:
    f.write('\n\n' + ko_chunk.strip())

with open(r'c:\git_repo\TKprof_book\books\dracula\chapters\ch06_en_modern.txt', 'a', encoding='utf-8') as f:
    f.write('\n\n' + en_chunk.strip())
