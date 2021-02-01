import re
import nltk
import preprocessing as pre

# Noun Part of Speech Tags used by NLTK
NOUNS = ['NN', 'NNS', 'NNP', 'NNPS']
VERBS = ['VB', 'VBG', 'VBD', 'VBN', 'VBP', 'VBZ']


class Document:
    """
    Representation of processing document.
    """
    def __init__(self, text):
        self.text = text
        self.words = []
        self.sentences = []
        self.normalized_sample = []
        self.bag_of_words = []
        self.sample = ''

    def change_document(self, new_text):
        """Set new document text.
        :param new_text: param for new text"""
        self.text = new_text
        self.sample = new_text

    def full_preprocessing(self):
        """General preprocessing on document sample. This method include:
        remove punctuation ( . and , are kept), remove english stop words,
        tokenize to sentences, words and list of tokenized sentences to words."""
        self.text = pre.remove_punctuation(self.text)
        self.text = pre.to_lowercase(self.text)
        self.words = pre.tokenize_to_words(self.text)
        self.words = pre.remove_stopwords(self.words)
        self.text = ' '.join(self.words)
        self.sentences = pre.tokenize_to_sentences(self.text)
        self.normalized_sample = [pre.tokenize_to_words(sent) for sent in self.sentences]
        return self.sentences

    def extract_phone_numbers(self):
        """Extract all phone numbers (9 digits standard) from sample document.
        :return: list of phone numbers"""
        reg = re.compile(r"(\(\+\d{2}\)\s*\d{3}[-\.\s]??\d{3}|\d{3}[-\.\s]\d{3}[-\.\s]\d{3})")
        return reg.findall(self.text)

    def extract_emails(self):
        """Extract all emails from sample document.
        :return: list of emails"""
        reg = re.compile(r"([\w\.-]+@\w+[.]\w{2,3})")
        return reg.findall(self.text)

    def create_bag_of_words(self):
        """Returns a bag of words created by counting frequency distribution.
        :return: list of emails"""
        self.bag_of_words = nltk.FreqDist(self.words)
        return self.bag_of_words

    def find_topic(self):
        """
        Method for finding topic of document
        :return: list of proposed topic
        """
        self.full_preprocessing()
        return self.important_nouns()

    def get_entities(self):
        """Build named entities, by chunking nltk.
        :return: list of entities"""
        entities = []
        sentences = pre.tokenize_to_sentences(self.sample)
        sentences = [nltk.pos_tag(pre.tokenize_to_words(sent)) for sent in sentences]
        for tagged_sentence in sentences:
            for chunk in nltk.ne_chunk(tagged_sentence):
                if type(chunk) == nltk.tree.Tree:
                    entities.append(''.join([c[0] for c in chunk]))
        return entities

    def important_nouns(self):
        """
        Create bag of words and pick most freq of them. Generate tagged entities.
        Find most important nouns for subject in case of compare nouns freq in BoW and entities.
        :return: list of most important nouns for subject search
        """
        b_o_w = self.create_bag_of_words()
        most_freq_nouns = [word for word, _ in b_o_w.most_common(20) if nltk.pos_tag([word])[0][1] in NOUNS]

        entities = self.get_entities()
        top_20_entities = [noun for noun, _ in nltk.FreqDist(entities).most_common(20)]

        subject_nouns = [entity for entity in top_20_entities if pre.to_lowercase(entity.split()[0]) in most_freq_nouns]
        return subject_nouns
