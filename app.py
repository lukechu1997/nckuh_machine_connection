# import pyodbc
from datetime import date
from PyQt6.QtWidgets import QMainWindow, QApplication
import sys, logging
from libs.view.main import Ui_dialog
from libs.view.uiFunctions import UiFunc

FORMAT = '%(asctime)s %(levelname)s: %(message)s'
logging.basicConfig(level=logging.DEBUG, filename=f'./logs/{date.today()}.log', filemode='a', format=FORMAT)

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_dialog()
        self.ui.setupUi(self)
        UiFunc(self.ui)

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec())