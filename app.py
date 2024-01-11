from datetime import date
from PyQt6.QtCore import QThread
from PyQt6.QtWidgets import QMainWindow, QApplication, QDialog
# from libs.controllers.optionController import optionController
from libs.controllers.mainController import MainController
from libs.view.ui import Ui_dialog as mainDialog
from libs.view.option import Ui_Dialog as optionDialog
import logging, os, sys
import dotenv
from libs.threads.fetchTestsThread import FetchTestsThread

dotenv.load_dotenv('.env')
basicPath = os.environ.get('BASIC_PATH')

def initializeFolder() :
  if not os.path.exists(f'{basicPath}'):
    os.makedirs(f'{basicPath}')
    print(f'{basicPath} created')
  if not os.path.exists(f'{basicPath}/logs'):
    os.mkdir(f'{basicPath}/logs')
    print(f'{basicPath}/logs created')
  if not os.path.exists(f'{basicPath}/dbs'):
    os.mkdir(f'{basicPath}/dbs')
    print(f'{basicPath}/dbs created')

class MainWindow(QMainWindow):
  def __init__(self):
    super(MainWindow, self).__init__()
    self.ui = mainDialog()
    self.ui.setupUi(self)
    self.mainController = MainController(self.ui)
    self.fetchTestsThread()
# thread 1
# query automation mdb every 15 mins
  def fetchTestsThread(self):
    self.thread = QThread()
    self.thread.run = FetchTestsThread().main
    self.thread.start()


if __name__ == '__main__':
  initializeFolder()
  FORMAT = '%(asctime)s %(levelname)s: %(message)s'
  logging.basicConfig(level=logging.DEBUG, filename=f'{basicPath}\\logs\\{date.today()}.log', filemode='a', format=FORMAT)
  app = QApplication([])
  window = MainWindow()
  window.show()
  sys.exit(app.exec())