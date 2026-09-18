"""Turkish text preprocessing: normalize, tokenize, drop stopwords."""

from __future__ import annotations

import re
import string
from functools import lru_cache

import nltk

PUNCTUATION = string.punctuation + "“”‘’…—–•·«»"
URL_RE = re.compile(r"https?://\S+|www\.\S+|t\.co/\S+", re.IGNORECASE)
MENTION_RE = re.compile(r"@\w+")
HASHTAG_RE = re.compile(r"#")
PIC_RE = re.compile(r"pictwitter\S*", re.IGNORECASE)
WHITELIST_RE = re.compile(r"[^a-zçğıöşüâîû0-9\s]")


def ensure_nltk_data() -> None:
    """Download the NLTK resources this project needs, once."""
    resources = (
        ("tokenizers/punkt", "punkt"),
        ("tokenizers/punkt_tab", "punkt_tab"),
        ("corpora/stopwords", "stopwords"),
    )
    for path, name in resources:
        try:
            nltk.data.find(path)
        except LookupError:
            nltk.download(name, quiet=True)


# nltk's Turkish list misses a few high-frequency function words.
EXTRA_STOPWORDS = {
    "bir",
    "bu",
    "şu",
    "o",
    "çok",
    "şey",
    "için",
    "ile",
    "gibi",
    "kadar",
    "daha",
    "en",
    "mi",
    "mı",
    "mu",
    "mü",
    "de",
    "da",
    "ki",
}


@lru_cache(maxsize=1)
def turkish_stopwords() -> set[str]:
    ensure_nltk_data()
    return set(nltk.corpus.stopwords.words("turkish")) | EXTRA_STOPWORDS


def normalize(text: str) -> str:
    text = text.replace("\n", " ").strip().lower()
    text = URL_RE.sub(" ", text)
    text = MENTION_RE.sub(" ", text)
    text = HASHTAG_RE.sub("", text)
    text = PIC_RE.sub(" ", text)
    text = text.translate(str.maketrans("", "", PUNCTUATION))
    text = WHITELIST_RE.sub(" ", text)
    return " ".join(text.split())


def tokenize(text: str) -> list[str]:
    ensure_nltk_data()
    return nltk.word_tokenize(text, language="turkish")


def is_stop(word: str) -> bool:
    return len(word) <= 1 or word in turkish_stopwords()


def remove_stops(tokens: list[str]) -> list[str]:
    return [token for token in tokens if not is_stop(token)]


def preprocess(text: str) -> list[str]:
    """Return normalized, tokenized, stopword-free tokens."""
    return remove_stops(tokenize(normalize(text)))
