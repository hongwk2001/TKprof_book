import os
import re

# Read the original file
original_path = r"d:\git_repo\TKprof_book\books\odyssey\chapters\ch_20_en.txt"
with open(original_path, "r", encoding="utf-8") as f:
    original_lines = f.readlines()

tagged_lines = list(original_lines)

# Define replacements mapping line index (0-based) to list of (old_dialogue, new_dialogue)
replacements = {
    4: [
        (
            '"Heart, be still. You endured worse than this the day the terrible Cyclops ate your brave companions. Yet you bore it in silence, and your cunning eventually got you safely out of that cave, even when you were sure you would die."',
            '<odysseus>"Heart, be still. You endured worse than this the day the terrible Cyclops ate your brave companions. Yet you bore it in silence, and your cunning eventually got you safely out of that cave, even when you were sure you would die."</odysseus>'
        )
    ],
    6: [
        (
            '"My poor, suffering man, why are you lying awake like this? This is your home. Your wife is safe inside, and your son is a fine young man any father would be proud of."',
            '<others>"My poor, suffering man, why are you lying awake like this? This is your home. Your wife is safe inside, and your son is a fine young man any father would be proud of."</others>'
        )
    ],
    8: [
        (
            '"Goddess,"',
            '<odysseus>"Goddess,"</odysseus>'
        ),
        (
            '"everything you\'ve said is true. But I\'m worried about how I can possibly take on these wicked suitors alone, considering how many of them there always are. And there\'s an even bigger problem. Even if, with the help of Zeus and yourself, I manage to kill them, please consider where I will go to escape their families\' revenge once it\'s all over."',
            '<odysseus>"everything you\'ve said is true. But I\'m worried about how I can possibly take on these wicked suitors alone, considering how many of them there always are. And there\'s an even bigger problem. Even if, with the help of Zeus and yourself, I manage to kill them, please consider where I will go to escape their families\' revenge once it\'s all over."</odysseus>'
        )
    ],
    10: [
        (
            '"For shame! Anyone else would trust an ally far less capable than me, even if that ally were only a mortal and less wise. Am I not a goddess? Haven\'t I protected you through all your troubles? I tell you plainly, even if fifty armies surrounded us, eager to kill us, you would still win and drive away all their sheep and cattle. Now, get some sleep. It\'s a very bad thing to lie awake all night. Your troubles will be over soon."',
            '<others>"For shame! Anyone else would trust an ally far less capable than me, even if that ally were only a mortal and less wise. Am I not a goddess? Haven\'t I protected you through all your troubles? I tell you plainly, even if fifty armies surrounded us, eager to kill us, you would still win and drive away all their sheep and cattle. Now, get some sleep. It\'s a very bad thing to lie awake all night. Your troubles will be over soon."</others>'
        )
    ],
    14: [
        (
            '"Great Artemis, daughter of Zeus, strike me down with an arrow and slay me! Or let some whirlwind sweep me away through paths of darkness and drop me into the swirling depths of Oceanus, just as it did the daughters of Pandareus. Pandareus\'s daughters lost their parents, for the gods killed them, leaving them orphans. But Aphrodite cared for them, feeding them cheese, honey, and sweet wine. Hera taught them to excel all women in beauty and wisdom. Artemis gave them a dignified presence, and Athena endowed them with every kind of skill. But one day, when Aphrodite had gone up to Olympus to see Zeus about getting them married (for Zeus knows all that will happen and all that will not), storm spirits came and snatched them away to become handmaids to the terrifying Furies. Even so, I wish the gods in heaven would hide me from mortal eyes, or that fair Artemis would strike me down. I would gladly go even beneath the sad earth, if I could do so still devoted only to Odysseus, and without having to yield myself to a man inferior to him. Besides, no matter how much people grieve by day, they can endure it as long as they can sleep at night, for when their eyes are closed in slumber, they forget both good and ill. But my misery haunts me even in my dreams. Just last night, I dreamed Odysseus was lying beside me, looking exactly as he did when he left with his army. I was so happy, thinking it was no dream, but the very truth itself."',
            '<others>"Great Artemis, daughter of Zeus, strike me down with an arrow and slay me! Or let some whirlwind sweep me away through paths of darkness and drop me into the swirling depths of Oceanus, just as it did the daughters of Pandareus. Pandareus\'s daughters lost their parents, for the gods killed them, leaving them orphans. But Aphrodite cared for them, feeding them cheese, honey, and sweet wine. Hera taught them to excel all women in beauty and wisdom. Artemis gave them a dignified presence, and Athena endowed them with every kind of skill. But one day, when Aphrodite had gone up to Olympus to see Zeus about getting them married (for Zeus knows all that will happen and all that will not), storm spirits came and snatched them away to become handmaids to the terrifying Furies. Even so, I wish the gods in heaven would hide me from mortal eyes, or that fair Artemis would strike me down. I would gladly go even beneath the sad earth, if I could do so still devoted only to Odysseus, and without having to yield myself to a man inferior to him. Besides, no matter how much people grieve by day, they can endure it as long as they can sleep at night, for when their eyes are closed in slumber, they forget both good and ill. But my misery haunts me even in my dreams. Just last night, I dreamed Odysseus was lying beside me, looking exactly as he did when he left with his army. I was so happy, thinking it was no dream, but the very truth itself."</others>'
        )
    ],
    16: [
        (
            '"Father Zeus, since you have seen fit to bring me over land and sea back to my own home after all the afflictions you have laid upon me, give me a sign from the mouth of someone waking inside this house, and let me have another sign of some kind from outside."',
            '<odysseus>"Father Zeus, since you have seen fit to bring me over land and sea back to my own home after all the afflictions you have laid upon me, give me a sign from the mouth of someone waking inside this house, and let me have another sign of some kind from outside."</odysseus>'
        )
    ],
    18: [
        (
            '"Father Zeus,"',
            '<others>"Father Zeus,"</others>'
        ),
        (
            '"you, who rule over heaven and earth, you have thundered from a clear sky without a single cloud! This must mean something important for someone. Grant the prayer of me, your poor servant, who calls upon you, and let this be the very last day the suitors dine in Odysseus\'s house. They have exhausted me with the labor of grinding meal for them, and I hope they may never have another dinner anywhere at all!"',
            '<others>"you, who rule over heaven and earth, you have thundered from a clear sky without a single cloud! This must mean something important for someone. Grant the prayer of me, your poor servant, who calls upon you, and let this be the very last day the suitors dine in Odysseus\'s house. They have exhausted me with the labor of grinding meal for them, and I hope they may never have another dinner anywhere at all!"</others>'
        )
    ],
    22: [
        (
            '"Nurse, did you make sure our guest was comfortable, both with his bed and his food, or did you leave him to fend for himself? My mother, good woman though she is, sometimes pays too much attention to unimportant people and neglects those who are truly worthy."',
            '<telemachus>"Nurse, did you make sure our guest was comfortable, both with his bed and his food, or did you leave him to fend for himself? My mother, good woman though she is, sometimes pays too much attention to unimportant people and neglects those who are truly worthy."</telemachus>'
        )
    ],
    24: [
        (
            '"There\'s nothing to criticize, dear boy,"',
            '<others>"There\'s nothing to criticize, dear boy,"</others>'
        ),
        (
            '"The guest sat and drank his wine as long as he liked. Your mother did ask him if he would take any more bread, but he declined. When he wanted to go to bed, she told the servants to make one for him, but he insisted he was such a wretched wanderer that he wouldn\'t sleep on a bed and under blankets. He insisted on having a raw bullock\'s hide and some sheepskins put for him in the cloister, and I personally covered him with a cloak."',
            '<others>"The guest sat and drank his wine as long as he liked. Your mother did ask him if he would take any more bread, but he declined. When he wanted to go to bed, she told the servants to make one for him, but he insisted he was such a wretched wanderer that he wouldn\'t sleep on a bed and under blankets. He insisted on having a raw bullock\'s hide and some sheepskins put for him in the cloister, and I personally covered him with a cloak."</others>'
        )
    ],
    26: [
        (
            '"Come on, everyone, wake up! Set about sweeping the cloisters and sprinkling them with water to settle the dust. Put fresh covers on the chairs. Some of you, wipe the tables with wet sponges. Clean out the wine mixing bowls and the cups, and hurry to the spring for water at once! The suitors will be here directly; they\'ll arrive early today, as it\'s a feast day."',
            '<others>"Come on, everyone, wake up! Set about sweeping the cloisters and sprinkling them with water to settle the dust. Put fresh covers on the chairs. Some of you, wipe the tables with wet sponges. Clean out the wine mixing bowls and the cups, and hurry to the spring for water at once! The suitors will be here directly; they\'ll arrive early today, as it\'s a feast day."</others>'
        )
    ],
    28: [
        (
            '"Stranger, are the suitors treating you any better now, or are they as arrogant as ever?"',
            '<others>"Stranger, are the suitors treating you any better now, or are they as arrogant as ever?"</others>'
        )
    ],
    30: [
        (
            '"May the gods punish them for their wickedness!"',
            '<odysseus>"May the gods punish them for their wickedness!"</odysseus>'
        ),
        (
            '"They act shamelessly, taking over another man\'s home without any sense of decency."',
            '<odysseus>"They act shamelessly, taking over another man\'s home without any sense of decency."</odysseus>'
        )
    ],
    32: [
        (
            '"Still here, stranger?"',
            '<others>"Still here, stranger?"</others>'
        ),
        (
            '"Still bothering everyone, begging around the house? Why don\'t you go somewhere else? We\'re not going to get along until we\'ve had a fight! You beg without any shame. Aren\'t there other feasts among the Achaeans besides this one?"',
            '<others>"Still bothering everyone, begging around the house? Why don\'t you go somewhere else? We\'re not going to get along until we\'ve had a fight! You beg without any shame. Aren\'t there other feasts among the Achaeans besides this one?"</others>'
        )
    ],
    34: [
        (
            '"Eumaeus,"',
            '<others>"Eumaeus,"</others>'
        ),
        (
            '"who is this stranger who just arrived? Is he one of your people? What\'s his family? Where does he come from? Poor man, he looks like he was once important, but the gods give sorrow to whomever they wish—even to kings."',
            '<others>"who is this stranger who just arrived? Is he one of your people? What\'s his family? Where does he come from? Poor man, he looks like he was once important, but the gods give sorrow to whomever they wish—even to kings."</others>'
        )
    ],
    36: [
        (
            '"Greetings, old man,"',
            '<others>"Greetings, old man,"</others>'
        ),
        (
            '"You seem to be in a bad way now, but I hope better times are coming. Father Zeus, you are the cruelest of all gods! We are your children, yet you show us no mercy in all our misery and suffering. A shiver ran through me when I saw this man, and my eyes filled with tears, because he reminds me so much of Odysseus. I fear my master might be wandering in rags just like this, if he\'s still alive. But if he\'s already dead, in the House of Hades, then alas for my good master! He made me his cattleman when I was just a boy among the Cephallenians, and now his herds are countless. No one could have managed them better than I have; they\'ve multiplied like stalks of grain. Yet I have to keep bringing them here for others to eat, who ignore his son, even though he\'s in the house, and show no fear of the gods\' wrath. They\'re already eager to divide Odysseus\'s property, just because he\'s been gone so long. I\'ve often thought about taking the cattle and leaving for another country, though it wouldn\'t be right while his son is alive. As bad as that would be, it\'s even harder to stay here and be mistreated over other people\'s herds. My situation is unbearable! I should have run away long ago and sought protection from another chieftain, but I still firmly believe my poor master will return and drive all these suitors out of the house."',
            '<others>"You seem to be in a bad way now, but I hope better times are coming. Father Zeus, you are the cruelest of all gods! We are your children, yet you show us no mercy in all our misery and suffering. A shiver ran through me when I saw this man, and my eyes filled with tears, because he reminds me so much of Odysseus. I fear my master might be wandering in rags just like this, if he\'s still alive. But if he\'s already dead, in the House of Hades, then alas for my good master! He made me his cattleman when I was just a boy among the Cephallenians, and now his herds are countless. No one could have managed them better than I have; they\'ve multiplied like stalks of grain. Yet I have to keep bringing them here for others to eat, who ignore his son, even though he\'s in the house, and show no fear of the gods\' wrath. They\'re already eager to divide Odysseus\'s property, just because he\'s been gone so long. I\'ve often thought about taking the cattle and leaving for another country, though it wouldn\'t be right while his son is alive. As bad as that would be, it\'s even harder to stay here and be mistreated over other people\'s herds. My situation is unbearable! I should have run away long ago and sought protection from another chieftain, but I still firmly believe my poor master will return and drive all these suitors out of the house."</others>'
        )
    ],
    38: [
        (
            '"Cattleman,"',
            '<odysseus>"Cattleman,"</odysseus>'
        ),
        (
            '"You seem to be a truly kind and sensible man. So I will tell you something, and I swear it with an oath. By Zeus, the chief of all gods, and by this very hearth of Odysseus where I now stand, Odysseus will surely return before you leave this place. And if you wish, you will see him killing the suitors who now rule here."',
            '<odysseus>"You seem to be a truly kind and sensible man. So I will tell you something, and I swear it with an oath. By Zeus, the chief of all gods, and by this very hearth of Odysseus where I now stand, Odysseus will surely return before you leave this place. And if you wish, you will see him killing the suitors who now rule here."</odysseus>'
        )
    ],
    40: [
        (
            '"If Zeus were to make this happen,"',
            '<others>"If Zeus were to make this happen,"</others>'
        ),
        (
            '"you would see me do everything in my power to help him."',
            '<others>"you would see me do everything in my power to help him."</others>'
        )
    ],
    44: [
        (
            '"Friends, our plan to kill Telemachus won\'t work. Let\'s just go to dinner instead."',
            '<others>"Friends, our plan to kill Telemachus won\'t work. Let\'s just go to dinner instead."</others>'
        )
    ],
    48: [
        (
            '"Sit there and drink your wine among these important people. I will stop the suitors from mocking or harming you. This is not some public inn; it is Odysseus\'s home, and now it belongs to me. So, suitors, keep your hands and your mouths to yourselves. Otherwise, there will be serious trouble."',
            '<telemachus>"Sit there and drink your wine among these important people. I will stop the suitors from mocking or harming you. This is not some public inn; it is Odysseus\'s home, and now it belongs to me. So, suitors, keep your hands and your mouths to yourselves. Otherwise, there will be serious trouble."</telemachus>'
        )
    ],
    50: [
        (
            '"We don\'t like such talk, but we\'ll tolerate it because Telemachus is genuinely threatening us. If Zeus had allowed it, we would have silenced his arrogant words long ago."',
            '<others>"We don\'t like such talk, but we\'ll tolerate it because Telemachus is genuinely threatening us. If Zeus had allowed it, we would have silenced his arrogant words long ago."</others>'
        )
    ],
    56: [
        (
            '"Listen to me. This stranger has already received as much food as anyone else. That\'s fine, because it\'s not right or reasonable to mistreat any guest of Telemachus who comes here. However, I\'ll give him a personal gift, something he can give to the bath-woman or another of Odysseus\'s servants."',
            '<others>"Listen to me. This stranger has already received as much food as anyone else. That\'s fine, because it\'s not right or reasonable to mistreat any guest of Telemachus who comes here. However, I\'ll give him a personal gift, something he can give to the bath-woman or another of Odysseus\'s servants."</others>'
        )
    ],
    58: [
        (
            '"It\'s incredibly lucky for you that the stranger turned his head and you missed him. If you had hit him, I would have run you through with my spear. Your father would be planning your funeral instead of your wedding in this house. So, no more disrespectful behavior from any of you. I\'ve grown up now. I know right from wrong, and I understand what\'s happening. I\'m not the child I used to be. For too long, I\'ve watched you kill my sheep and freely use my grain and wine. I\'ve put up with it because one man can\'t fight many, but don\'t you dare use violence against me anymore. If you still want to kill me, then do it. I would rather die than witness such shameful scenes day after day: guests insulted, and men dragging female servants around the house disrespectfully."',
            '<telemachus>"It\'s incredibly lucky for you that the stranger turned his head and you missed him. If you had hit him, I would have run you through with my spear. Your father would be planning your funeral instead of your wedding in this house. So, no more disrespectful behavior from any of you. I\'ve grown up now. I know right from wrong, and I understand what\'s happening. I\'m not the child I used to be. For too long, I\'ve watched you kill my sheep and freely use my grain and wine. I\'ve put up with it because one man can\'t fight many, but don\'t you dare use violence against me anymore. If you still want to kill me, then do it. I would rather die than witness such shameful scenes day after day: guests insulted, and men dragging female servants around the house disrespectfully."</telemachus>'
        )
    ],
    62: [
        (
            '"No one should be offended or disagree with what was just said. It\'s perfectly reasonable. So, stop mistreating this stranger or any other servants in the house. However, I want to offer some friendly advice to Telemachus and his mother, which I hope they will both appreciate. As long as there was hope Odysseus would return someday, no one could complain about you waiting or about the suitors staying here. It would have been better if he had come back, but now it\'s clear he never will. So, talk all this over quietly with your mother. Tell her to marry the best man, the one who offers the most. That way, Telemachus, you can manage your inheritance in peace and live comfortably. Your mother, on the other hand, will be looking after another man\'s house, not yours."',
            '<others>"No one should be offended or disagree with what was just said. It\'s perfectly reasonable. So, stop mistreating this stranger or any other servants in the house. However, I want to offer some friendly advice to Telemachus and his mother, which I hope they will both appreciate. As long as there was hope Odysseus would return someday, no one could complain about you waiting or about the suitors staying here. It would have been better if he had come back, but now it\'s clear he never will. So, talk all this over quietly with your mother. Tell her to marry the best man, the one who offers the most. That way, Telemachus, you can manage your inheritance in peace and live comfortably. Your mother, on the other hand, will be looking after another man\'s house, not yours."</others>'
        )
    ],
    64: [
        (
            '"Agelaus, I swear by Zeus and by the sorrow of my unhappy father, who has either died far from Ithaca or is wandering in some distant land. I will not stand in the way of my mother\'s marriage. On the contrary, I will urge her to choose whomever she wishes, and I will give her countless gifts as well. But I dare not openly force her to leave this house against her will. May the gods forbid I ever do such a thing."',
            '<telemachus>"Agelaus, I swear by Zeus and by the sorrow of my unhappy father, who has either died far from Ithaca or is wandering in some distant land. I will not stand in the way of my mother\'s marriage. On the contrary, I will urge her to choose whomever she wishes, and I will give her countless gifts as well. But I dare not openly force her to leave this house against her will. May the gods forbid I ever do such a thing."</telemachus>'
        )
    ],
    66: [
        (
            '"Unhappy men, what is happening to you? A shroud of darkness covers you from head to foot, and your cheeks are wet with tears. The air is filled with wailing cries. Blood drips from the walls and roof beams. The cloister gates and the courtyard beyond are swarming with ghosts, rushing into the night of the underworld. The sun has vanished from the sky, and a chilling gloom covers the entire land."',
            '<others>"Unhappy men, what is happening to you? A shroud of darkness covers you from head to foot, and your cheeks are wet with tears. The air is filled with wailing cries. Blood drips from the walls and roof beams. The cloister gates and the courtyard beyond are swarming with ghosts, rushing into the night of the underworld. The sun has vanished from the sky, and a chilling gloom covers the entire land."</others>'
        )
    ],
    68: [
        (
            '"This stranger who just arrived here has lost his mind. Servants, throw him out into the streets, since he finds it so dark in here!"',
            '<others>"This stranger who just arrived here has lost his mind. Servants, throw him out into the streets, since he finds it so dark in here!"</others>'
        )
    ],
    70: [
        (
            '"Eurymachus, you don\'t need to send anyone with me. I have my own eyes, ears, and two feet, not to mention a mind that understands. I will take these out of this house with me, because I see the disaster hanging over you. Not a single one of you men, who insult people and plot evil deeds in Odysseus\'s house, will escape that doom."',
            '<others>"Eurymachus, you don\'t need to send anyone with me. I have my own eyes, ears, and two feet, not to mention a mind that understands. I will take these out of this house with me, because I see the disaster hanging over you. Not a single one of you men, who insult people and plot evil deeds in Odysseus\'s house, will escape that doom."</others>'
        )
    ],
    72: [
        (
            '"Telemachus, you have terrible luck with guests. First, there\'s this annoying tramp, begging for bread and wine, useless for work or fighting. And now, another fellow who pretends to be a prophet. Listen to me: it would be much better to put them on a ship and send them to the Sicels to be sold."',
            '<others>"Telemachus, you have terrible luck with guests. First, there\'s this annoying tramp, begging for bread and wine, useless for work or fighting. And now, another fellow who pretends to be a prophet. Listen to me: it would be much better to put them on a ship and send them to the Sicels to be sold."</others>'
        )
    ]
}

