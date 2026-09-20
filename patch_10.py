import json

file_path = 'c:/git_repo/TKprof_book/books/two_cities/json/book3_ch_01.json'

with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

translations = {
    'P003_1': {
        'ko': '1792년 가을 영국에서 파리를 향해 가는 여행자는 자신의 길을 천천히 나아갔다.',
        'en': 'The traveler proceeded slowly on his way, heading toward Paris from England in the autumn of the year 1792.'
    },
    'P003_2': {
        'ko': '몰락하고 불운한 프랑스 국왕이 그의 모든 영광 속에서 왕좌에 앉아 있었다 하더라도, 그는 나쁜 도로와 나쁜 마차, 그리고 나쁜 말들로 인해 자신을 지연시킬 만큼 충분히 많은 어려움과 마주쳤을 것이다.',
        'en': 'He would have encountered more than enough bad roads, bad carriages, and bad horses to delay him, even if the fallen and unfortunate King of France had been on his throne in all his glory;'
    },
    'P003_3': {
        'ko': '그러나 변화된 시대는 이것들 이외의 다른 장애물들로 가득 차 있었다.',
        'en': 'but the changed times were filled with other obstacles besides these.'
    },
    'P003_4': {
        'ko': '모든 마을 성문과 세관에는 국가의 머스킷 소총을 가장 폭발적으로 발사할 준비가 된 시민 애국자들의 무리가 있었고, 그들은 오고 가는 모든 이들을 멈춰 세워 반대 심문을 하고, 서류를 검사하고, 그들만의 목록에서 이름을 찾아보고는, 변덕스러운 판단이나 변덕이 동터오는 자유, 평등, 박애, 아니면 죽음의 나눌 수 없는 하나의 공화국을 위해 최선이라고 여기는 대로 그들을 돌려보내거나, 통과시키거나, 혹은 멈춰 세우고 구금했다.',
        'en': 'Every town gate and village tollhouse had its band of citizen-patriots, with their national muskets in a most explosive state of readiness. They stopped all comers and goers, interrogated them, inspected their papers, checked their names against their own lists, and either turned them back, sent them on, or arrested them, just as their capricious judgment or fancy deemed best for the dawning One and Indivisible Republic of Liberty, Equality, Fraternity, or Death.'
    },
    'P004_1': {
        'ko': '그의 여정이 불과 몇 프랑스 리그밖에 진행되지 않았을 때, Charles Darnay는 파리에서 훌륭한 시민으로 선언받기 전까지는 이 시골 길을 따라 그가 돌아갈 희망이 없다는 것을 깨닫기 시작했다.',
        'en': 'Only a very few French leagues of his journey had been completed when Charles Darnay began to realize that for him, along these country roads, there was no hope of return until he had been declared a good citizen in Paris.'
    },
    'P004_2': {
        'ko': '지금 무슨 일이 일어나든, 그는 여정의 끝까지 가야만 했다.',
        'en': 'Whatever might happen now, he had to continue to the end of his journey.'
    },
    'P004_3': {
        'ko': '어떤 초라한 마을이 그를 에워싸고 닫히거나 평범한 장벽이 그의 뒤 도로에 내려질 때마다, 그는 그것이 그와 영국 사이를 가로막는 일련의 쇠문들 중 또 다른 하나라는 것을 알았다.',
        'en': 'Every time a poor village closed in on him, or a common barrier dropped across the road behind him, he knew it was just another iron door in the series that barred him from England.'
    },
    'P004_4': {
        'ko': '보편적인 감시가 그를 그토록 옥죄었기에, 만약 그가 그물에 잡혔거나 우리에 갇혀 목적지로 이송되고 있다 하더라도, 그는 자신의 자유가 이보다 더 완벽하게 사라졌다고 느끼지는 못했을 것이다.',
        'en': 'The universal watchfulness surrounded him so completely that even if he had been caught in a net or were being sent to his destination in a cage, he could not have felt that his freedom was more totally gone.'
    },
    'P005_1': {
        'ko': '이러한 보편적인 감시는 한 구간의 고속도로에서 그를 스무 번이나 멈춰 세웠을 뿐만 아니라, 그를 쫓아가서 데려오고, 그보다 앞서가서 미리 멈춰 세우며, 그와 함께 말을 타고 가며 그를 구금함으로써 하루에도 스무 번씩이나 그의 진행을 지연시켰다.',
        'en': 'This universal watchfulness not only stopped him on the highway twenty times per stage, but it also delayed his progress twenty times a day by riding after him and taking him back, riding ahead of him and stopping him in advance, or riding alongside him and keeping him in custody.'
    },
    'P005_2': {
        'ko': '그가 여전히 파리에서 멀리 떨어진 큰길가의 작은 마을에서 지쳐 잠자리에 들었을 때, 그는 프랑스 내에서만 며칠째 여정을 이어가고 있었다.',
        'en': 'He had already been traveling in France for days when he went to bed exhausted in a small town on the main road, still a long way from Paris.'
    }
}

count = 0
for block in data:
    if block.get('tag') in translations:
        block['ko'] = translations[block['tag']]['ko']
        block['en'] = translations[block['tag']]['en']
        count += 1

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print(f"Patched {count} blocks")
