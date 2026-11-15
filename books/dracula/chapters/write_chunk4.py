import codecs

paras = [
'''Letter from Mrs. Harker to Van Helsing.''',
'''"September 25, 6:30 PM.''',
'''"Dear Dr. Van Helsing,—''',
'''"I want to thank you a thousand times for sending such a kind letter. I feel like a heavy burden has been lifted from my heart. But if his journal is all true, what truly terrible things exist in this world! How frightening it is if that man—that monster—is really here in London! Just thinking about it makes me shudder. While writing this letter, I just received a telegram from Jonathan saying he will leave Launceston on the 6:25 train tonight and arrive here at 10:18. Knowing he is coming home makes me feel completely unafraid tonight. So, instead of lunch tomorrow, if it is not too early, how about coming at 8:00 AM to have breakfast with us? If you are busy, you can take the 10:30 train and arrive at Paddington around 2:35. You do not need to reply to this letter. If I do not hear from you, I will assume you are coming for breakfast.''',
'''"Sincerely,''',
'''"Your ever devoted and grateful friend,''',
'''"Mina Harker."''',
'''Jonathan Harker's Journal.''',
'''September 26.—I never thought I would write in this journal again, but the time has finally come. When I returned home last night, Mina was waiting with dinner ready. After we ate, she told me everything about Dr. Van Helsing's visit, giving him a copy of our journal, and how much she had worried about me. Then she showed me the doctor's letter stating that everything I had written in my journal was true. That news seems to have made me a completely new person. What had broken me all this time was the terrible doubt of not knowing what was real and what was an illusion. I had been lost in thick darkness, suffering from helplessness and paranoia. But now that I know the truth, I am no longer afraid—even if it is the Count himself. In the end, his plan to come to London succeeded, and the man I saw really was the Count. He had grown younger, but how on earth could that be? If Dr. Van Helsing is as wonderful as Mina says, he must be the exact person we need to uncover the Count's identity and hunt him down. Mina and I stayed awake late discussing all of this. While Mina gets ready to go out, I plan to go to the hotel in a few minutes to fetch the doctor....''',
'''The doctor seemed inwardly surprised to see me. When I entered the room and greeted him, he grasped both my shoulders, turned my face toward the light, stared at me intently, and said.''',
'''"But Madam Mina told me you were ill. That you had suffered a great shock." Hearing this kind, sharply-featured old gentleman call my wife "Madam Mina" somehow made me smile. I smiled and replied.''',
'''"It is true that I was bedridden and suffered a great shock, but you have already cured my illness, Doctor."''',
'''"How do you mean I cured you?"''',
'''"Thanks to the letter you sent Mina last night. I was lost in deep doubt, feeling as if my entire life was unreal. I didn't know what to believe—I couldn't even trust my own senses. Because I didn't know what to believe, I didn't know what to do. So I simply buried myself in work, trying to escape into my old ordinary routine. But even that routine didn't work for me, and I ended up losing even my belief in myself. Doctor, you probably don't know what it feels like to doubt everything about yourself, even your sanity. No, you could never know. Someone with strong eyebrows like yours would never have experienced such a thing." He chuckled, seemingly pleased by my words, and said.''',
'''"Aha! So you know a bit of physiognomy (reading character from faces). I learn more every hour I am here. I am very much looking forward to having breakfast with you today. And Mr. Jonathan, forgive this old man's compliment, but you are truly blessed to have such a wife." I nodded and listened silently, for I could gladly listen all day to the doctor praising Mina.''',
'''"Your wife is one of the most perfect creatures God has ever made. She is a person God created Himself to show men—and other women as well—that a heaven we can enter truly exists, and that its light can shine right here on earth. She is so true, kind, and noble, yet utterly without selfishness—a rare thing indeed in this suspicious and selfish age. And as for you—I read all the letters you sent to poor Miss Lucy, and some of the letters Lucy left behind also mentioned you. So I had known about you through the words of others for a few days. But it was only through reading your journal last night that I finally saw the real you. Shall we shake hands? Let us be lifelong friends."''',
'''We shook hands, and his genuine, kind demeanor brought a lump to my throat.''',
'''"Now then," he continued. "May I ask you for one more favor? I have an enormous task before me, and the first step is to gather information. You could help me. Could you tell me what happened before you left for Transylvania? I might ask for other kinds of help later, but right now, this is what I need."''',
'''"Listen, Doctor," I said. "Does your task happen to involve the Count?"''',
'''"It does," he answered solemnly.''',
'''"In that case, I am with you with all my heart. Since you have to catch the 10:30 train, you won't have time to read my records right now. But I will pack a bundle of papers for you, so you can read them on the train."''',
'''After breakfast, I saw him off at the station. As we exchanged goodbyes, he said.''',
'''"If I send someone, could you come to London? With Madam Mina, too."''',
'''"If you call, both of us will come anytime," I replied.''',
'''""'''
]

with codecs.open('C:/git_repo/TKprof_book/books/dracula/chapters/ch14_en.txt', 'a', 'utf-8') as f:
    f.write('\n\n'.join(paras))
