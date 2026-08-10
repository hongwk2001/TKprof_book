import json

data = json.load(open('align_data.json', encoding='utf-8'))
ko_sents = data['ko_sents']
en = data['en']

total_en = sum(len(p) for p in en)
total_ko = sum(len(s) for s in ko_sents)
ratio = total_ko / total_en

en_targets = [len(p) * ratio for p in en]

# We want to partition ko_sents into len(en) contiguous blocks.
# Let dp[i][j] be the min cost to partition first j sentences into i blocks.
# Cost is the squared difference from the target length.

N = len(ko_sents)
K = len(en)

dp = [[float('inf')] * (N + 1) for _ in range(K + 1)]
dp[0][0] = 0
parent = [[0] * (N + 1) for _ in range(K + 1)]

# Precompute prefix sums for ko_sents lengths
pref = [0] * (N + 1)
for i in range(N):
    pref[i+1] = pref[i] + len(ko_sents[i])

for i in range(1, K + 1):
    target = en_targets[i-1]
    for j in range(i, N + 1):
        # We need to form the i-th block ending at sentence j.
        # It can start at any sentence k from i-1 to j-1.
        # But we can optimize to only search a reasonable window.
        best_cost = float('inf')
        best_k = 0
        
        # Estimate ideal length of prefix up to k:
        # We are at block i, ending at j. This is a bit slow if we do full O(K * N^2)
        # K=102, N=471, N^2 = 220000. 102 * 220k = 22M operations, completely fine in python!
        
        for k in range(i-1, j):
            block_len = pref[j] - pref[k]
            cost = dp[i-1][k] + abs(block_len - target)**2
            if cost < best_cost:
                best_cost = cost
                best_k = k
                
        dp[i][j] = best_cost
        parent[i][j] = best_k

# Backtrack
aligned_ko = []
curr_j = N
for i in range(K, 0, -1):
    k = parent[i][curr_j]
    block = ko_sents[k:curr_j]
    aligned_ko.append(' '.join(block))
    curr_j = k
    
aligned_ko.reverse()

# Verify counts and no empty blocks
empty_blocks = [i for i, b in enumerate(aligned_ko) if not b.strip()]
print('Empty blocks:', empty_blocks)

with open('c:/git_repo/TKprof_book/books/dracula/chapters/aligned_ko_ch23.txt', 'w', encoding='utf-8') as f:
    f.write('\n\n'.join(aligned_ko))

print('Done DP alignment. Total blocks:', len(aligned_ko))
