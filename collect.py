"""Historical tweet collection notes.

The original collector used twint to search Twitter for positive and
negative emoji queries. Twint is unmaintained and no longer works against
X/Twitter, so this script does not collect new data.

The cleaned sentences from that collection live in data/sentences/.
Rebuild the lexicon with:

    python prepare_data.py
"""

from __future__ import annotations

POSITIVE_EMOJIS = [
    ":)",
    "<3",
    "😀",
    "😃",
    "😄",
    "😁",
    "😆",
    "😅",
    "😂",
    "🤣",
    "☺️",
    "😊",
    "😇",
    "🙂",
    "🙃",
    "😍",
    "🤓",
    "😎",
    "👏",
    "👍",
    "🙏",
    "❤️",
]

NEGATIVE_EMOJIS = [
    ":(",
    "😞",
    "😔",
    "😟",
    "😕",
    "🙁",
    "☹️",
    "😣",
    "😖",
    "😫",
    "😩",
    "😢",
    "😭",
    "😤",
    "😠",
    "😡",
    "😥",
    "😓",
    "🤒",
]


def main() -> int:
    print(
        "Tweet collection via twint is retired.\n"
        "Cleaned sentences are in data/sentences/. "
        "Rebuild counts with: python prepare_data.py"
    )
    print(f"positive emoji queries: {len(POSITIVE_EMOJIS)}")
    print(f"negative emoji queries: {len(NEGATIVE_EMOJIS)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
