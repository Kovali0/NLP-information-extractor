import sys
import re
from PyQt5 import QtWidgets
from MainWindow import Ui_MainWindow
import preprocessing as pre


class Document:
    """
    Representation of processing document.
    """
    def __init__(self, text):
        self.text = text
        self.normalized_sample = ''

    def change_document(self, new_text):
        """
        Set new document text
        :param new_text: param for new text
        """
        self.text = new_text

    def preprocessing(self):
        """
        General preprocessing on document sample
        """
        self.text = pre.remove_punctuation(self.text)
        self.text = ' '.join(pre.remove_stopwords(pre.tokenize_to_words(self.text)))
        sentences = pre.tokenize_to_sentences(self.text)
        self.normalized_sample = [pre.tokenize_to_words(sent) for sent in sentences]
        return sentences

    def extract_phone_numbers(self):
        reg = re.compile(r"(\(\+\d{2}\)\s*\d{3}[-\.\s]??\d{3}|\d{3}[-\.\s]\d{3}[-\.\s]\d{3})")
        return reg.findall(self.text)

    def extract_emails(self):
        reg = re.compile(r"([\w\.-]+@\w+[.]\w{2,3})")
        return reg.findall(self.text)


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
    ui.topic_btn.clicked.connect(lambda: ui.topics_list.addItems(sample.preprocessing()))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    main(MainWindow, ui)
    sys.exit(app.exec_())
