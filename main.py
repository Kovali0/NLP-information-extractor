import sys
from PyQt5 import QtWidgets
from MainWindow import Ui_MainWindow
import preprocessing as pre


class Document:
    """
    Representation of processing document.
    """
    def __init__(self, text):
        self.text = text

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
        pre.tokenize_to_words(self.text)


def main(main_window, ui):
    """
    Main program
    :param main_window: application main window
    :param ui: designed ui
    """
    main_window.show()
    sample = Document("")
    ui.get_document().textChanged.connect(lambda: sample.change_document(ui.get_document().toPlainText()))
    ui.topic_btn.clicked.connect(lambda: sample.preprocessing())


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    main(MainWindow, ui)
    sys.exit(app.exec_())
