import nltk
import locale
import string
from nltk.corpus import stopwords
from turkishnlp import detector

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

def perform_preprocessing(text):
    text = text.translate(str.maketrans('', '', string.punctuation)).lower()
    #text = zemberek.normalizer.normalize(text)
    tokens = tokenize(text)
    #tokens = remove_stops(tokens)
    #tokens = zemberek.stemmer.stem_words(tokens)
    #tokens = remove_stops(tokens)
    return tokens

text = 'meta sufimiydi nydi okuyup üflyecenmi ne yapcaksn yap artık bizde bilelim ne nmaran vrsa yeter sıktın artık :)'
print(perform_preprocessing(text))

obj = detector.TurkishNLP()
obj.create_word_set()
lwords = obj.list_words(text)
print(obj.auto_correct(lwords))


