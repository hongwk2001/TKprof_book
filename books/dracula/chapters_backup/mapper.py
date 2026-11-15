import json

with open('sentences.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

sentences = [line.split(':', 1)[1].strip() for line in lines]

# We will build 73 paragraphs.
# Let's initialize 73 empty lists.
paragraphs = [[] for _ in range(73)]

def assign(start, end, p_idx):
    for i in range(start, end + 1):
        paragraphs[p_idx].append(sentences[i])

# Mapping based on my manual analysis:
assign(0, 2, 0) # P001, P002 (Wait, 0 is P001, 1 is P002? Let's check sentences.txt)
# Wait, let's refine the mapping!
