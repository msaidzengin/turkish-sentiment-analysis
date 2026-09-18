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
4. Look each token up in `dataset/all_words.txt`.
5. Word polarity is `(positive_count - negative_count) / total`.
6. The sentence score is the mean polarity of matched tokens.
7. Labels: `positive` (>= 0.15), `negative` (<= -0.15), otherwise `neutral`.

Words need at least 25 total occurrences and `|polarity| >= 0.30` to enter
the lexicon. That filters out function words and emoji-noise tokens.

## Data

| Path | What it is |
| --- | --- |
| `new/` | Historical tweet dumps, split by emoji query |
| `dataset/all_words.txt` | `word positive_count negative_count` |
| `dataset/positive_words.txt` | Positive-side word counts |
| `dataset/negative_words.txt` | Negative-side word counts |
| `dataset/*_stemmed.txt` | Stemmed count tables |
| `dataset/*_sentences.txt` | Cleaned and stemmed tweet sentences |
| `dataset/tweets.zip` | Archived raw tweet dump |

Rebuild counts after adding files under `new/`:

```bash
python prepare_data.py
python prepare_data.py --stem
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
