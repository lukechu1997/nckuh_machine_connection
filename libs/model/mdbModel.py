import datetime
import logging
import os
from sqlalchemy import engine, create_engine, MetaData
from sqlalchemy import select, Table, update, desc
import sqlalchemy_access as sa_a
import sqlalchemy_access.pyodbc as sa_a_pyodbc

class MdbModel:
  def __init__(self):
    try:
      accessPath = os.environ.get('ACCESS_PATH')
      connStr = (
        r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};"
        f"DBQ={accessPath if accessPath else 'Automation.mdb'};"
        r"ExtendedAnsiSQL=1;"
      )
      connectionUrl = engine.URL.create(
        "access+pyodbc",
        query={"odbc_connect": connStr}
      )
      self.engine = create_engine(connectionUrl)
      self.metadata = MetaData()
      self.metadata.reflect(self.engine)
    except Exception as e:
      logging.critical(f'[Mdb Exception] {e}')
      print('Mdb Exception', e)

  def testFindUnique(self, data):
    testTable = Table("Test", self.metadata)
    with self.engine.connect() as conn:
      data = conn.execute(select(testTable)
              # .where(testTable.columns.SPEC_KIND == data['specKind'])
              # .where(testTable.columns.SPEC_YEAR == data['specYear'])
              .where(testTable.columns.SPEC_NO == data['specNo'])
              .order_by(desc(testTable.columns.SUID))
              ).mappings().first()
      return data if data else {}
    
  def testFindMany(
    self, 
    startTime = (datetime.date.today() - datetime.timedelta(days=1)).strftime('%Y-%m-%d'),
    endTime = datetime.date.today()
  ):
    testTable = Table("Test", self.metadata)
    with self.engine.connect() as conn:
      data = conn.execute(select(testTable).where(testTable.columns.TX_TIME.between(startTime, endTime)))
      return data.mappings().all()
  
  def testUpdate(self, id, data):
    testTable = Table("Test", self.metadata)
    updateValues = {}
    for key, val in data.items():
      updateValues[testTable.columns[key]] = val

    with self.engine.connect() as conn:
      conn.execute(update(testTable)
            .where(testTable.columns.SUID == id)
            .values(updateValues))
      conn.commit()

  def resultFindMany(
    self, 
    startTime = (datetime.date.today() - datetime.timedelta(days=1)).strftime('%Y-%m-%d'),
    endTime = datetime.date.today()
  ):
    resultTable = Table("Result", self.metadata)
    with self.engine.connect() as conn:
      data = conn.execute(select(resultTable).where(resultTable.columns['TX_TIME'].between(startTime, endTime)))
      return data.mappings().all()

  def resultInsert(self, dataDict = {}):
    resultTable = Table("Result", self.metadata)
    logging.info('insert result')
    logging.info(dataDict)
    with self.engine.connect() as conn:
      conn.execute(resultTable.insert(), dataDict)
      conn.commit()
  
  def resultUpdate(self, data):
    testTable = Table("Result", self.metadata)
    updateValues = {}
    for key, val in data.items():
      updateValues[testTable.columns[key]] = val

    with self.engine.connect() as conn:
      conn.execute(update(testTable)
            .where(testTable.columns.SUID == id)
            .values(updateValues))
      conn.commit()
      
  def test(self):
    cursor = self.conn.cursor()
    for tableInfo in cursor.tables(tableType='TABLE'):
      print(tableInfo.table_name)

if __name__ == '__main__':
  print('mdb connection')
  mdbModel = MdbModel()
  