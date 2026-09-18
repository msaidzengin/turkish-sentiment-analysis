"""Lexicon-based Turkish sentiment analysis.

The polarity lexicon is built from emoji-labeled tweets: each word's score
is (positive_count - negative_count) / (positive_count + negative_count)
using the frequencies in data/lexicon/word-counts.txt.
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from TurkishStemmer import TurkishStemmer

from preprocess import preprocess

ROOT = Path(__file__).resolve().parent
ALL_WORDS = ROOT / "data" / "lexicon" / "word-counts.txt"

MIN_TOTAL = 25
MIN_ABS_SCORE = 0.30
MIN_LEN = 3


@dataclass(frozen=True)
class SentimentResult:
    text: str
    label: str
    score: float
    tokens: list[str]
    matched: list[tuple[str, float]]

    def as_text(self) -> str:
        hits = ", ".join(f"{word}({value:+.2f})" for word, value in self.matched) or "—"
        return (
            f"text:    {self.text}\n"
            f"label:   {self.label}\n"
            f"score:   {self.score:+.3f}\n"
            f"tokens:  {' '.join(self.tokens) or '—'}\n"
            f"matched: {hits}"
        )


def _is_token(word: str) -> bool:
    if len(word) < MIN_LEN:
        return False
    return word.isalpha()


@lru_cache(maxsize=1)
def load_lexicon(path: Path = ALL_WORDS) -> dict[str, float]:
    lexicon: dict[str, float] = {}
    if not path.exists():
        raise FileNotFoundError(f"Lexicon file not found: {path}")

    with path.open(encoding="utf-8") as handle:
        for raw in handle:
            parts = raw.split()
            if len(parts) != 3:
                continue
            word, pos_s, neg_s = parts
            if not _is_token(word):
                continue
            try:
                pos, neg = int(pos_s), int(neg_s)
            except ValueError:
                continue
            total = pos + neg
            if total < MIN_TOTAL:
                continue
            score = (pos - neg) / total
            if abs(score) < MIN_ABS_SCORE:
                continue
            lexicon[word] = score
    return lexicon


@lru_cache(maxsize=1)
def _stemmer() -> TurkishStemmer:
    return TurkishStemmer()


def analyze(text: str, stem: bool = True) -> SentimentResult:
    """Score a Turkish sentence. Score is in [-1, 1]."""
    tokens = preprocess(text)
    if stem:
        stemmer = _stemmer()
        tokens = [stemmer.stem(token) for token in tokens]

    lexicon = load_lexicon()
    matched = [(token, lexicon[token]) for token in tokens if token in lexicon]
    if matched:
        score = sum(value for _, value in matched) / len(matched)
    else:
        score = 0.0

    if score >= 0.15:
        label = "positive"
    elif score <= -0.15:
        label = "negative"
    else:
        label = "neutral"

    return SentimentResult(
        text=text,
        label=label,
        score=score,
        tokens=tokens,
        matched=matched,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Score Turkish text with the emoji-labeled tweet lexicon."
    )
    parser.add_argument("text", nargs="*", help="Text to analyze")
    parser.add_argument(
        "--no-stem",
        action="store_true",
        help="Skip Turkish stemming before lexicon lookup",
    )
    args = parser.parse_args(argv)

    if args.text:
        samples = [" ".join(args.text)]
    else:
        piped = []
        if not sys.stdin.isatty():
            piped = [line.strip() for line in sys.stdin if line.strip()]
        samples = piped or [
            "bu film çok güzeldi bayıldım",
            "berbat bir gündü her şey çok kötüydü",
            "masa kalem defter",
        ]

    for index, sample in enumerate(samples):
        if index:
            print()
        print(analyze(sample, stem=not args.no_stem).as_text())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
