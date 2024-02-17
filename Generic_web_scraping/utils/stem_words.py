import nltk
from nltk.stem import PorterStemmer

# nltk.download('punkt')
stemmer = PorterStemmer()

def stem_sentence(sentence):
    words = nltk.word_tokenize(sentence)
    stemmed_words = [stemmer.stem(word) for word in words]
    stemmed_sentence = " ".join(stemmed_words)
    return stemmed_sentence
