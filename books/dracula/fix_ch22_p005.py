def fix_ch22_p005():
    filepath = 'chapters/ch22_en.txt'
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    # Find the broken split: "When Dr.\n\n[P005b] Van Helsing asked if he had heard multiple \"voices\" or just a single \"voice,\" the orderly replied that he couldn't be certain."
    old_block = """[P005a] Dr. Seward asked the orderly who was on duty in the hallway if he had heard anything. The orderly confessed that he had been sitting down and dozing off, but was awakened by loud voices in the room. He then heard Renfield loudly shout, "God! God! God!" several times. After that, there was the sound of a heavy fall, and when he entered the room, he found Renfield lying face down on the floor, exactly as the doctors had discovered him. When Dr.

[P005b] Van Helsing asked if he had heard multiple "voices" or just a single "voice," the orderly replied that he couldn't be certain. Initially, it sounded like two people, but since no one else was in the room, he assumed it must have been only one. He stated he could swear under oath, if necessary, that the patient was the one who spoke the word "God." Once we were alone, Dr. Seward told us that he did not want to investigate the matter any further."""

    new_block = """[P005a] Dr. Seward asked the orderly who was on duty in the hallway if he had heard anything. The orderly confessed that he had been sitting down and dozing off, but was awakened by loud voices in the room. He then heard Renfield loudly shout, "God! God! God!" several times. After that, there was the sound of a heavy fall, and when he entered the room, he found Renfield lying face down on the floor, exactly as the doctors had discovered him. When Dr. Van Helsing asked if he had heard multiple "voices" or just a single "voice," the orderly replied that he couldn't be certain.

[P005b] Initially, it sounded like two people, but since no one else was in the room, he assumed it must have been only one. He stated he could swear under oath, if necessary, that the patient was the one who spoke the word "God." Once we were alone, Dr. Seward told us that he did not want to investigate the matter any further."""

    if old_block in text:
        text = text.replace(old_block, new_block)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(text)
        print("Successfully fixed P005a and P005b split in ch22_en.txt!")
    else:
        print("Could not find exact old_block, checking text search...")

if __name__ == '__main__':
    fix_ch22_p005()
