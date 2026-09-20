import json
import os

patch_data = {
    'book2_ch_20': {
        'P006_1': {
            'ko': '“이런 영광을 주셔서 큰 은혜를 입었습니다.” 스트라이버(Stryver) 씨가 말했다. “제가 차례가 되어도 이런 영광을 돌려드릴 기회를 얻을 만큼 운이 좋지 않기 때문에 저에게 이런 영광이 베풀어지는 것은 더욱 드문 일입니다.”',
            'en': '“I am greatly indebted to you for this honor,” said Mr. Stryver, “which is all the more rare for me to receive, as I am never fortunate enough to have the opportunity to return it to you when my turn comes.”'
        }
    },
    'book2_ch_21': {
        'P027_2': {
            'ko': '그의 중얼거리는 상상 외에는 그것들을 볼 수 있는 빛이 없었습니다. 그는 한 번 이상 창문으로 다가가 밖을 내다보며 메아리에 귀를 기울이곤 했습니다.',
            'en': 'with no light to see them by except his own muttering imagination; more than once, he would step to the window and look out to listen to the echoes.'
        },
        'P036_1': {
            'ko': '“여기 있소!” 드파르주(Defarge)가 퉁명스러운 목소리로, 마치 자신의 몸통 일부인 것처럼 그의 옆에서 굳건하게 말을 타고 있는 남자에게 말했다.',
            'en': '“Here he is!” said Defarge in a gruff voice, to a man who rode as solidly by his side as if he were a part of his own body.'
        },
        'P050_2': {
            'ko': '하지만 드파르주(Defarge)가 그 위를 넘어가는 순간, 이 반짝이는 빛들은 그에게 감옥의 루버(환기창)가 되었고, 그는 그곳이 바스티유(Bastille) 감옥이라는 것을 알았다.',
            'en': 'But the moment Defarge crossed over it, these glints of light became the louvers of a prison to him, and he knew it was the Bastille.'
        },
        'P057_2': {
            'ko': '그들과 함께 드파르주(Defarge)가 있었다.',
            'en': 'With them was Defarge.'
        }
    },
    'book2_ch_24': {
        'P008_3': {
            'ko': '스스로 남겨진 그 집은, 타종 장치(striker)가 바늘을 떼어낸 거대한 시계의 부속품처럼, 그만의 조용한 발걸음으로 미끄러지듯 움직였다.',
            'en': 'The house, left to itself, glided along with its own silent step, like the mechanisms of a massive clock when the striker has removed its hands.'
        },
        'P023_1': {
            'ko': '왜냐하면, 그 편지의 내용은 그에게 파멸적이었기 때문이다; 편지의 모든 단어가 타격이었고, 그가 그것을 읽었을 때, 그는 마치 자신의 사형 집행 영장을 읽고 있는 것처럼 느껴졌다.',
            'en': 'For the contents of the letter were devastating to him; every word was a blow, and when he read it, he felt as if he were reading his own death warrant.'
        },
        'P049_5': {
            'ko': '그것은 찰스 다네이(Charles Darnay)에게 모든 방법 중 최선의 것이었다.',
            'en': 'It was the best of all the ways for Charles Darnay.'
        },
        'P050_3': {
            'ko': '그의 이름으로 쓰여지고 그에게로 보내진 편지가 도착했고, 그는 겁쟁이가 될 수 없었다.',
            'en': 'The letter, written in his name and addressed to him, had arrived, and he could not be a coward.'
        }
    },
    'book3_ch_01': {
        'P007_1': {
            'ko': '무리의 중앙에 있던 드파르주(Defarge)가 그를 바라보며 말했다. “당신을 안다, 시민이여.”',
            'en': 'Defarge, who was in the center of the group, looked at him and said: “I know you, Citizen.”'
        },
        'P027_2': {
            'ko': '그는 그러지 않았소.”',
            'en': 'he has not.”'
        },
        'P036_4': {
            'ko': '나는 무장한 애국자들의 호위 아래 파리로 가고 있으며, 내 친구 드파르주(Defarge)의 직접적인 보호를 받으며 파리로 가고 있소.”',
            'en': 'I am going to Paris under the escort of armed patriots, and I am going to Paris under the direct protection of a friend of mine, Defarge.”'
        },
        'P053_3': {
            'ko': '“그가 그렇게 했소!”',
            'en': '“That he has!”'
        }
    },
    'book3_ch_02': {
        'P002_1': {
            'ko': '파리의 생제르맹(Saint Germain) 구역에 설립된 텔슨 은행(Tellson’s Bank)은 안뜰로 접근하고 높은 벽과 튼튼한 문으로 거리와 차단된 큰 집의 별관에 있었다.',
            'en': 'Tellson\'s Bank, located in the Saint Germain Quarter of Paris, was situated in a wing of a large house, accessible through a courtyard and enclosed from the street by a high wall and a sturdy gate.'
        },
        'P007_2': {
            'ko': '그곳에 안경을 쓰고 책에 코를 박은 채 로리(Lorry) 씨가 앉아서 일을 하고 있었다.',
            'en': 'There, with his spectacles on and his nose buried in a book, Mr. Lorry sat working.'
        },
        'P020_1': {
            'ko': '“오, 사랑하는 친구여!” 그녀의 아내가 두 무릎을 꿇고 애원의 고통 속에 두 손을 움켜쥐며 외쳤다. “오, 사랑하는 친구여! 내 남편이!”',
            'en': '“Oh, my dear friend!” cried his wife, falling to both her knees and clasping her hands in an agony of pleading, “Oh, my dear friend! My husband!”'
        },
        'P026_1': {
            'ko': '순식간에 큰 문의 종이 울리고, 발소리와 목소리의 큰 소음이 안뜰로 쏟아져 들어왔다.',
            'en': 'In an instant, the bell at the main gate rang, and a loud clatter of footsteps and voices poured into the courtyard.'
        },
        'P034_1': {
            'ko': '“그들은,” 로리(Lorry) 씨가 굳게 닫힌 방을 두려운 듯이 힐끗 돌아보며 그 단어들을 속삭였다. “죄수들을 학살하고 있소."',
            'en': '“They are,” Mr. Lorry whispered the words, glancing fearfully round at the locked room, “murdering the prisoners."'
        },
        'P035_1': {
            'ko': '마네트(Manette) 박사는 그의 손을 꽉 쥐고 맨머리로 서둘러 방을 나갔으며, 로리(Lorry) 씨가 블라인드로 다시 돌아왔을 때는 안뜰에 있었다.',
            'en': 'Doctor Manette squeezed his hand, hurried out of the room bareheaded, and was already in the courtyard by the time Mr. Lorry returned to the window blind.'
        },
        'P036_3': {
            'ko': '그리고 나서 로리(Lorry) 씨는 그가 모두에게 둘러싸여, 어깨를 맞대고 손을 어깨에 얹은 채 줄지어 선 스무 명의 남자들 한가운데서 “바스티유(Bastille) 죄수 만세!”라는 외침과 함께 서둘러 나가는 것을 보았다.',
            'en': 'and then Mr. Lorry saw him, surrounded by everyone, and in the middle of a line of twenty men long, all linked shoulder to shoulder and hand to shoulder, being hurried out with shouts of—\'Long live the Bastille prisoner!\''
        },
        'P039_2': {
            'ko': '군인들의 칼이 거기서 벼려진단다,” 로리(Lorry) 씨가 말했다. “이곳은 이제 국유 재산이고, 일종의 무기고(armoury)로 사용되고 있지, 내 사랑.”',
            'en': 'The soldiers’ swords are sharpened there,” said Mr. Lorry. “The place is national property now, and used as a sort of armory, my dear.”'
        },
        'P041_1': {
            'ko': '로리(Lorry) 씨가 다시 내다보았을 때 거대한 숫돌인 지구가 돌아가 있었고, 안뜰에는 해가 붉게 물들어 있었다.',
            'en': 'The great grindstone, Earth, had turned when Mr. Lorry looked out again, and the sun cast a red glow over the courtyard.'
        }
    },
    'book3_ch_03': {
        'P002_1': {
            'ko': '영업시간이 돌아왔을 때 로리(Lorry) 씨의 사업가적인 마음속에 떠오른 첫 번째 고려 사항 중 하나는 이것이었다. 즉, 그에게는 망명자 죄수의 아내를 은행 지붕 아래 숨겨줌으로써 텔슨 은행(Tellson’s)을 위험에 빠뜨릴 권리가 없다는 것이었다.',
            'en': 'One of the first considerations that arose in Mr. Lorry’s business-minded head when business hours began was this: he had no right to endanger Tellson\'s by sheltering the wife of an emigré prisoner under the Bank\'s roof.'
        },
        'P004_1': {
            'ko': '정오가 다가오고 박사는 돌아오지 않았으며, 일 분 일 초의 지연이 텔슨 은행(Tellson’s)을 위태롭게 하는 상황에서 로리(Lorry) 씨는 루시(Lucie)와 상의했다.',
            'en': 'As noon approached, the Doctor had not returned, and with every passing minute of delay threatening to compromise Tellson’s, Mr. Lorry consulted with Lucie.'
        },
        'P004_4': {
            'ko': '이에 대해 사업상의 반대가 없었고, 찰스(Charles)가 무사하여 풀려난다 하더라도 도시를 떠날 가망이 없음을 내다본 로리(Lorry) 씨는 그러한 숙소를 찾으러 나갔고, 높고 우울한 건물들의 닫힌 블라인드가 버려진 집들을 나타내는 외진 골목길 높은 곳에서 적당한 곳을 찾았다.',
            'en': 'Since there was no business objection to this plan, and as he anticipated that even if all went well with Charles and he was released, he could not expect to leave the city, Mr. Lorry went out in search of such a lodging. He found a suitable one high up in a secluded side street, where the closed blinds in all the other windows of a tall, gloomy square of buildings marked abandoned homes.'
        },
        'P007_1': {
            'ko': '“반갑습니다,” 로리(Lorry) 씨가 말했다. “저를 아십니까?”',
            'en': '“At your service,” said Mr. Lorry. “Do you know me?”'
        },
        'P012_1': {
            'ko': '로리(Lorry) 씨는 큰 관심과 동요를 느끼며 말했다.',
            'en': 'Greatly interested and agitated, Mr. Lorry said:'
        },
        'P018_1': {
            'ko': '“나와 동행하시겠소,” 이 쪽지를 소리 내어 읽고 나서 기쁘게 안도한 로리(Lorry) 씨가 말했다. “그의 아내가 머무는 곳으로?”',
            'en': '“Will you accompany me,” said Mr. Lorry, joyfully relieved after reading this note aloud, “to where his wife is staying?”'
        },
        'P020_1': {
            'ko': '드파르주(Defarge)가 얼마나 기묘할 정도로 내성적이고 기계적인 태도로 말하는지 아직 거의 눈치채지 못한 채, 로리(Lorry) 씨는 모자를 쓰고 그들과 함께 안뜰로 내려갔다.',
            'en': 'Barely noticing as yet the curiously reserved and mechanical way in which Defarge spoke, Mr. Lorry put on his hat, and they went down into the courtyard.'
        },
        'P021_1': {
            'ko': '“드파르주(Defarge) 부인, 확실하군요!” 로리(Lorry) 씨가 약 17년 전과 완전히 똑같은 자세로 있던 그녀를 남겨두고 떠났던 기억을 떠올리며 말했다.',
            'en': '“Madame Defarge, surely!” said Mr. Lorry, who had left her in exactly the same posture some seventeen years ago.'
        },
        'P023_1': {
            'ko': '“부인도 우리와 함께 가는 건가요?” 로리(Lorry) 씨가 그들이 움직이는 대로 그녀도 움직이는 것을 보고 물었다.',
            'en': '“Is Madame coming with us?” inquired Mr. Lorry, seeing that she moved when they moved.'
        },
        'P025_1': {
            'ko': '드파르주(Defarge)의 태도에 이상함을 느끼기 시작한 로리(Lorry) 씨는 그를 의심스럽게 쳐다보며 앞장섰다.',
            'en': 'Beginning to be struck by Defarge’s demeanor, Mr. Lorry looked at him dubiously and led the way.'
        },
        'P026_2': {
            'ko': '그녀는 로리(Lorry) 씨가 전해준 남편의 소식에 환희에 빠졌고, 그의 쪽지를 전해준 손을 움켜쥐었다--그 손이 밤에 남편 곁에서 무슨 일을 하고 있었는지, 그리고 어쩌면 우연이 아니었다면 남편에게 무슨 짓을 했을지도 모른 채.',
            'en': 'She was thrown into ecstasy by the news Mr. Lorry brought of her husband, and she clasped the hand that delivered his note—little suspecting what that hand had been doing near him in the night, and what it might have done to him, but for chance.'
        },
        'P030_1': {
            'ko': '“얘야,” 로리(Lorry) 씨가 설명하기 위해 끼어들며 말했다.',
            'en': '“My dear,” said Mr. Lorry, stepping in to explain;'
        },
        'P030_5': {
            'ko': '내 생각엔,” 세 사람 모두의 돌처럼 굳은 태도가 점점 더 그에게 각인됨에 따라 위로의 말을 다소 머뭇거리며 로리(Lorry) 씨가 말했다. “내가 상황을 제대로 설명하고 있는 거요, 드파르주(Defarge) 시민?”',
            'en': 'I believe,” said Mr. Lorry, rather faltering in his reassuring words as the stony demeanor of all three impressed itself more and more upon him, “I state the matter correctly, Citizen Defarge?”'
        },
        'P032_1': {
            'ko': '“루시(Lucie), 그러는 게 낫겠구나,” 로리(Lorry) 씨가 어조와 태도로 비위를 맞추기 위해 최선을 다하며 말했다. “귀여운 아이와 우리의 훌륭한 프로스(Pross)를 여기로 데려오렴.',
            'en': '“You had better, Lucie,” said Mr. Lorry, doing all he could to conciliate them by his tone and manner, “bring the dear child here, and our good Pross.'
        },
        'P035_1': {
            'ko': '“예, 부인.” 로리(Lorry) 씨가 대답했다.',
            'en': '“Yes, madame,” answered Mr. Lorry;'
        },
        'P052_1': {
            'ko': '“용기를 내렴, 친애하는 루시(Lucie),” 로리(Lorry) 씨가 그녀를 일으켜 세우며 말했다. “용기를, 용기를!"',
            'en': '“Courage, my dear Lucie,” said Mr. Lorry as he helped her up. “Courage, courage!"'
        },
        'P054_1': {
            'ko': '“쯧, 쯧!” 로리(Lorry) 씨가 말했다.',
            'en': '“Tut, tut!” said Mr. Lorry;'
        }
    },
    'book3_ch_04': {
        'P003_1': {
            'ko': '마네트 박사는 로리(Lorry) 씨에게 굳이 강조할 필요도 없는 비밀 유지라는 조건하에, 군중이 그를 대학살의 현장을 거쳐 라 포르스(La Force) 감옥으로 데려갔다고 전했다.',
            'en': 'To Mr. Lorry, the Doctor communicated, under a strict injunction of secrecy that required no elaboration, that the crowd had led him through a scene of carnage to the prison of La Force.'
        },
        'P006_1': {
            'ko': '로리(Lorry) 씨가 이러한 비밀을 전해 듣고 이제 예순두 살이 된 친구의 얼굴을 지켜볼 때, 그러한 끔찍한 경험들이 옛날의 위험을 되살리지 않을까 하는 불안감이 그의 마음에 일어났다.',
            'en': 'As Mr. Lorry received these confidences, and as he watched the face of his friend, who was now sixty-two years old, a foreboding arose within him that such dreadful experiences might rekindle the old danger.'
        },
        'P009_2': {
            'ko': '그럼에도 불구하고 현명한 로리(Lorry) 씨는 그 안에 그를 지탱해 주는 새로운 자부심이 있다는 것을 알았다.',
            'en': 'still, the sagacious Mr. Lorry perceived that it contained a new, sustaining pride.'
        },
        'P009_9': {
            'ko': '그와 루시(Lucie)의 이전 상대적 위치가 역전되었지만, 오직 가장 활기찬 감사와 애정만이 그것들을 역전시킬 수 있었으니, 그에게 그토록 많은 것을 해준 그녀에게 어떤 봉사를 하는 것 외에는 그가 자부심을 가질 수 없었기 때문이다. “모두 참 흥미로운 일이군,” 로리(Lorry) 씨는 그 특유의 상냥하고 예리한 태도로 생각했다. “하지만 모두 자연스럽고 옳은 일이야."',
            'en': 'The earlier relative positions of himself and Lucie had been reversed, but only in the way that the most vibrant gratitude and affection could reverse them, for his sole pride lay in providing some service to the one who had done so much for him. "It is all curious to witness," thought Mr. Lorry in his amiably shrewd manner, "but entirely natural and right;"'
        }
    },
    'book3_ch_05': {
        'P052_1': {
            'ko': '의자 위에 승마 코트를 벗어둔 채, 절대 남의 눈에 띄어서는 안 되는 로리(Lorry) 씨와 함께 있는 저 사람은 누구란 말인가?',
            'en': 'Who could that be with Mr. Lorry—the owner of the riding coat left on the chair—who had to remain unseen?'
        }
    },
    'book3_ch_06': {
        'P010_14': {
            'ko': '죄수가 볼 수 있는 한, 그 재판소와 관련이 없는 사람들 중에서 평소의 옷을 입고 거친 카르마뇰(Carmagnole) 복장을 입지 않은 남자는 그와 로리(Lorry) 씨뿐이었다.',
            'en': 'As far as the prisoner could tell, he and Mr. Lorry were the only men present, unconnected with the Tribunal, who wore their regular clothes rather than adopting the coarse garb of the Carmagnole.'
        },
        'P042_2': {
            'ko': '카르마뇰(Carmagnole)의 거센 소용돌이를 뚫고 힘겹게 헤쳐 나오느라 숨을 헐떡이며 헐레벌떡 들어온 로리(Lorry) 씨의 손을 꽉 잡은 후에;',
            'en': 'after gripping the hand of Mr. Lorry, who came panting in breathlessly from his struggle against the chaotic torrent of the Carmagnole;'
        }
    },
    'book3_ch_07': {
        'P005_5': {
            'ko': '그리고 (로리(Lorry) 씨에 의해 그들에게 거의 전적으로 이관된) 제리(Jerry)는 그들의 매일의 하인이 되어 매일 밤 그곳에서 잠을 잤다.',
            'en': 'and Jerry (almost entirely handed over to them by Mr. Lorry) had become their daily retainer, sleeping there every night.'
        },
        'P006_2': {
            'ko': '그러므로 제리 크런처(Jerry Cruncher) 씨의 이름이 아래 문설주를 합당하게 장식했다.',
            'en': 'Mr. Jerry Cruncher’s name, therefore, suitably decorated the doorpost down below;'
        },
        'P008_1': {
            'ko': '지난 몇 달 동안 프로스(Pross) 양과 크런처(Cruncher) 씨는 물품 조달의 역할을 수행해 왔다.',
            'en': 'For the past few months, Miss Pross and Mr. Cruncher had carried out the duties of purveyors;'
        },
        'P008_7': {
            'ko': '결과적으로 그녀는 크런처(Cruncher) 씨만큼이나 그 “허튼소리”(그녀가 부르기 좋아하는 대로)에 대해 알지 못했다.',
            'en': 'consequently, she knew no more about that “nonsense” (as she preferred to call it) than Mr. Cruncher did.'
        },
        'P009_1': {
            'ko': '“자, 크런처(Cruncher) 씨,” 기쁨으로 눈이 붉어진 프로스(Pross) 양이 말했다.',
            'en': '“Now, Mr. Cruncher,” said Miss Pross, whose eyes were red with happiness;'
        },
        'P014_1': {
            'ko': '크런처(Cruncher) 씨는 다소 조심스럽게 그것이 “늙은 닉(Old Nick, 악마)의 것”을 의미한다고 설명했다.',
            'en': 'Mr. Cruncher, with a bit of diffidence, explained that he meant “Old Nick’s.”'
        },
        'P022_1': {
            'ko': '크런처(Cruncher) 씨는 충성심에 사로잡혀 마치 교회에 온 사람처럼 으르렁거리며 프로스(Pross) 양의 말을 따라 했다.',
            'en': 'Mr. Cruncher, in a surge of loyalty, growled the words repeatedly after Miss Pross, like someone at church.'
        },
        'P025_4': {
            'ko': '자, 크런처(Cruncher) 씨!--움직이지 마세요, 무당벌레 아가씨!”',
            'en': 'Now, Mr. Cruncher!—Don’t you move, Ladybird!”'
        },
        'P026_2': {
            'ko': '로리(Lorry) 씨가 곧 은행에서 돌아올 것으로 예상되었다.',
            'en': 'Mr. Lorry was expected to return shortly from the Banking House.'
        }
    }
}

base_dir = 'c:/git_repo/TKprof_book/books/two_cities/json/'
for ch, patches in patch_data.items():
    file_path = os.path.join(base_dir, f'{ch}.json')
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        for block in data:
            if block.get('tag') in patches:
                block['ko'] = patches[block['tag']]['ko']
                block['en'] = patches[block['tag']]['en']
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
print('Patch complete!')
