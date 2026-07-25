import os

def tag_dialogue():
    input_path = r"d:\git_repo\TKprof_book\books\odyssey\chapters\ch_22_en.txt"
    output_dir = r"d:\git_repo\TKprof_book\books\odyssey\chapters\tagged"
    output_path = os.path.join(output_dir, "tagged_ch_22_en.txt")
    
    with open(input_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    replacements = [
        # Line 5
        (
            'declared, "The great archery contest is over. Now, let\'s see if Apollo will grant me the power to hit another target—one that no man has ever struck before."',
            'declared, <odysseus>"The great archery contest is over. Now, let\'s see if Apollo will grant me the power to hit another target—one that no man has ever struck before."</odysseus>'
        ),
        # Line 9
        (
            'shouted, "Stranger, you\'ll pay dearly for shooting people like this! You won\'t live to see another contest. You\'re a dead man! The one you killed was the finest young man in Ithaca, and for this crime, vultures will feast on your body!"',
            'shouted, <others>"Stranger, you\'ll pay dearly for shooting people like this! You won\'t live to see another contest. You\'re a dead man! The one you killed was the finest young man in Ithaca, and for this crime, vultures will feast on your body!"</others>'
        ),
        # Line 13
        (
            '"You dogs! Did you really think I wouldn\'t return from Troy? You\'ve squandered my wealth, forced my female servants to your beds, and tried to marry my wife while I was still alive! You feared neither gods nor men. Now, you will die!"',
            '<odysseus>"You dogs! Did you really think I wouldn\'t return from Troy? You\'ve squandered my wealth, forced my female servants to your beds, and tried to marry my wife while I was still alive! You feared neither gods nor men. Now, you will die!"</odysseus>'
        ),
        # Line 17
        (
            '"If you are truly Lord Odysseus," he began, "then your words are just. We have done great wrong in your lands and in your house. But Antinous, the ringleader of all our sins, already lies dead. Everything was his doing. He didn\'t truly want to marry Queen Penelope; he didn\'t care much for marriage at all. What he truly desired was something else entirely, and Zeus did not grant it to him. He wanted to kill your son and become the most powerful man in Ithaca. Now that he has met the death he deserved, please spare the lives of your people. We will make everything right and fully repay you for all we have eaten and drunk in your house. Each of us will pay a fine worth twenty oxen, and we will continue to offer you gold and bronze until your heart softens. Until we have done this, no one can complain about your anger towards us."',
            '<others>"If you are truly Lord Odysseus,"</others> he began, <others>"then your words are just. We have done great wrong in your lands and in your house. But Antinous, the ringleader of all our sins, already lies dead. Everything was his doing. He didn\'t truly want to marry Queen Penelope; he didn\'t care much for marriage at all. What he truly desired was something else entirely, and Zeus did not grant it to him. He wanted to kill your son and become the most powerful man in Ithaca. Now that he has met the death he deserved, please spare the lives of your people. We will make everything right and fully repay you for all we have eaten and drunk in your house. Each of us will pay a fine worth twenty oxen, and we will continue to offer you gold and bronze until your heart softens. Until we have done this, no one can complain about your anger towards us."</others>'
        ),
        # Line 19
        (
            'said, "Even if you gave me everything you possess now, and everything you ever will possess, I will not stop my hand until I have made every single one of you pay in full. You must fight, or try to run for your lives. But I promise you, not a single one of you will escape!"',
            'said, <odysseus>"Even if you gave me everything you possess now, and everything you ever will possess, I will not stop my hand until I have made every single one of you pay in full. You must fight, or try to run for your lives. But I promise you, not a single one of you will escape!"</odysseus>'
        ),
        # Line 23
        (
            '"My friends, this man will show us no mercy! He\'ll stand right there and shoot us down until every one of us is dead. So, let\'s fight back! Draw your swords, and use the tables as shields against his arrows. Let\'s rush him fiercely, drive him from the floor and the doorway. Then we can get into town and raise such an alarm that his shooting will surely stop!"',
            '<others>"My friends, this man will show us no mercy! He\'ll stand right there and shoot us down until every one of us is dead. So, let\'s fight back! Draw your swords, and use the tables as shields against his arrows. Let\'s rush him fiercely, drive him from the floor and the doorway. Then we can get into town and raise such an alarm that his shooting will surely stop!"</others>'
        ),
        # Line 29
        (
            '"Father, let me bring you a shield, two spears, and a bronze helmet for your head. I\'ll arm myself too, and bring armor for the swineherd and the cowherd. We all need to be armed!"',
            '<telemachus>"Father, let me bring you a shield, two spears, and a bronze helmet for your head. I\'ll arm myself too, and bring armor for the swineherd and the cowherd. We all need to be armed!"</telemachus>'
        ),
        # Line 31
        (
            '"Go quickly and get them!" Odysseus replied. "Do it before my arrows run out. If I\'m left alone, they might manage to push me away from the door."',
            '<odysseus>"Go quickly and get them!"</odysseus> Odysseus replied. <odysseus>"Do it before my arrows run out. If I\'m left alone, they might manage to push me away from the door."</odysseus>'
        ),
        # Line 35
        (
            'shouted loudly, "Can\'t someone go through the trapdoor and tell the people what\'s happening? Help would come at once, and we could quickly put an end to this man and his deadly archery!"',
            'shouted loudly, <others>"Can\'t someone go through the trapdoor and tell the people what\'s happening? Help would come at once, and we could quickly put an end to this man and his deadly archery!"</others>'
        ),
        # Line 37
        (
            '"That won\'t work, Agelaus," Melanthius replied. "The entrance to that narrow passage is dangerously close to the outer courtyard\'s entrance. Even one brave man could stop any number of people from getting in. But I know what I\'ll do. I\'ll bring you weapons from the storeroom. I\'m certain Odysseus and his son have hidden their arms there!"',
            '<others>"That won\'t work, Agelaus,"</others> Melanthius replied. <others>"The entrance to that narrow passage is dangerously close to the outer courtyard\'s entrance. Even one brave man could stop any number of people from getting in. But I know what I\'ll do. I\'ll bring you weapons from the storeroom. I\'m certain Odysseus and his son have hidden their arms there!"</others>'
        ),
        # Line 39
        (
            'said, "Someone among the women inside is helping the suitors against us, or it could be Melanthius himself."',
            'said, <odysseus>"Someone among the women inside is helping the suitors against us, or it could be Melanthius himself."</odysseus>'
        ),
        # Line 41
        (
            'replied, "Father, the fault is mine. It\'s entirely my fault. I left the storeroom door open, and they were sharper than I was. Eumaeus, go and close the door. Then check to see if it\'s one of the women, or if it\'s Melanthius, Dolios\'s son, as I suspect."',
            'replied, <telemachus>"Father, the fault is mine. It\'s entirely my fault. I left the storeroom door open, and they were sharper than I was. Eumaeus, go and close the door. Then check to see if it\'s one of the women, or if it\'s Melanthius, Dolios\'s son, as I suspect."</telemachus>'
        ),
        # Line 43
        (
            'said, "Your Majesty Odysseus, brave son of Laertes, it\'s that villain Melanthius, just as we suspected! He\'s going to the storeroom. If I can overpower him, should I kill him? Or should I drag him here so you can take your own revenge for all the evil he\'s done in your house?"',
            'said, <others>"Your Majesty Odysseus, brave son of Laertes, it\'s that villain Melanthius, just as we suspected! He\'s going to the storeroom. If I can overpower him, should I kill him? Or should I drag him here so you can take your own revenge for all the evil he\'s done in your house?"</others>'
        ),
        # Line 45
        (
            'replied, "Telemachus and I will hold these suitors in check, no matter what they do. Both of you, go back and bind Melanthius\'s hands and feet behind his back. Throw him into the storeroom and lock the door tightly. Then tie a rope around his body and hang him from a high pillar, close to the rafters. He will die slowly in agony."',
            'replied, <odysseus>"Telemachus and I will hold these suitors in check, no matter what they do. Both of you, go back and bind Melanthius\'s hands and feet behind his back. Throw him into the storeroom and lock the door tightly. Then tie a rope around his body and hang him from a high pillar, close to the rafters. He will die slowly in agony."</odysseus>'
        ),
        # Line 47
        (
            'shouted triumphantly at Melanthius, "Melanthius, you\'ll spend the night on a comfortable bed, just as you deserve! When morning comes from the streams of Oceanus, you\'ll know very well it\'s time for you to drive in the goats for the suitors\' feast!"',
            'shouted triumphantly at Melanthius, <others>"Melanthius, you\'ll spend the night on a comfortable bed, just as you deserve! When morning comes from the streams of Oceanus, you\'ll know very well it\'s time for you to drive in the goats for the suitors\' feast!"</others>'
        ),
        # Line 49
        (
            'He said, "Mentor, please help me. Don\'t forget your old comrade, who has done you many favors. Besides, aren\'t we age-mates?"',
            'He said, <odysseus>"Mentor, please help me. Don\'t forget your old comrade, who has done you many favors. Besides, aren\'t we age-mates?"</odysseus>'
        ),
        # Line 51
        (
            'criticize her. "Mentor!" he shouted. "Don\'t let Odysseus trick you into siding with him and fighting us suitors! Here\'s what we\'ll do: once we\'ve killed this father and son, we\'ll kill you too. You\'ll pay for it with your life. After we kill you, we\'ll confiscate all your property, both inside and outside your house, and combine it with Odysseus\'s wealth. Your sons and daughters won\'t live in your house, and your wife won\'t be able to live in the city of Ithaca!"',
            'criticize her. <others>"Mentor!"</others> he shouted. <others>"Don\'t let Odysseus trick you into siding with him and fighting us suitors! Here\'s what we\'ll do: once we\'ve killed this father and son, we\'ll kill you too. You\'ll pay for it with your life. After we kill you, we\'ll confiscate all your property, both inside and outside your house, and combine it with Odysseus\'s wealth. Your sons and daughters won\'t live in your house, and your wife won\'t be able to live in the city of Ithaca!"</others>'
        ),
        # Line 53
        (
            'angrily. "Odysseus," she said, "your strength and prowess are not what they were when you fought the Trojans for nine long years for noble Helen! Back then, you killed countless enemies, and Priam\'s city fell because of your cunning plans. So why have you so lamentably lost your courage now? You are here in your own home, on your own land, facing these suitors! Come on, my brave friend, stand by my side and watch how Mentor, son of Alcimus, fights your enemies and repays your kindness!"',
            'angrily. <others>"Odysseus,"</others> she said, <others>"your strength and prowess are not what they were when you fought the Trojans for nine long years for noble Helen! Back then, you killed countless enemies, and Priam\'s city fell because of your cunning plans. So why have you so lamentably lost your courage now? You are here in your own home, on your own land, facing these suitors! Come on, my brave friend, stand by my side and watch how Mentor, son of Alcimus, fights your enemies and repays your kindness!"</others>'
        ),
        # Line 57
        (
            'shouted to them, "Friends, he\'ll soon have to stop fighting! Mentor has left, doing nothing but bragging. They are standing at the doors with no support. Don\'t all aim at him at once. Instead, six of you throw your spears first. See if you can win glory by killing him! Once he falls, we won\'t need to worry about the others!"',
            'shouted to them, <others>"Friends, he\'ll soon have to stop fighting! Mentor has left, doing nothing but bragging. They are standing at the doors with no support. Don\'t all aim at him at once. Instead, six of you throw your spears first. See if you can win glory by killing him! Once he falls, we won\'t need to worry about the others!"</others>'
        ),
        # Line 59
        (
            'said to his men, "Friends, I think we\'d better throw our spears into their midst now! Otherwise, they\'ll finish all the harm they\'ve done to us by killing us outright!"',
            'said to his men, <odysseus>"Friends, I think we\'d better throw our spears into their midst now! Otherwise, they\'ll finish all the harm they\'ve done to us by killing us outright!"</odysseus>'
        ),
        # Line 63
        (
            'saying, "Foul-mouthed son of Polytherses, don\'t be so foolish as to curse wickedly another time! Let your words follow heaven\'s will, for the gods are much stronger than men. I give you this advice as a gift. It repays you for kicking Odysseus when he was begging in his own house!"',
            'saying, <others>"Foul-mouthed son of Polytherses, don\'t be so foolish as to curse wickedly another time! Let your words follow heaven\'s will, for the gods are much stronger than men. I give you this advice as a gift. It repays you for kicking Odysseus when he was begging in his own house!"</others>'
        ),
        # Line 67
        (
            'pleaded, "Lord Odysseus, please have mercy on me and spare my life! I never wronged any of the women in your household, either in word or deed. In fact, I tried to stop the others. I saw what they were doing, but they wouldn\'t listen to me. Now they are paying for their folly. I was their sacrificing priest. If you kill me, I will die without having done anything to deserve it. I will receive no thanks for all the good I tried to do."',
            'pleaded, <others>"Lord Odysseus, please have mercy on me and spare my life! I never wronged any of the women in your household, either in word or deed. In fact, I tried to stop the others. I saw what they were doing, but they wouldn\'t listen to me. Now they are paying for their folly. I was their sacrificing priest. If you kill me, I will die without having done anything to deserve it. I will receive no thanks for all the good I tried to do."</others>'
        ),
        # Line 69
        (
            'replied, "If you were their sacrificing priest, then you must have prayed many times that it would be a long time before I returned home. You must have prayed that you might marry my wife and have children by her. Therefore, you must die."',
            'replied, <odysseus>"If you were their sacrificing priest, then you must have prayed many times that it would be a long time before I returned home. You must have prayed that you might marry my wife and have children by her. Therefore, you must die."</odysseus>'
        ),
        # Line 73
        (
            'said, "Lord Odysseus, please have mercy on me and spare my life! If you kill a minstrel like me, who can sing for both gods and men, you will regret it later. I compose all my own songs, and heaven grants me all kinds of inspiration. I could sing to you as if you were a god! So please, don\'t be so quick to cut off my head. Your own son, Telemachus, will testify for me. I did not want to frequent your house and sing for the suitors after their meals. But they were too many and too strong; they forced me."',
            'said, <others>"Lord Odysseus, please have mercy on me and spare my life! If you kill a minstrel like me, who can sing for both gods and men, you will regret it later. I compose all my own songs, and heaven grants me all kinds of inspiration. I could sing to you as if you were a god! So please, don\'t be so quick to cut off my head. Your own son, Telemachus, will testify for me. I did not want to frequent your house and sing for the suitors after their meals. But they were too many and too strong; they forced me."</others>'
        ),
        # Line 75
        (
            'father. "Stop!" he cried. "This man is guiltless. Don\'t harm him. And let\'s spare Medon too. He was always good to me when I was a boy. Of course, that\'s assuming Philoetius or Eumaeus hasn\'t already killed him. Or that he hasn\'t fallen in your path while you were raging through the courtyard."',
            'father. <telemachus>"Stop!"</telemachus> he cried. <telemachus>"This man is guiltless. Don\'t harm him. And let\'s spare Medon too. He was always good to me when I was a boy. Of course, that\'s assuming Philoetius or Eumaeus hasn\'t already killed him. Or that he hasn\'t fallen in your path while you were raging through the courtyard."</telemachus>'
        ),
        # Line 79
        (
            '"Here I am, young master!" he said. "So please, stay your hand and speak to your father. Otherwise, he will kill me in his rage against the suitors. They wasted his wealth and were so foolishly disrespectful to you."',
            '<others>"Here I am, young master!"</others> he said. <others>"So please, stay your hand and speak to your father. Otherwise, he will kill me in his rage against the suitors. They wasted his wealth and were so foolishly disrespectful to you."</others>'
        ),
        # Line 81
        (
            'him. "Don\'t be afraid. Telemachus has spared your life. From now on, you\'ll see, and you can tell others, how much better good deeds turn out than bad ones. So, you and the bard, go out to the outer courtyard, away from this slaughter, while I finish my work here."',
            'him. <odysseus>"Don\'t be afraid. Telemachus has spared your life. From now on, you\'ll see, and you can tell others, how much better good deeds turn out than bad ones. So, you and the bard, go out to the outer courtyard, away from this slaughter, while I finish my work here."</odysseus>'
        ),
        # Line 85
        (
            'Telemachus. "Call Nurse Eurycleia. I have something to say to her."',
            'Telemachus. <odysseus>"Call Nurse Eurycleia. I have something to say to her."</odysseus>'
        ),
        # Line 87
        (
            'quarters. "Hurry out," he called. "You, the elder in charge of all the women in the house. Come outside; my father wants to speak with you."',
            'quarters. <telemachus>"Hurry out,"</telemachus> he called. <telemachus>"You, the elder in charge of all the women in the house. Come outside; my father wants to speak with you."</telemachus>'
        ),
        # Line 89
        (
            'stopped her. "Nurse," he said, "celebrate in silence. Control yourself and don\'t make a sound. It\'s wrong to gloat over the dead. Divine judgment and their own evil deeds brought these men to ruin. They disrespected everyone who came near them, rich or poor. They met a miserable end as punishment for their wickedness and foolishness. Now, tell me which of the women in the house behaved badly and which remained innocent."',
            'stopped her. <odysseus>"Nurse,"</odysseus> he said, <odysseus>"celebrate in silence. Control yourself and don\'t make a sound. It\'s wrong to gloat over the dead. Divine judgment and their own evil deeds brought these men to ruin. They disrespected everyone who came near them, rich or poor. They met a miserable end as punishment for their wickedness and foolishness. Now, tell me which of the women in the house behaved badly and which remained innocent."</odysseus>'
        ),
        # Line 91
        (
            '"I\'ll tell you the honest truth, my son," Eurycleia answered. "There are fifty women in this house whom we teach to card wool and do all sorts of housework. Of these, twelve have behaved improperly and were disrespectful to me and Queen Penelope. They showed no disrespect to young master Telemachus, because he has only recently grown, and the Queen never allowed him to give orders to the female servants. But I should go upstairs and tell your wife everything that has happened, for some god must have put her to sleep."',
            '<others>"I\'ll tell you the honest truth, my son,"</others> Eurycleia answered. <others>"There are fifty women in this house whom we teach to card wool and do all sorts of housework. Of these, twelve have behaved improperly and were disrespectful to me and Queen Penelope. They showed no disrespect to young master Telemachus, because he has only recently grown, and the Queen never allowed him to give orders to the female servants. But I should go upstairs and tell your wife everything that has happened, for some god must have put her to sleep."</others>'
        ),
        # Line 93
        (
            '"Don\'t wake the Queen yet," Odysseus replied. "Instead, tell the women who behaved badly to come to me."',
            '<odysseus>"Don\'t wake the Queen yet,"</odysseus> Odysseus replied. <odysseus>"Instead, tell the women who behaved badly to come to me."</odysseus>'
        ),
        # Line 95
        (
            'swineherd. "Begin," Odysseus said, "to clear away the dead, and make the women help you. Then, get sponges and clean water to scrub down the tables and chairs. After you\'ve thoroughly cleaned the entire hall, take those women into the space between the domed room and the outer courtyard wall. Then, stab them with your swords until they are completely dead, until they forget all their secret affairs with the suitors."',
            'swineherd. <odysseus>"Begin,"</odysseus> Odysseus said, <odysseus>"to clear away the dead, and make the women help you. Then, get sponges and clean water to scrub down the tables and chairs. After you\'ve thoroughly cleaned the entire hall, take those women into the space between the domed room and the outer courtyard wall. Then, stab them with your swords until they are completely dead, until they forget all their secret affairs with the suitors."</odysseus>'
        ),
        # Line 97
        (
            'two, "I won\'t let these women have an easy death. They were disrespectful to me and my mother, and they slept with the suitors."',
            'two, <telemachus>"I won\'t let these women have an easy death. They were disrespectful to me and my mother, and they slept with the suitors."</telemachus>'
        ),
        # Line 103
        (
            'Eurycleia, "Bring me sulfur, which cleanses all impurities, and fetch fire also, so I may burn it and purify these halls. Go, moreover, and tell Penelope to come here with her ladies-in-waiting, and call all the other maidservants that are in the house."',
            'Eurycleia, <odysseus>"Bring me sulfur, which cleanses all impurities, and fetch fire also, so I may burn it and purify these halls. Go, moreover, and tell Penelope to come here with her ladies-in-waiting, and call all the other maidservants that are in the house."</odysseus>'
        ),
        # Line 105
        (
            '"Everything you\'ve said is true," Eurycleia answered, "but let me bring you some fresh clothes—a shirt and cloak. You shouldn\'t wear these tattered rags any longer. It\'s not proper."',
            '<others>"Everything you\'ve said is true,"</others> Eurycleia answered, <others>"but let me bring you some fresh clothes—a shirt and cloak. You shouldn\'t wear these tattered rags any longer. It\'s not proper."</others>'
        ),
        # Line 107
        (
            '"First, light the fire," replied Odysseus.',
            '<odysseus>"First, light the fire,"</odysseus> replied Odysseus.'
        )
    ]
    
    modified = content
    for target, replacement in replacements:
        if target not in modified:
            print(f"ERROR: Target string not found:\n{target[:100]}...")
            return
        modified = modified.replace(target, replacement)
        
    os.makedirs(output_dir, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(modified)
        
    print("Tagged file written successfully.")
    
    # Verification
    stripped = modified
    for tag in ["<odysseus>", "</odysseus>", "<telemachus>", "</telemachus>", "<others>", "</others>"]:
        stripped = stripped.replace(tag, "")
        
    if stripped == content:
        print("VERIFICATION SUCCESSFUL: Stripped text matches original character-for-character.")
    else:
        print("VERIFICATION FAILED! Differences found.")

if __name__ == "__main__":
    tag_dialogue()
