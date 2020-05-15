import nltk
import string
from nltk.corpus import stopwords

def is_stop(word):
    stop_words = set(nltk.corpus.stopwords.words("turkish"))
    if word in stop_words:
        return True
    if len(word) <= 1:
        return True
    return False

def remove_stops(tokens):
    return [token for token in tokens if not is_stop(token)]

def tokenize(text):
    return nltk.word_tokenize(text, 'turkish')

def preprocess(text):
    text = text.translate(str.maketrans('', '', string.punctuation)).lower()
    tokens = tokenize(text)
    tokens = remove_stops(tokens)
    return tokens


