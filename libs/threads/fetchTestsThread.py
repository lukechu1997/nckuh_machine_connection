import datetime
import time
# from ..model.mdbModel import MdbModel
from ..model.sqliteModel import SqliteModel

class FetchTestsThread:
  def main(self):
    # self.mdb = MdbModel()
    try:
      self.sqlite = SqliteModel()
      while True:
        endTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        startTime = (datetime.datetime.fromisoformat(endTime) - datetime.timedelta(minutes=1)).strftime('%Y-%m-%d %H:%M:%S')
        # self.mdb.testFindMany(startTime, endTime)
        testsData = self.sqlite.testsFindMany(startTime, endTime)
        print('testsData:', testsData)
        print({"startTime": startTime, "endTime": endTime})
        time.sleep(60)
    except Exception:
      print(Exception)