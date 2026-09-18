"""Historical tweet collection notes.

The original collector used twint to search Twitter for positive and
negative emoji queries and wrote dumps into new/. Twint is unmaintained
and no longer works against X/Twitter, so this script does not collect
new data.

The dumps that were already collected remain in new/ and are enough to
rebuild the lexicon with:

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
        "Existing dumps are in new/. Rebuild counts with: python prepare_data.py"
    )
    print(f"positive emoji queries: {len(POSITIVE_EMOJIS)}")
    print(f"negative emoji queries: {len(NEGATIVE_EMOJIS)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
