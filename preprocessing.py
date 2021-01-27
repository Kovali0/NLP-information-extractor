import re

import nltk
from nltk.corpus import stopwords
stop_words = stopwords.words('english')


def tokenize_to_words(text):
    """Tokenize sample text to list of words.
    :param text: sample to preprocessing :return: list of words in sample"""
    words = nltk.word_tokenize(text)
    return words


def tokenize_to_sentences(text):
    """Tokenize sample text to list of whole sentences.
    :param text: sample to preprocessing :return: list of sentences"""
    sentences = nltk.sent_tokenize(text)
    return sentences


def remove_stopwords(words):
    """Remove stop words from list of tokenized words.
    :param words: list of tokenized words :return: list of tokenized words without stop words"""
    return [word for word in words if word not in stop_words]


def to_lowercase(sample):
    """Convert all characters to lowercase in sample text.
    :param sample: sample text to preprocessing :return: sample with only lowercase characters"""
    return sample.lower()


def remove_punctuation(sample):
    """Remove punctuations, but kept '.' and '-'.
    :param sample: sample text to preprocessing :return: sample without punctuations"""
    sample = re.sub(r'[^A-Za-z .-]+', '', sample)
    return sample

