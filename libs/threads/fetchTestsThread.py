import datetime
from ..model.mdbModel import MdbModel

class FetchTestsThread:
  def __init__(self):
    self.mdb = MdbModel()
  
  def main(self):
    while True:
      startTime = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%s')
      self.mdb.testFindMany()