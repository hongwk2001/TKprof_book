import os

base_dir = r"d:\git_repo\TKprof_book\books\beowulf\chapters"

mapping = {
    "ch_00_en.txt": "Prologue: The First King, Scyld Scefing",
    "ch_01_en.txt": "Chapter One: The Great Hall, Heorot and the Monster, Grendel",
    "ch_02_en.txt": "Chapter Two: The Terror of Grendel and the Sorrow of King Hrothgar",
    "ch_03_en.txt": "Chapter Three: The Hero of Geatland, Beowulf",
    "ch_04_en.txt": "Chapter Four: The Danish Coast-Guard and the Arrival of Beowulf",
    "ch_05_en.txt": "Chapter Five: The King's Herald, Wulfgar",
    "ch_06_en.txt": "Chapter Six: The Meeting with King Hrothgar",
    "ch_07_en.txt": "Chapter Seven: Beowulf's Pledge to Fight Grendel",
    "ch_08_en.txt": "Chapter Eight: Hrothgar's Past and the Feast at Heorot",
    "ch_09_en.txt": "Chapter Nine: The Jealous Courtier, Unferth",
    "ch_10_en.txt": "Chapter Ten: Beowulf's Swimming Contest with Breca",
    "ch_11_en.txt": "Chapter Eleven: Queen Wealhtheow and the Night Watch",
    "ch_12_en.txt": "Chapter Twelve: The Attack of Grendel",
    "ch_13_en.txt": "Chapter Thirteen: The Battle in the Hall",
    "ch_14_en.txt": "Chapter Fourteen: The Victory and Grendel's Torn Arm",
    "ch_15_en.txt": "Chapter Fifteen: The Defeat of Grendel",
    "ch_16_en.txt": "Chapter Sixteen: The Song of the Singer, Sigemund",
    "ch_17_en.txt": "Chapter Seventeen: King Heremod and Hrothgar's Praise",
    "ch_18_en.txt": "Chapter Eighteen: Hrothgar's Victory Gifts",
    "ch_19_en.txt": "Chapter Nineteen: The Great Feast and the Story of Finn",
    "ch_20_en.txt": "Chapter Twenty: The Story of Finn, Hengest and Hildeburh",
    "ch_21_en.txt": "Chapter Twenty-One: Queen Wealhtheow's Plea for Her Sons",
    "ch_22_en.txt": "Chapter Twenty-Two: The Golden Collar and the Sleepers",
    "ch_23_en.txt": "Chapter Twenty-Three: The Revenge of Grendel's Mother",
    "ch_24_en.txt": "Chapter Twenty-Four: The Death of Aeschere and the Swamp of Monsters",
    "ch_25_en.txt": "Chapter Twenty-Five: Beowulf's Promise to Hunt the Hag",
    "ch_26_en.txt": "Chapter Twenty-Six: The Giant Sword and the Swim to the Cave",
    "ch_27_en.txt": "Chapter Twenty-Seven: The Underwater Battle and the Melted Blade",
    "ch_28_en.txt": "Chapter Twenty-Eight: The Return to the Surface with Grendel's Head",
    "ch_29_en.txt": "Chapter Twenty-Nine: The Presentation of the Trophies",
    "ch_30_en.txt": "Chapter Thirty: Hrothgar's Sermon on Pride",
    "ch_31_en.txt": "Chapter Thirty-One: The Farewell Feast",
    "ch_32_en.txt": "Chapter Thirty-Two: The Departure and Hrothgar's Tears",
    "ch_33_en.txt": "Chapter Thirty-Three: The Return to Geatland and the Tale of Modthryth",
    "ch_34_en.txt": "Chapter Thirty-Four: Beowulf's Report to King Hygelac",
    "ch_35_en.txt": "Chapter Thirty-Five: The Geatish Feud and the Gifts of Treasure",
    "ch_36_en.txt": "Chapter Thirty-Six: The Fifty-Year Reign and the Dragon's Fire",
    "ch_37_en.txt": "Chapter Thirty-Seven: Beowulf's Grief and the Eleven Companions",
    "ch_38_en.txt": "Chapter Thirty-Eight: The March to the Barrow",
    "ch_39_en.txt": "Chapter Thirty-Nine: Beowulf's Last Battle",
    "ch_40_en.txt": "Chapter Forty: The Loyal Companion, Wiglaf",
    "ch_41_en.txt": "Chapter Forty-One: The Death of the Dragon",
    "ch_42_en.txt": "Chapter Forty-Two: The Treasure Hoard Revealed",
    "ch_43_en.txt": "Chapter Forty-Three: Beowulf's Death and the Mourning of the Geats",
}

for filename, new_title in mapping.items():
    filepath = os.path.join(base_dir, filename)
    if os.path.exists(filepath):
        # Read content
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            lines = f.readlines()
        
        if lines:
            old_title = lines[0].strip()
            lines[0] = new_title + "\n"
            
            # Write back
            with open(filepath, 'w', encoding='utf-8') as f:
                f.writelines(lines)
            print(f"Updated {filename}: '{old_title}' -> '{new_title}'")
        else:
            print(f"Warning: {filename} is empty")
    else:
        print(f"Error: {filename} not found")
