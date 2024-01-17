import datetime
import dotenv
import logging
import pyodbc
import os
import sqlalchemy

class MdbModel:
  def __init__(self):
    try:
      accessPath = os.environ.get('ACCESS_PATH')
      connStr = (
        r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};"
        f"DBQ={accessPath if accessPath else '.\Automation.mdb'};"
        r"ExtendedAnsiSQL=1;"
      )

      connectionUrl = sqlalchemy.engine.URL.create(
        "access+pyodbc",
        query={"odbc_connect": connStr}
      )
      self.engine = sqlalchemy.create_engine(connectionUrl)
      # self.conn = pyodbc.connect(connStr)
      # self.cursor = self.conn.cursor()
    except Exception as e:
      logging.critical(f'[Mdb Exception] {e}')
      print('Mdb Exception', e)

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
    queryStr = f"SELECT * FROM TEST WHERE [SPEC_KIND] = '{data['specKind']}' AND [SPEC_YEAR] = '{data['specYear']}' AND [SPEC_NO] = '{data['specNo']}';"
    self.cursor.execute(queryStr)
    columns = [column[0] for column in self.cursor.description]
    data = self.cursor.fetchone()
    resData = {}
    if data:
      resData = dict(zip(columns, data))

    return resData
    
  def testFindMany(
    self, 
    startTime = (datetime.date.today() - datetime.timedelta(days=1)).strftime('%Y-%m-%d'),
    endTime = datetime.date.today()
  ):
    queryStr = 'SELECT * FROM Test WHERE [TX_TIME] BETWEEN ? AND ?;'
    self.cursor.execute(queryStr, startTime, endTime)
    columns = [column[0] for column in self.cursor.description]
    data = []
    for row in self.cursor.fetchall():
      data.append(dict(zip(columns, row)))
    
    return data
  
  def testUpdate(self, id, data):
    queryStr = f'UPDATE Test SET ? WHERE SUID = ?'
    self.cursor.execute(
      queryStr, 
      ','.join(map(lambda items: '='.join(items), data.items())),
      id
    )
    self.cursor.commit()

  def resultInsert(self, dataDict = {}):
    self.engine.begine().execute(sqlalchemy.insert('Result'), dataDict)
    
    # queryStr = f"INSERT INTO Result ({','.join(dataDict.keys())}) VALUES ('{"','".join(dataDict.values())}')"
    # print(queryStr)
    # self.cursor.execute(
    #   queryStr
    # )
    # self.cursor.commit()
  
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
  mdbModel.test()