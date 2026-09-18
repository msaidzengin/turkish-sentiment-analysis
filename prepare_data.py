"""Rebuild word-count tables from the historical tweet dumps in new/.

The checked-in dataset/ files already contain this output. Run this only
when you add more labeled tweets.
"""

from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path

from TurkishStemmer import TurkishStemmer

from preprocess import normalize, preprocess

ROOT = Path(__file__).resolve().parent
NEW_DIR = ROOT / "new"
DATASET = ROOT / "dataset"


def _read_tweets(path: Path) -> list[str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    tweets: list[str] = []
    for line in lines:
        text = line.strip()
        if not text or text.lower() == "tweet":
            continue
        cleaned = normalize(text)
        if cleaned:
            tweets.append(cleaned)
    return tweets


def _collect(label_prefix: str) -> list[str]:
    tweets: list[str] = []
    for path in sorted(NEW_DIR.glob(f"{label_prefix}*.txt")):
        tweets.extend(_read_tweets(path))
    return tweets


def _count_words(tweets: list[str], stem: bool) -> Counter[str]:
    stemmer = TurkishStemmer() if stem else None
    counts: Counter[str] = Counter()
    for tweet in tweets:
        tokens = preprocess(tweet)
        if stemmer is not None:
            tokens = [stemmer.stem(token) for token in tokens]
        counts.update(tokens)
    return counts


def _write_counts(path: Path, counts: Counter[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for word, count in sorted(counts.items()):
            handle.write(f"{word} {count}\n")


def _write_all_words(path: Path, positive: Counter[str], negative: Counter[str]) -> None:
    words = set(positive) | set(negative)
    with path.open("w", encoding="utf-8") as handle:
        for word in sorted(words):
            handle.write(f"{word} {positive.get(word, 0)} {negative.get(word, 0)}\n")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Rebuild lexicon files from new/")
    parser.add_argument(
        "--stem",
        action="store_true",
        help="Also write stemmed word-count files",
    )
    args = parser.parse_args(argv)

    if not NEW_DIR.exists():
        raise SystemExit(f"Tweet dump folder not found: {NEW_DIR}")

    positive_tweets = _collect("p")
    negative_tweets = _collect("n")
    if not positive_tweets and not negative_tweets:
        raise SystemExit("No tweets found under new/")

    pos_counts = _count_words(positive_tweets, stem=False)
    neg_counts = _count_words(negative_tweets, stem=False)

    DATASET.mkdir(parents=True, exist_ok=True)
    _write_counts(DATASET / "positive_words.txt", pos_counts)
    _write_counts(DATASET / "negative_words.txt", neg_counts)
    _write_all_words(DATASET / "all_words.txt", pos_counts, neg_counts)

    if args.stem:
        _write_counts(DATASET / "positive_words_stemmed.txt", _count_words(positive_tweets, stem=True))
        _write_counts(DATASET / "negative_words_stemmed.txt", _count_words(negative_tweets, stem=True))

    print(f"positive tweets: {len(positive_tweets)}")
    print(f"negative tweets: {len(negative_tweets)}")
    print(f"positive words:  {len(pos_counts)}")
    print(f"negative words:  {len(neg_counts)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
