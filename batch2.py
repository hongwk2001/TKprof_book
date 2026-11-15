import json
import os

translations = {
    135: {"ko": "\"넌 저주받은 망명자야,\" 대장장이가 망치를 손에 쥐고 군중을 뚫고 맹렬히 그에게 달려들며 소리쳤다.", "en": "\"You are a cursed emigrant,\" cried a farrier, making at him in a furious manner through the press, hammer in hand;"},
    136: {"ko": "\"그리고 넌 저주받은 귀족이야!\"", "en": "\"and you are a cursed aristocrat!\""},
    137: {"ko": "역장이 이 남자와 기수의 고삐(그가 분명히 노리고 있던) 사이에 끼어들며 달래듯 말했다. \"그를 내버려 두시오;", "en": "The postmaster interposed himself between this man and the rider's bridle (at which he was evidently making), and soothingly said, \"Let him be;"},
    138: {"ko": "그를 내버려 두시오!", "en": "let him be!"},
    139: {"ko": "그는 파리에서 재판을 받을 것이오.\"", "en": "He will be judged at Paris.\""},
    140: {"ko": "\"재판을 받는다고!\" 대장장이가 망치를 휘두르며 반복했다. \"그래! 그리고 반역자로 유죄 판결을 받겠지.\" 이에 군중은 찬성의 함성을 질렀다.", "en": "\"Judged!\" repeated the farrier, swinging his hammer. \"Ay! and condemned as a traitor.\" At this the crowd roared approval."},
    141: {"ko": "마당으로 말 머리를 돌리려던 역장을 저지하며 (술에 취한 애국자는 밧줄을 손목에 감은 채 안장에 침착하게 앉아 지켜보고 있었다), 다네이는 자신의 목소리가 들릴 수 있게 되자마자 말했다:", "en": "Checking the postmaster, who was for turning his horse's head to the yard (the drunken patriot sat composedly in his saddle looking on, with the line round his wrist), Darnay said, as soon as he could make his voice heard:"},
    142: {"ko": "\"친구들, 당신들은 스스로를 속이고 있거나, 아니면 속고 있는 것이오.", "en": "\"Friends, you deceive yourselves, or you are deceived."},
    143: {"ko": "나는 반역자가 아니오.\"", "en": "I am not a traitor.\""},
    144: {"ko": "\"그는 거짓말을 하고 있어!\" 대장장이가 소리쳤다. \"그는 법령 이후로 반역자야.", "en": "\"He lies!\" cried the smith. \"He is a traitor since the decree."},
    145: {"ko": "그의 저주받은 목숨은 그의 것이 아니야!\"", "en": "His cursed life is not his own!\""},
    146: {"ko": "또 다른 순간이었다면 그를 덮쳤을 군중의 눈에 살기가 번뜩이는 것을 다네이가 본 순간, 역장은 말을 마당 안으로 돌렸고, 호위병은 그의 말 옆구리에 바짝 붙어 말을 몰았으며, 역장은 낡은 이중문을 닫고 빗장을 질렀다.", "en": "At the instant when Darnay saw a rush in the eyes of the crowd, which another instant would have brought upon him, the postmaster turned his horse into the yard, the escort rode in close upon his horse's flanks, and the postmaster shut and barred the crazy double gates."},
    147: {"ko": "대장장이가 망치로 문을 내리쳤고 군중은 신음 소리를 냈다;", "en": "The farrier struck a blow upon them with his hammer, and the crowd groaned;"},
    148: {"ko": "하지만 더 이상의 일은 일어나지 않았다.", "en": "but, no more was done."},
    149: {"ko": "\"대장장이가 말한 이 법령이란 것이 무엇입니까?\" 다네이가 역장에게 감사를 표한 후 마당에 그와 나란히 서서 물었다.", "en": "\"What is this decree that the smith spoke of?\" Darnay asked the postmaster, when he had thanked him, and stood beside him in the yard."},
    150: {"ko": "\"진실로, 망명자의 재산을 매각하라는 법령입니다.\"", "en": "\"Truly, a decree for selling the property of emigrants.\""},
    151: {"ko": "\"언제 통과되었습니까?\"", "en": "\"When passed?\""},
    152: {"ko": "\"14일에요.\"", "en": "\"On the fourteenth.\""},
    153: {"ko": "\"내가 영국을 떠난 날이군요!\"", "en": "\"The day I left England!\""},
    154: {"ko": "\"모두들 그것은 여러 개 중 하나일 뿐이고, 아직 없다면, 앞으로 모든 망명자를 추방하고 돌아오는 모든 사람에게 사형을 선고하는 다른 법령들이 있을 거라고 말합니다.", "en": "\"Everybody says it is but one of several, and that there will be others--if there are not already--banishing all emigrants, and condemning all to death who return."},
    155: {"ko": "당신의 목숨이 당신의 것이 아니라고 그가 말한 것은 그런 의미였습니다.\"", "en": "That is what he meant when he said your life was not your own.\""},
    156: {"ko": "\"하지만 아직 그런 법령은 없지 않습니까?\"", "en": "\"But there are no such decrees yet?\""},
    157: {"ko": "\"내가 뭘 알겠습니까!\" 역장이 어깨를 으쓱하며 말했다;", "en": "\"What do I know!\" said the postmaster, shrugging his shoulders;"},
    158: {"ko": "\"그럴 수도 있고, 그렇게 될 수도 있겠지요.", "en": "\"there may be, or there will be."},
    159: {"ko": "다 마찬가지입니다.\"", "en": "It is all the same."},
    160: {"ko": "그들은 한밤중까지 다락방의 짚 위에서 쉬다가, 온 마을이 잠든 후 다시 말을 타고 앞으로 나아갔다.", "en": "They rested on some straw in a loft until the middle of the night, and then rode forward again when all the town was asleep."},
    161: {"ko": "이 거칠고 기이한 밤길을 비현실적으로 만든, 익숙한 것들에서 관찰되는 많은 급격한 변화들 중에서 적지 않은 것은 수면의 겉보기 부족이었다.", "en": "Among the many wild changes observable on familiar things which made this wild ride unreal, not the least was the seeming rarity of sleep."},
    162: {"ko": "음산한 도로 위로 길고 외로운 박차를 가한 후, 그들은 어둠 속에 잠겨 있지 않고 불빛으로 모두 반짝이는 가난한 오두막 무리에 도착하곤 했고, 한밤중에 사람들이 유령 같은 모습으로 시들어가는 자유의 나무 주위를 손에 손을 잡고 돌거나, 모두 함께 모여 자유의 노래를 부르는 것을 보았다.", "en": "After long and lonely spurring over dreary roads, they would come to a cluster of poor cottages, not steeped in darkness, but all glittering with lights, and would find the people, in a ghostly manner in the dead of the night, circling hand in hand round a shrivelled tree of Liberty, or all drawn up together singing a Liberty song."},
    163: {"ko": "그러나 다행히도 그날 밤 보베에는 그들이 그곳을 벗어날 수 있도록 도와줄 수면이 있었고 그들은 다시 한 번 고독과 외로움 속으로 지나갔다:", "en": "Happily, however, there was sleep in Beauvais that night to help them out of it and they passed on once more into solitude and loneliness:"},
    164: {"ko": "때 이른 추위와 젖은 공기를 뚫고 덜그럭거리며 나아가면서, 그해 땅의 어떤 열매도 맺지 못한 황폐한 들판 사이를 지났는데, 불에 탄 집들의 검게 그을린 잔해들과, 모든 도로에서 망을 보던 애국자 순찰대가 매복 상태에서 갑자기 나타나 그들의 길을 가로막고 날카롭게 고삐를 당기는 일들로 변화가 많았다.", "en": "jingling through the untimely cold and wet, among impoverished fields that had yielded no fruits of the earth that year, diversified by the blackened remains of burnt houses, and by the sudden emergence from ambuscade, and sharp reining up across their way, of patriot patrols on the watch on all the roads."},
    165: {"ko": "마침내 파리의 장벽 앞에서 날이 밝았다.", "en": "Daylight at last found them before the wall of Paris."},
    166: {"ko": "그들이 말을 타고 다가갔을 때 장벽은 닫혀 있었고 삼엄하게 경비되고 있었다.", "en": "The barrier was closed and strongly guarded when they rode up to it."},
    167: {"ko": "\"이 죄수의 서류는 어디에 있나?\" 경비병의 부름을 받고 나온 결연해 보이는 권위자가 요구했다.", "en": "\"Where are the papers of this prisoner?\" demanded a resolute-looking man in authority, who was summoned out by the guard."}
}

with open('c:/git_repo/TKprof_book/work_queue.json', 'r', encoding='utf-8') as f:
    queue = json.load(f)

for i in range(135, 168):
    entry = queue[i]
    if i in translations:
        # Patch the file
        filepath = os.path.join('c:/git_repo/TKprof_book/books/two_cities/json', entry['file'])
        with open(filepath, 'r', encoding='utf-8') as jf:
            file_data = json.load(jf)
        for block in file_data:
            if block.get('target_raw') == entry['target_raw'] or block.get('tag') == entry['target_raw']:
                block['ko'] = translations[i]['ko']
                block['en'] = translations[i]['en']
                break
        with open(filepath, 'w', encoding='utf-8') as jf:
            json.dump(file_data, jf, ensure_ascii=False, indent=2)
        # Update queue
        entry['status'] = 'done'

with open('c:/git_repo/TKprof_book/work_queue.json', 'w', encoding='utf-8') as f:
    json.dump(queue, f, ensure_ascii=False, indent=2)

print("Batch 2 completed!")
