import datetime
import dotenv
import logging
import pyodbc
import os

class MdbModel:
  def __init__(self):
    try:
      accessPath = os.environ.get('ACCESS_PATH')
      connStr = (
        r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};"
        f"DBQ={accessPath};"
      )
      self.conn = pyodbc.connect(connStr)
      self.cursor = self.conn.cursor()
    except Exception:
      print('Exception', Exception)

  def updateAccessPath(self, accessPath):
    try:
      self.conn.close()
      connStr = (
        r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};"
        f"DBQ={accessPath};"
      )
      self.conn = pyodbc.connect(connStr)
      self.cursor = self.conn.cursor()
      dotenv.set_key('.env', 'ACCESS_PATH', accessPath)
    except Exception:
      logging.critical(Exception)
      print('Exception: ', Exception)

  def testFindUnique(self, data):
    queryStr = 'SELECT * FROM TEST WHERE [SPEC_KIND] = "?" AND [SPEC_YEAR] = "?" AND [SPEC_NO] = "?";'
    self.cursor.execute(queryStr, data['specKind'], data['specYear'], data['specNo'])
    columns = [column[0] for column in self.cursor.description]
    data = self.cursor.fetchone()
    # for row in self.cursor.fetch():
    #   data.append(dict(zip(columns, row)))
    
    return dict(zip(columns, data))
  
  def testFindMany(
    self, 
    startDate = (datetime.date.today() - datetime.timedelta(days=1)).strftime('%Y-%m-%d'),
    endDate = datetime.date.today()
  ):
    queryStr = 'SELECT * FROM Test WHERE [TX_TIME] BETWEEN ? AND ?;'
    self.cursor.execute(queryStr, startDate, endDate)
    columns = [column[0] for column in self.cursor.description]
    data = []
    for row in self.cursor.fetchall():
      data.append(dict(zip(columns, row)))
    
    return data
  
  def testUpdate(self, id):
    queryStr = 'UPDATE Test SET DOWNLOAD_TIME = ? WHERE SUID = ?'
    self.cursor.execute(
      queryStr, 
      datetime.datetime.now(),
      id
    )
    self.cursor.commit()

  def resultInsert(self, dataDict = {}):
    queryStr = 'INSERT INTO Result (?) VALUES (?)'
    self.cursor.execute(
      queryStr,
      ', '.join(dataDict.keys()),
      ', '.join(dataDict.values())
    )
    self.cursor.commit()
  
  def resultUpdate(self, dataDict):
    queryStr = 'INSERT INTO Result (?) VALUES (?)'
    self.cursor.execute(
      queryStr,
      ', '.join(dataDict.keys()),
      ', '.join(dataDict.values())
    )
    self.cursor.commit()
      
  def test(self):
    cursor = self.conn.cursor()
    for tableInfo in cursor.tables(tableType='TABLE'):
      print(tableInfo.table_name)

if __name__ == '__main__':
  print('mdb connection')
  mdbModel = MdbModel()