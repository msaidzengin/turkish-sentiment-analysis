import nltk
import string
from nltk.corpus import stopwords


def preprocess(text):
    """
    Tokenize -> Normalize -> Stemming -> Stopping
    :param text: String, sentence
    :return: Returns preprocessed text as a list
    """
    
    text = text.translate(str.maketrans('', '', string.punctuation)).lower()
    words = nltk.word_tokenize(text)
    words = [nltk.LancasterStemmer().stem(word) for word in words]
    words = [word for word in words if word not in stopwords.words('turkish')]
    
    return words