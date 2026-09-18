"""Rebuild the word-count lexicon from data/sentences/.

The checked-in data/lexicon/word-counts.txt is already this output.
Run this only after you change the sentence files.
"""

from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path

from TurkishStemmer import TurkishStemmer

from preprocess import preprocess

ROOT = Path(__file__).resolve().parent
SENTENCES = ROOT / "data" / "sentences"
LEXICON = ROOT / "data" / "lexicon"
POSITIVE = SENTENCES / "positive.txt"
NEGATIVE = SENTENCES / "negative.txt"
WORD_COUNTS = LEXICON / "word-counts.txt"


def _read_sentences(path: Path) -> list[str]:
    if not path.exists():
        raise SystemExit(f"Sentence file not found: {path}")
    sentences: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        text = line.strip()
        if not text or text.lower() == "tweet":
            continue
        sentences.append(text)
    return sentences


def _count_words(sentences: list[str], stem: bool) -> Counter[str]:
    stemmer = TurkishStemmer() if stem else None
    counts: Counter[str] = Counter()
    for sentence in sentences:
        tokens = preprocess(sentence)
        if stemmer is not None:
            tokens = [stemmer.stem(token) for token in tokens]
        counts.update(tokens)
    return counts


def _write_word_counts(path: Path, positive: Counter[str], negative: Counter[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    words = set(positive) | set(negative)
    with path.open("w", encoding="utf-8") as handle:
        for word in sorted(words):
            handle.write(f"{word} {positive.get(word, 0)} {negative.get(word, 0)}\n")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Rebuild data/lexicon/word-counts.txt from data/sentences/"
    )
    parser.add_argument(
        "--stem",
        action="store_true",
        help="Stem tokens before counting",
    )
    args = parser.parse_args(argv)

    positive = _read_sentences(POSITIVE)
    negative = _read_sentences(NEGATIVE)
    pos_counts = _count_words(positive, stem=args.stem)
    neg_counts = _count_words(negative, stem=args.stem)
    _write_word_counts(WORD_COUNTS, pos_counts, neg_counts)

    print(f"positive sentences: {len(positive)}")
    print(f"negative sentences: {len(negative)}")
    print(f"lexicon words:      {len(pos_counts) + len(neg_counts - pos_counts)}")
    print(f"wrote {WORD_COUNTS.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
