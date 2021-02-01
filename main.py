import sys
import pickle
import nltk
from PyQt5 import QtWidgets
from MainWindow import Ui_MainWindow
import preprocessing as pre
from document import Document

# Noun Part of Speech Tags used by NLTK
NOUNS = ['NN', 'NNS', 'NNP', 'NNPS']
VERBS = ['VB', 'VBG', 'VBD', 'VBN', 'VBP', 'VBZ']


def train_tagger():
    """
    Create and train on brown and treebank corpuses, nltk simple tagger with 3 layers.
    Layers: Unigram, Bigram and Trigram.
    :return: trained trigram tagger object
    """
    train_corpus = nltk.corpus.brown.tagged_sents()
    train_corpus += nltk.corpus.treebank.tagged_sents()
    layer0 = nltk.DefaultTagger('NN')
    layer1 = nltk.UnigramTagger(train_corpus, backoff=layer0)
    layer2 = nltk.BigramTagger(train_corpus, backoff=layer1)
    trigram_tagger = nltk.TrigramTagger(train_corpus, backoff=layer2)
    pickle.dump(trigram_tagger, open('trained_tagger.pkl', 'wb'))
    return trigram_tagger


def get_svo(sentence, subject):
    """
    Create svo model.
    :param sentence: sample sentence
    :param subject: main subject noun
    :return: dictionary with svo
    """
    subject_idx = next((i for i, v in enumerate(sentence) if v[0].lower() == subject), None)
    print(subject_idx)
    data = {'subject': subject}
    print(len(sentence))
    for i in range(subject_idx, len(sentence)):
        found_action = False
        for j, (token, tag) in enumerate(sentence[i+1:]):
            if tag in VERBS:
                data['action'] = token
                found_action = True
            if tag in NOUNS and found_action == True:
                data['object'] = token
                data['phrase'] = sentence[i: i+j+2]
                return data
    return {}


def topic_finder(document):
    """
    Main method for finding topics in text, document.
    :param document: sample text
    :return: list of possible topics
    """
    topics_list = []
    try:
        important_nouns = document.find_topic()
        trigram_tagger = pickle.load(open('trained_tagger.pkl', 'rb')) # train_tagger()
        sentences = pre.tokenize_to_sentences(pre.remove_punctuation(document.sample))
        sentences = [pre.tokenize_to_words(sent) for sent in sentences]
        sentences = [sentence for sentence in sentences if important_nouns[0].lower() in [word.lower() for word in sentence]]
        tagged_sentences = [trigram_tagger.tag(sent) for sent in sentences]
        important_nouns = document.find_topic()
        svo_data = [get_svo(sentence, important_nouns[0].lower()) for sentence in tagged_sentences]
        for svo in svo_data:
            sentence = ''
            for word in svo.get('phrase'):
                sentence += word[0] + ' '
            topics_list.append(sentence)
    except IndexError:
        if not topics_list:
            topics_list.append("Topic not found. Need more data.")
    return topics_list


def main(main_window, ui):
    """
    Main program
    :param main_window: application main window
    :param ui: designed ui
    """

    main_window.show()
    sample = Document("")
    ui.get_document().textChanged.connect(lambda: sample.change_document(ui.get_document().toPlainText()))
    ui.phone_numbers_btn.clicked.connect(lambda: ui.phone_numbers_list.clear())
    ui.phone_numbers_btn.clicked.connect(lambda: ui.phone_numbers_list.addItems(sample.extract_phone_numbers()))
    ui.email_btn.clicked.connect(lambda: ui.emails_list.clear())
    ui.email_btn.clicked.connect(lambda: ui.emails_list.addItems(sample.extract_emails()))
    ui.topic_btn.clicked.connect(lambda: ui.topics_list.clear())
    ui.topic_btn.clicked.connect(lambda: ui.topics_list.addItems(topic_finder(sample)))


def exception_hook_fun(exc_type, value, traceback):
    """
    Catching exception in program on global scope and print it.
    :param exc_type: exc param
    :param value: exc param
    :param traceback: exc param
    """
    print(exc_type, value, traceback)
    sys.excepthook(exc_type, value, traceback)
    sys.exit(1)


if __name__ == '__main__':
    sys.except_hook = exception_hook_fun
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    Ui_Mw = Ui_MainWindow()
    Ui_Mw.setupUi(MainWindow)
    main(MainWindow, Ui_Mw)
    sys.exit(app.exec_())