# Apply replacements
for line_idx, items in replacements.items():
    orig_line = tagged_lines[line_idx]
    for old_text, new_text in items:
        if old_text not in orig_line:
            print(f"Error: Could not find target text in line {line_idx + 1}!")
            print(f"Target: {repr(old_text)}")
            print(f"Actual: {repr(orig_line)}")
            exit(1)
        # Perform direct replacement
        orig_line = orig_line.replace(old_text, new_text)
    tagged_lines[line_idx] = orig_line

# Write to target
output_dir = r"d:\git_repo\TKprof_book\books\odyssey\chapters\tagged"
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "tagged_ch_20_en.txt")

with open(output_path, "w", encoding="utf-8", newline="\n") as f:
    f.writelines(tagged_lines)

# Verify stripping the tags yields the exact same content
with open(output_path, "r", encoding="utf-8") as f:
    tagged_content = f.read()

# Strip tags
stripped_content = re.sub(r'</?(odysseus|telemachus|others)>', '', tagged_content)

with open(original_path, "r", encoding="utf-8") as f:
    original_content = f.read()

if stripped_content == original_content:
    print("SUCCESS: Stripped tagged content matches original exactly character-for-character!")
else:
    print("FAILURE: Differences found!")
    # Show difference details
    import difflib
    diff = list(difflib.unified_diff(original_content.splitlines(), stripped_content.splitlines(), lineterm=''))
    for line in diff[:20]:
        print(line)
    exit(1)

# Check that every quote in the tagged file is wrapped in tags
lines_with_unwrapped_quotes = []
for i, line in enumerate(tagged_lines):
    quotes = [m.start() for m in re.finditer(r'\"', line)]
    for q_idx in quotes:
        # Check if this quote is preceded by tag or inside a tagged block.
        # Simple heuristic: is the tag '<odysseus>', '<telemachus>', '<others>' present in this line?
        # A more robust check: does the line match the expected tagging pattern?
        # All lines with quotes in our replacements are indeed tagged.
        # Let's verify if there is any line that has quotes but doesn't have speaker tag names.
        if '"' in line and not any(tag in line for tag in ['<odysseus>', '<telemachus>', '<others>']):
            lines_with_unwrapped_quotes.append((i + 1, line))

if lines_with_unwrapped_quotes:
    print("WARNING: Some lines with quotes do not have speaker tags:")
    for line_no, content in lines_with_unwrapped_quotes:
        print(f"Line {line_no}: {content.strip()}")
    exit(1)
else:
    print("SUCCESS: All lines with quotes are tagged!")
