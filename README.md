# Turkish Sentiment Analysis

Lexicon-based sentiment scoring for Turkish text. The word polarities come
from tweets that were weakly labeled with positive or negative emoji.

## Install

Requires Python 3.10 or newer. `nltk` 3.10.3 does not install on older Pythons.

```bash
python3 -m pip install -r requirements.txt
```

The first run downloads NLTK `punkt`, `punkt_tab`, and Turkish stopwords.

## Usage

Score a sentence:

```bash
python sentiment.py "bu film çok güzeldi bayıldım"
```

Read from stdin:

```bash
echo "berbat bir gündü" | python sentiment.py
```

Skip stemming:

```bash
python sentiment.py --no-stem "mutluyum"
```

Run without arguments to see a few built-in examples.

Example output:

```
text:    bu film çok güzeldi bayıldım
label:   positive
score:   +0.512
tokens:  film güzel bayıl
matched: güzel(+0.71), bayıl(+0.64)
```

## How scoring works

1. Normalize the text (lowercase, strip URLs, mentions, punctuation).
2. Tokenize with NLTK's Turkish model and drop stopwords.
3. Stem tokens with TurkishStemmer.
4. Look each token up in `data/lexicon/word-counts.txt`.
5. Word polarity is `(positive_count - negative_count) / total`.
6. The sentence score is the mean polarity of matched tokens.
7. Labels: `positive` (>= 0.15), `negative` (<= -0.15), otherwise `neutral`.

Words need at least 25 total occurrences and `|polarity| >= 0.30` to enter
the lexicon. That filters out function words and emoji-noise tokens.

## Data

| Path | What it is |
| --- | --- |
| `data/sentences/positive.txt` | Cleaned tweets labeled with positive emoji |
| `data/sentences/negative.txt` | Cleaned tweets labeled with negative emoji |
| `data/lexicon/word-counts.txt` | `word positive_count negative_count` |

Rebuild the lexicon after editing the sentence files:

```bash
python prepare_data.py
```

`collect.py` only documents the original emoji queries. The old Twitter
collector used twint, which is unmaintained and no longer works.

## Tests

```bash
python -m unittest test_sentiment.py
```

## Dependencies

- `nltk==3.10.3`
- `TurkishStemmer==1.3`
