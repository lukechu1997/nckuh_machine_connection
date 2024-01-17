from datetime import date
from PyQt6.QtCore import QThread
from PyQt6.QtWidgets import QMainWindow, QApplication
from libs.controllers.mainController import MainController
from libs.view.ui import Ui_dialog as mainDialog
import logging, os, sys
import dotenv
from libs.threads.fetchTestsThread import FetchTestsThread

extDataDir = os.getcwd()
if getattr(sys, 'frozen', False):
    extDataDir = sys._MEIPASS
dotenv.load_dotenv(dotenv_path=os.path.join(extDataDir, '.env'))
dotenv.set_key(dotenv_path=os.path.join(extDataDir, '.env'), key_to_set='EXT_DATA_DIR', value_to_set=extDataDir)
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
  try:
    initializeFolder()
    FORMAT = '%(asctime)s %(levelname)s: %(message)s'
    logging.basicConfig(level=logging.DEBUG, filename=f'{basicPath}\\logs\\{date.today()}.log', filemode='a', format=FORMAT)
    app = QApplication([])
    window = MainWindow()
    window.show()    
    sys.exit(app.exec())

  except Exception as e:
    logging.critical(e)
    logging.critical(sys.exc_info())