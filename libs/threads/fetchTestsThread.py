import datetime
import logging
import time
from ..model.mdbModel import MdbModel
from ..model.sqliteModel import SqliteModel

class FetchTestsThread:
  def main(self):
    try:
      self.mdb = MdbModel()
      self.sqlite = SqliteModel()
      while True:
        endTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        startTime = (datetime.datetime.fromisoformat(endTime) - datetime.timedelta(minutes=10)).strftime('%Y-%m-%d %H:%M:%S')
        rawTestsData = self.mdb.testFindMany(startTime, endTime)
        # testsData = []
        if rawTestsData: 
          for data in rawTestsData :
            self.sqlite.insertTests({
              'sect_no': data['SECT_NO'],
              'spec_kind': data['SPEC_KIND'],
              'spec_year': data['SPEC_YEAR'],
              'spec_no': data['SPEC_NO'],
              'sample_type': data['SAMPLE_TYPE'],
              'request_no': data['REQUEST_NO'],
              'chart_no': data['CHART_NO'],
              'name': data['NAME'],
              'sno': data['SNO'],
              'bottle_id': data['BOTTLE_ID'],
            })
        # testsData = self.sqlite.testsFindMany(startTime, endTime)
        # print('testsData:', testsData)
        # print({"startTime": startTime, "endTime": endTime})
        time.sleep(600)
    except Exception as e:
      logging.critical(f'[Thread Exception] {e}')
      print('Thread Exception', e)