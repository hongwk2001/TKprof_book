import json

translations = {
    "book3_ch_14.json__batch0030": [
        {"ko": "저 끔찍한 수레들이 굴러가는 소리가 나잖소!", "en": "“There's the sound of those dreadful carts rolling by!”"},
        {"ko": "저 소린 들리시죠, 아가씨?”", "en": "“You can hear that, miss?”"},
        {"ko": "“저는 아무것도,” 그가 자신에게 말하고 있다는 것을 본 Miss Pross가 대답했다. “들리지 않아요.", "en": "“I can hear,” said Miss Pross, seeing that he was talking to her, “nothing.”"},
        {"ko": "아, 선량한 당신, 먼저 큰 굉음이 있었고 그 뒤에 엄청난 정적이 찾아왔는데, 그 정적은 내 목숨이 붙어 있는 한 영원히 깨지지 않을 것처럼 단단히 고정되고 변치 않는 것 같아요.”", "en": "“Oh, my good man, first there was a great crash, and then a great stillness, and that stillness feels so permanent and unchangeable that it seems it will never be broken for the rest of my life.”"},
        {"ko": "“저 끔찍한 수레들이 굴러가는 소리, 이제 여정의 끝에 다다른 저 소리마저 못 듣는다면,” Mr.", "en": "“If she can't hear the sound of those dreadful carts, which are now very close to the end of their journey,” said Mr."},
        {"ko": "Cruncher가 어깨 너머로 힐끗 쳐다보며 말했다. “내 생각엔 진정 그녀가 이 세상에서 다른 어떤 소리도 다시는 듣지 못할 것 같군.”", "en": "Cruncher, glancing over his shoulder, “then it's my opinion that she truly will never hear anything else in this world.”"},
        {"ko": "그리고 진정 그녀는 다시는 듣지 못했다.", "en": "And indeed, she never did."}
    ]
}

chapter_file = 'c:/git_repo/TKprof_book/books/two_cities/json/book3_ch_14.json'
queue_file = 'c:/git_repo/TKprof_book/books/two_cities/json/work_queue.json'

with open(chapter_file, 'r', encoding='utf-8') as f:
    chapter_data = json.load(f)

for batch_id, trans_list in translations.items():
    with open(queue_file, 'r', encoding='utf-8') as f:
        queue = json.load(f)
    
    batch = next(b for b in queue if b['batch_id'] == batch_id)
    tags = batch['tags']
    
    for block in chapter_data:
        if block['tag'] in tags:
            idx = tags.index(block['tag'])
            block['ko'] = trans_list[idx]['ko']
            block['en'] = trans_list[idx]['en']
            
    for b in queue:
        if b['batch_id'] == batch_id:
            b['status'] = 'done'
            
    with open(queue_file, 'w', encoding='utf-8') as f:
        json.dump(queue, f, indent=2)

with open(chapter_file, 'w', encoding='utf-8') as f:
    json.dump(chapter_data, f, indent=2, ensure_ascii=False)

print("Batch 30 done")
