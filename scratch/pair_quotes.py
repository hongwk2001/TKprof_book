with open(r"d:\git_repo\TKprof_book\books\odyssey\chapters\ch_14_ko.txt", "r", encoding="utf-8") as f:
    content = f.read()

import re
quotes = [m.start() for m in re.finditer('"', content)]

with open(r"d:\git_repo\TKprof_book\scratch\pair_quotes_out.txt", "w", encoding="utf-8") as out:
    out.write(f"Number of double quotes: {len(quotes)}\n")
    for i in range(0, len(quotes), 2):
        start = quotes[i]
        end = quotes[i+1] if i+1 < len(quotes) else -1
        out.write(f"Quote Pair {i//2 + 1}:\n")
        out.write(f"  Start index: {start}, End index: {end}\n")
        if end != -1:
            snippet = content[start:end+1]
            if len(snippet) > 200:
                snippet = snippet[:100] + " ... [TRUNCATED] ... " + snippet[-100:]
            out.write(f"  Text: {repr(snippet)}\n")
        else:
            out.write(f"  Unpaired quote! Text from start: {repr(content[start:start+100])}\n")
