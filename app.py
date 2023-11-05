# import pyodbc
import sys, logging
from PyQt6.QtWidgets import QMainWindow, QApplication
from view.main import Ui_Dialog
from datetime import date

FORMAT = '%(asctime)s %(levelname)s: %(message)s'
logging.basicConfig(level=logging.DEBUG, filename=f'./logs/{date.today()}.log', filemode='a', format=FORMAT)

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec())