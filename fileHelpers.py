
from collections import Counter
import json
from os import close, walk
import os
import unicodedata
from pypdf import PdfReader


import re

def pre_tokenize(text):
    # splits into words, numbers, and individual punctuation
    return re.findall(r"\w+|[^\w\s]", text.lower())

def clean_text(text):
    text = text.replace("-\n", "")               # rejoin hyphenated line breaks
    return unicodedata.normalize("NFKC", text)

def build_splits(word_freqs):
    return {word: list(word) + ["</w>"] for word in word_freqs}

def build_word_freqs(documents):
    word_freqs = Counter()
    for text in documents:
        word_freqs.update(pre_tokenize(text))
    return word_freqs


f = []

word_freqs  = Counter() 


def retrieve_files(mypath):
    word_freqs = build_word_freqs(iter_documents(mypath))
    return build_splits(word_freqs), word_freqs


def iter_documents(mypath):
    """Yield raw text, one document at a time. Swap/extend this for new sources."""
    for dirpath, dirnames, filenames in walk(mypath):
        for name in filenames:
            path = os.path.join(dirpath, name)
            if name.lower().endswith(".pdf"):
                reader = PdfReader(path)
                text = " ".join(page.extract_text() or "" for page in reader.pages)
                yield clean_text(text)
            elif name.lower().endswith(".txt"):
                with open(path, encoding="utf-8") as f:
                    yield clean_text(f.read())




def save_tokenizer(vocab, merges, path):
    vocabData = {
        "vocab": {token: idx for idx, token in enumerate(vocab)},
        
    }
    mergesData = {
        "merges": merges
    }
    with open(f"{path}/{os.getenv('TOKEN_VAULT')}", "w", encoding="utf-8") as f:
        json.dump(vocabData, f, ensure_ascii=False, indent=2)
    with open(f"{path}/{os.getenv('MERGES_VAULT')}", "w", encoding="utf-8") as f:
        json.dump(mergesData, f, ensure_ascii=False, indent=2)


def load_tokenizer(path):
    with open(f"{path}/{os.getenv('TOKEN_VAULT')}", encoding="utf-8") as f:
        vocabData = json.load(f)
    with open(f"{path}/{os.getenv('MERGES_VAULT')}", encoding="utf-8") as f:
        mergesData = json.load(f)
    vocab = vocabData["vocab"]
    merges = [tuple(pair) for pair in mergesData["merges"]]
    return vocab, merges
