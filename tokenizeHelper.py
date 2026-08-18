
from collections import Counter

def getSingleTokens(splits):
    return {t for tokens in splits.values() for t in tokens}


# Claude generated progres bar
def progress_bar(current, total, width=40):
    frac = current / total
    filled = int(width * frac)
    bar = "█" * filled + "-" * (width - filled)
    print(f"\r|{bar}| {current}/{total} ({frac:.0%})", end="", flush=True)
    if current == total:
        print()  # newline when done




def findMergeToken(splits, word_freqs):

    tokenFreqs = Counter()
    
    for word, freq in word_freqs.items():
        token = splits[word]
      
        # at this point we have every base token, 
        # now we can start counting the most frequent pairs of tokens
        
        for i in range(len(token) - 1):
            pair = (token[i], token[i + 1])
            tokenFreqs[pair] += freq
            
        
    if not tokenFreqs:
        return None

    
    return tokenFreqs.most_common(1)[0][0]


def apply_merge(pair, splits):
    a, b = pair
    merged = a + b
    for word, tokens_list in splits.items():
        i = 0
        while i < len(tokens_list) - 1:
            if tokens_list[i] == a and tokens_list[i + 1] == b:
                tokens_list[i:i + 2] = [merged]  # 2 elements -> 1
            else:
                i += 1
