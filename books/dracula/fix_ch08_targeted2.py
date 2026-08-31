import os
import re

def fix_targeted_chunk2():
    filepath = 'chapters/ch08_ko.txt'
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    
    aligned_chunk = """[P047] 8월 19일 - 기뻐라, 기뻐라, 기뻐라! 비록 온통 기쁜 일만 있는 건 아니지만요. 방금 사랑하는 내 조나단이 있는 곳을 알려주는 소식을 들었거든요. 조나단은 뇌수염을 앓고 부다페스트의 한 병원에서 지내고 있었습니다. 건강을 꽤 회복하긴 했지만 기력이 많이 쇠한 모양이에요. 저는 곧장 조나단에게로 떠나 수간호사가 되어줄 생각입니다. 그러려면 클루지에 갈 때처럼 밤낮으로 기차를 타야 하니 이제 짐을 싸야겠어요. 옷은 딱 한 벌만 챙겼고, 루시가 제 트렁크를 런던으로 가져가기로 했습니다. 서둘러서 준비해야겠어요!

[P048a] 부다페스트 성 요셉 및 성모 마리아 병원의 아가타 수녀가

[P048b] 윌헬미나 머리 양에게 보낸 편지.

[P049] "8월 12일

[P050] "친애하는 부인께,

[P051a] "직접 펜을 들 만큼 아직 기력을 회복하진 못하셨지만, 하커 씨의 부탁으로 제가 대신 편지를 전합니다. 다만 이곳에서 사랑어린 보살핌을 받은 덕분에 상태는 많이 호전되었습니다.

[P051b] 정중한 인사와 함께 업무가 늦어져 죄송하며 맡겨진 모든 일에 최선을 다하겠다는 메시지를 엑서터의 피터 호킨스 씨에게 전해달라고 부탁하셨는데, 이것이 그가 기억하는 전부였습니다.

[P053] "안녕히 계십시오.

[P053b] "깊은 연민과 축복을 담아,

[P054] "아가타 수녀 올림.

[P055a] "추신 - 환자분이 잠든 틈을 타 봉투를 다시 열고 몇 가지 말씀을 덧붙입니다. 환자분은 어떤 극심한 충격을 받았고, 뇌척수막염을 앓는 동안 늑대니 독이니 피니 유령이니 악마니 하는 것들을 끔찍하게 헛소리하듯 중얼거리셨습니다. 이게 사실일지는 모르겠지만요.

[P055b] 당분간은 이런 일로 그를 자극할 만한 것이 없도록 각별히 주의하시기 바랍니다. 병의 흔적이 그에게 깊게 남아 있으니까요.

[P055c] 그 난폭한 행동을 보고 영국인인 걸 눈치챈 역무원들이 고향으로 돌아가는 완행 열차표를 동정심에 사주었답니다. 그가 이곳에서 보살핌을 잘 받고 있으니 마음 푹 놓으시길 바랍니다. 특유의 다정함과 온화함으로 이미 우리 모두의 마음을 사로잡았답니다. 정말 훌륭한 분이세요."
"""

    # We need to replace from [P047a] up to right before [P056].
    # In the current ch08_ko.txt, [P047] doesn't have 'a' anymore? Wait, let's look at the dump from debug_ko_tags.txt!
    # Ah! The previous script decremented old tags.
    # What was [P047a] before is now... wait!
    # My previous script:
    # "We will decrement all tags in `after` by 1 so [P047] becomes [P046], [P048] -> [P047], etc."
    # The old [P047] was "* * * * *" -> became [P046].
    # The old [P048a] was "8월 19일..." -> became [P047a].
    # So the tag is currently [P047a].
    
    start_idx = text.find('[P047a]')
    end_idx = text.find('[P056]')
    
    before = text[:start_idx]
    after = text[end_idx:]
    
    # We don't need to decrement or increment the remaining tags this time!
    # Why? Because in English, the tags are [P047] to [P055c].
    # The next English tag is [P056] ("Dr. Seward's Diary").
    # The next Korean tag in `after` is ALREADY [P056] ("수어드 박사의 일기").
    # So by replacing exactly this chunk and ending right before [P056],
    # the sequence naturally aligns with English! No tag shifting needed for the rest of the document!
    
    final_text = before + aligned_chunk.strip() + '\n\n' + after
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(final_text)

if __name__ == '__main__':
    fix_targeted_chunk2()
