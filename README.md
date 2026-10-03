# Turkish Sentiment Analysis

Lexicon-based sentiment scoring for Turkish text, using word polarities from emoji-labeled tweets.

## Install

Requires Python 3.10 or newer. `nltk` 3.10.3 does not install on older Pythons.

```bash
git clone https://github.com/msaidzengin/turkish-sentiment-analysis.git
cd turkish-sentiment-analysis
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

On Windows, activate with `.venv\Scripts\activate` instead of `source`.

The first run downloads NLTK `punkt`, `punkt_tab`, and Turkish stopwords.

## Usage

From the repository root, with the virtual environment active:

```bash
python sentiment.py "bu film çok güzeldi bayıldım"
```

Example output:

```
text:    bu film çok güzeldi bayıldım
label:   positive
score:   +0.420
tokens:  film güzel bayıl
matched: güzel(+0.42), bayıl(+0.42)
```

Read sentences from stdin, one per line:

```bash
printf '%s\n' "berbat bir gündü her şey çok kötüydü" "masa kalem defter" | python sentiment.py
```

```
text:    berbat bir gündü her şey çok kötüydü
label:   negative
score:   -0.405
tokens:  berbat günt kötü
matched: kötü(-0.41)

text:    masa kalem defter
label:   neutral
score:   +0.000
tokens:  masa kalem defter
matched: —
```

Skip stemming. The same positive sentence no longer matches the lexicon:

```bash
python sentiment.py --no-stem "bu film çok güzeldi bayıldım"
```

```
text:    bu film çok güzeldi bayıldım
label:   neutral
score:   +0.000
tokens:  film güzeldi bayıldım
matched: —
```

With no arguments, the script scores three built-in sentences: the positive example above, the negative example, and `masa kalem defter`.

```bash
python sentiment.py
python sentiment.py --help
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

Rebuild the lexicon only after editing the sentence files. This overwrites `data/lexicon/word-counts.txt`. The examples above use the lexicon already in the repository. `--stem` counts stems instead of surface forms.

```bash
python prepare_data.py
```

```
positive sentences: 266743
negative sentences: 230245
lexicon words:      374240
wrote data/lexicon/word-counts.txt
```

`collect.py` does not download tweets. The old collector used twint, which no longer works.

```bash
python collect.py
```

```
Tweet collection via twint is retired.
Cleaned sentences are in data/sentences/. Rebuild counts with: python prepare_data.py
positive emoji queries: 22
negative emoji queries: 19
```

## Tests

```bash
python -m unittest test_sentiment.py
```

## Dependencies

- `nltk==3.10.3`
- `TurkishStemmer==1.3`
