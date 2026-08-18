import os

from fileHelpers import retrieve_files, save_tokenizer
from tokenizeHelper import apply_merge, findMergeToken, getSingleTokens, progress_bar
from dotenv import load_dotenv

load_dotenv()


tokenBudget = 2000

training_path = os.getenv("TRAINING_PATH")
if not training_path:
    raise RuntimeError("TRAINING_PATH not set")

splits, word_freqs = retrieve_files(training_path)
# handle unknown tokens
special = ["<unk>", "<pad>"]
vocab = special + sorted(getSingleTokens(splits))

merges = []
""" print(f"Initial number of tokens: {tokens}") """
while len(vocab) < tokenBudget:
    pair = findMergeToken(splits, word_freqs)
    if pair is None:
        break
    apply_merge(pair, splits)
    merges.append(pair)
    vocab.append(pair[0] + pair[1])


    progress_bar(len(merges), tokenBudget)
print()
print(f"Final number of tokens: {len(vocab)}")
print(f"Final number of merges: {len(merges)}")
save_tokenizer(vocab, merges, os.getenv('VAULT_PATH')       
)

