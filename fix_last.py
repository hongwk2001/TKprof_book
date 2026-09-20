import json

with open('c:/git_repo/TKprof_book/translated_batches/batch_0_99.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

for x in d:
    ko = x['ko']
    if 'Joe!"' in ko and 'pull' in ko:
        x['ko'] = '한 번만 더 당기면 정상에 도착할 거야, 빌어먹을, 여기까지 오는 데 충분히 고생했으니까!, 조!'
    elif 'Jerry' in ko and 'hoarse' in ko:
        x['ko'] = '호위병이 혼잣말로 투덜거렸습니다. "만약 저게 제리라면, 제리의 목소리는 마음에 안 들어. 목소리가 내 취향에는 너무 쉬었군, 그 제리라는 사람."'
    elif 'Hey you!' in ko and 'muttering' in ko:
        x['ko'] = '호위병이 혼잣말로 중얼거렸습니다. "그러길 바라지만 그렇게 확신할 순 없지." "어이 너!"'
    elif 'holsters' in ko and 'saddle' in ko:
        x['ko'] = '그리고 네 그 안장에 권총집이 있다면, 네 손이 그 근처에 가는 걸 내 눈에 띄게 하지 마.'
    elif 'bullet' in ko and 'mistake' in ko:
        x['ko'] = '왜냐하면 난 아주 빨리 실수를 저지르고, 그럴 땐 총알로 하거든.'

with open('c:/git_repo/TKprof_book/translated_batches/batch_0_99.json', 'w', encoding='utf-8') as f:
    json.dump(d, f, ensure_ascii=False, indent=2)
