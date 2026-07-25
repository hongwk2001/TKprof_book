import os
import re
import urllib.request
import collections

# Download a standard word list of valid English words if not already cached
WORDS_URL = "https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt"
CACHE_PATH = r"d:\git_repo\TKprof_book\scratch\words_alpha.txt"

if not os.path.exists(CACHE_PATH):
    try:
        urllib.request.urlretrieve(WORDS_URL, CACHE_PATH)
    except Exception as e:
        print(f"Failed to download dictionary: {e}")
        sys.exit(1)

# Load the dictionary into a set for O(1) lookups
with open(CACHE_PATH, "r", encoding="utf-8") as f:
    valid_words = set(word.strip().lower() for word in f if word.strip())

# Add some common names, French words, and special terms used in Scaramouche
valid_words.update([
    "scaramouche", "andre", "louis", "moreau", "kercadiou", "aline", "vilmorin", "philippe",
    "chabrillane", "climene", "binet", "le", "de", "la", "tour", "dazyr", "gavrillac", "gueroy",
    "michelet", "sautron", "plougastel", "benet", "levesque", "chapelier", "des", "du", "d", "nantes",
    "rennes", "paris", "dieu", "omnes", "omnibus", "rhadamantus", "pantaloon", "harlequin",
    "columbine", "polichinelle", "scaramuccia", "pasquin", "covenant", "meudon", "bretagne",
    "breton", "seigneur", "tiers", "etat", "jacobin", "jacobins", "spadassin", "spadassins",
    "spadassinicide", "spadassinicides", "rodomont", "pierrot", "scaramouches", "guichen",
    "maure", "pipriac", "feydau", "gavrillacs", "kercadious", "tressilian", "vilmorins",
    "fougeres", "liege", "chateau", "chateaux", "gendarme", "gendarmes", "diguillon", "provost",
    "comédie", "théâtre", "française", "rhadamanth", "rhadamanthine", "miserere", "monseigneur",
    "abbé", "mademoiselle", "monsieur", "messieurs", "marquis", "marquise", "comte", "comtesse",
    "vicomte", "chevalier", "seigneurie", "laquais", "corvée", "gabelles", "lettres", "cachet",
    "droit", "seigneurial", "cahier", "cahiers", "états", "généraux", "bourgeois", "bourgeoisie",
    "châtelet", "gardes", "françaises", "tuileries", "guillotine", "larned", "pitt", "danton", "marat",
    "rené", "desmoulins", "camille", "chénier", "talma", "duport", "lameth", "barnave", "cazalès",
    "maury", "plougastels", "chabrillanes", "chevaliers", "sautrons", "balthazar", "knotty",
    "impromptu", "impromptus", "turlupin", "trivelin", "tabarin", "pasquino", "scaramouch",
    "gros-guillaume", "gaultier-garguille"
])

base_dir = r"d:\git_repo\TKprof_book\books\scaramouche\chapters"

word_counts = collections.Counter()
word_locations = collections.defaultdict(list)

# Regex to find words (handling apostrophes like "don't" or "André-Louis" split)
word_re = re.compile(r"\b[a-zA-Z]+(?:'[a-zA-Z]+)?\b")

for root, dirs, files in os.walk(base_dir):
    for f in files:
        if f.endswith("_en.txt"):
            path = os.path.join(root, f)
            book_name = os.path.basename(os.path.dirname(path))
            try:
                with open(path, "r", encoding="utf-8") as file:
                    for line_idx, line in enumerate(file, 1):
                        found = word_re.findall(line)
                        for w in found:
                            wl = w.lower()
                            word_counts[wl] += 1
                            word_locations[wl].append((f"{book_name}/{f}", line_idx, line.strip()))
            except Exception as e:
                pass

suspect_words = []
for word, count in word_counts.items():
    if word not in valid_words:
        if len(word) <= 2 or word.upper() in ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"]:
            continue
        suspect_words.append((word, count))

suspect_words.sort(key=lambda x: (x[1], x[0]))

results_path = r"d:\git_repo\TKprof_book\scratch\spell_check_results.txt"
with open(results_path, "w", encoding="utf-8") as out:
    out.write(f"Found {len(suspect_words)} unique words not in the standard dictionary.\n")
    out.write("-" * 80 + "\n")
    for word, count in suspect_words:
        locs = word_locations[word]
        loc_str = ", ".join(f"{loc[0]}:{loc[1]}" for loc in locs[:3])
        if len(locs) > 3:
            loc_str += f" (+{len(locs)-3} more)"
        out.write(f"Word: {word!r} (appears {count} times) at {loc_str}\n")
        out.write(f"   Context: {locs[0][2][:100]}\n")

print("Spell check completed. Results written to scratch/spell_check_results.txt")
