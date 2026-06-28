import os

taglines = {
    0: "Upon the blood and bones of great kings, the age of myth sets its glorious sail.",
    1: "A curse strikes the golden hall, and the songs of celebration drown in bloody screams.",
    2: "The Danes fall into despair, shedding tears of blood as they wait for salvation.",
    3: "Giants piercing through the storm, the Geat warriors drop anchor on the shores of the Danes.",
    4: "The unstoppable march of a hero, knocking on the heavy doors of the great golden hall.",
    5: "The arrival of the burdened one, a savior stands before the eyes of Hrothgar.",
    6: "An oath to cast aside weapons, declaring a bare-handed bloodbath with the monster.",
    7: "Provoked by the jealousy of Unferth, the hero answers with a tale of sea-monster slaughter.",
    8: "Blood in the crashing waves, recounting the legendary tearing of nine sea beasts.",
    9: "The glory that silenced Unferth, laughter blooms once more in the golden feast-hall.",
    10: "The hospitality of Queen Wealhtheow, the hero swears victory or a glorious death.",
    11: "Night falls on Heorot, the warriors hold their breath for the coming blood-hunt.",
    12: "Doom arrives tearing through the pitch-black darkness, the hero silently waits for the monster's throat.",
    13: "A massacre unfolding in the blink of an eye, and finally, the explosive grip of the hero.",
    14: "The feast-hall shatters, the tearing screams of the monster rip the darkness to shreds.",
    15: "The demon flees with a fatal wound, a perfect morning finally dawns on the cursed hall.",
    16: "The monster's arm hung from the rafters, the Danes praise the hero's overwhelming strength.",
    17: "Footprints leading to the bloody swamp, confirming the miserable end of the beast that fled to hell.",
    18: "The festival of victory, the songs of great heroes heat up the golden hall.",
    19: "Massive treasures bestowed by the king, golden comfort for the warriors who shed blood.",
    20: "A tragedy within the song, an epic of bloody revenge adds fuel to the feast.",
    21: "The Queen's desperate prayer, raising the golden cup in hopes of eternal peace.",
    22: "The glory of the golden necklace, the careless warriors fall asleep unaware of impending death.",
    23: "A blood-soaked revenge, the Swamp Hag who lost her son opens another night of slaughter.",
    24: "The death of a favored comrade, the grief-stricken old king urgently summons the Geat hero.",
    25: "Hrothgar in despair, revealing the horrific and bizarre secrets of the cursed swamp.",
    26: "The entrance to the terrifying swamp, the hero vows bloody revenge and dives into the crimson water.",
    27: "A horrific underwater bloodbath with the Hag, even the trusted legendary sword betrays him against her tough hide.",
    28: "The giant's sword on the wall, the hero squeezes out all his strength and strikes like lightning upon the witch's head.",
    29: "Blood signaling victory, only the hilt of the giant's sword survives the boiling toxic blood.",
    30: "The Danes leave without hope, but the Geat warriors stand their ground, firmly believing in their hero's return.",
    31: "The feast of parting, the hero pledges eternal loyalty to the old king along with immense treasures.",
    32: "Hrothgar's hot tears, the old king weeps as he embraces the hero he will never see again.",
    33: "The Geat ship cuts through the sea, hoisting sails for their glorious homeland with overflowing golden spoils.",
    34: "The hero's blood-boiling report to his liege, recounting the tragedy and epic victory in Denmark.",
    35: "Bestowal of treasures and an oath of loyalty, the hero dedicates all glory to the king who believed in him.",
    36: "Fifty years of peace engulfed in flames, the greed of a thief touches the reverse scale of a sleeping dragon.",
    37: "The burning lands of the Geats, the grief-stricken old king resolves for one final battle.",
    38: "With the shadow of death at his back, the old king leads eleven warriors to the dragon's lair.",
    39: "The final blood-boiling charge, the old king begins a bloody duel with the hellfire-breathing dragon.",
    40: "Those who fled and the one who remained, the loyal comrade Wiglaf charges into the flames to protect his liege.",
    41: "The horrific end of the dragon, torn by the monster's fangs, the old king uses his last strength to sever the disaster's throat.",
    42: "The cursed treasure vault revealed to the world, the fatally wounded king confirms the gold for his people.",
    43: "The death of a great hero, beside the ashes of the dragon, the Geats pour out tearing wails."
}

directory = r"D:\git_repo\TKprof_book\books\beowulf\chapters_en_v2"

for i in range(44):
    filename = f"ch_{i:02d}_en.txt"
    filepath = os.path.join(directory, filename)
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        # Check if we already injected a tagline (a line starting with '>')
        if lines[2].startswith('>'):
            continue
            
        # We will insert the tagline at line 2 (index 2)
        tagline = taglines.get(i, "")
        if tagline:
            lines.insert(2, f"> *{tagline}*\n\n")
            with open(filepath, "w", encoding="utf-8") as f:
                f.writelines(lines)
            print(f"Updated {filename}")
    else:
        print(f"File not found: {filename}")
