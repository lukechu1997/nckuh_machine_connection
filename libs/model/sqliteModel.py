import sqlite3
import os
from sqlalchemy import create_engine, MetaData, select
from sqlalchemy import Table, Boolean, Column, DateTime, Integer, String
# from sqlalchemy.orm import declarative_base

# Base = declarative_base()

# class TestsTable(Base):
#   __tablename__ = 'Tests'
#   id = Column(Integer, primary_key=True),
#   sect_no = Column(String),
#   spec_kind = Column(String),
#   spec_year = Column(String),
#   spec_no = Column(String),
#   sample_type = Column(String),
#   request_no = Column(String),
#   chart_no = Column(String),
#   name = Column(String),
#   sno = Column(String),
#   bottle_id = Column(String),
#   create_time = Column(DateTime),


class SqliteModel():
  def __init__(self):
    # try:
    #   self.dbInit()
    #   self.engine = create_engine(f'sqlite:///{os.environ.get('SQLITE_PATH')}', echo=True)
    #   self.metadata = MetaData()
    #   self.resultsTable = Table('results', self.metadata)
    #   self.testsTable = Table('tests', self.metadata)
    # except Exception as e:
    #   print(e)
    self.__connectDB()
    self.dbInit()
    self.__disconnectDB()

  def __connectDB(self):
    try:
      conn = sqlite3.connect(os.environ.get('SQLITE_PATH'))
      self.conn = conn
      self.cursorObj = conn.cursor()
    except sqlite3.Error:
      print('error!!!')
      print(sqlite3.Error)
  
  def __disconnectDB(self):
    self.conn.commit()
    self.conn.close()

  def dbInit(self):
    conn = sqlite3.connect(os.environ.get('SQLITE_PATH'))
    cursorObj = conn.cursor()
  #   self.testsTable = Table(
  #     "tests",
  #     self.metadata,
  #     Column('id', Integer, primary_key=True),
  #     Column('sect_no', String),
  #     Column('spec_kind', String),
  #     Column('spec_year', String),
  #     Column('spec_no', String),
  #     Column('sample_type', String),
  #     Column('request_no', String),
  #     Column('chart_no', String),
  #     Column('name', String),
  #     Column('sno', String),
  #     Column('bottle_id', String),
  #     Column('create_time', DateTime),
  #   )
  #   self.resultsTable = Table(
  #     Column('id', Integer, primary_key=True),
  #     Column('category', String),
  #     Column('sample_no', String),
  #     Column('sequence_no', String),
  #     Column('sect_no', String),
  #     Column('spec_kind', String),
  #     Column('spec_year', String),
  #     Column('spec_no', String),
  #     Column('rack_id', String),
  #     Column('position', String),
  #     Column('sample_type', String),
  #     Column('control_lot', String),
  #     Column('manual_dilution', String),
  #     Column('comment', String),
  #     Column('analyte_no', String),
  #     Column('count_value', String),
  #     Column('concentration_value', String),
  #     Column('judgment', String),
  #     Column('remark', String),
  #     Column('auto_dilution_ratio', String),
  #     Column('cartridge_lot_no', String),
  #     Column('substrate_lot_no', String),
  #     Column('measurement_date', String),
  #     Column('measuring_time', String),
  #     Column('uploaded', Boolean),
  #     Column('create_time', String),
  #   )
  #   self.metadata.create_all(self.engine)
    cursorObj.execute('''
      CREATE TABLE if not exists tests(
        id INTEGER PRIMARY KEY,
        sect_no TEXT,
        spec_kind TEXT,
        spec_year TEXT,
        spec_no TEXT,
        sample_type TEXT,
        request_no TEXT,
        chart_no TEXT,
        name TEXT,
        sno TEXT,
        bottle_id TEXT,
        create_time DATETIME DEFAULT (datetime(CURRENT_TIMESTAMP, 'localtime'))
      );''')
    cursorObj.execute('''
      CREATE TABLE if not exists results(
        id INTEGER PRIMARY KEY,
        category TEXT,
        sample_no TEXT,
        sequence_no TEXT,
        patient_id TEXT,
        spec_year TEXT,
        rack_id TEXT,
        position TEXT,
        sample_type TEXT,
        control_lot TEXT,
        manual_dilution TEXT,
        comment TEXT,
        analyte_no TEXT,
        count_value TEXT,
        concentration_value TEXT,
        judgment TEXT,
        remark TEXT,
        auto_dilution_ratio TEXT,
        cartridge_lot_no TEXT,
        substrate_lot_no TEXT,
        measurement_date TEXT,
        measuring_time TEXT,
        uploaded NUMERIC DEFAULT 0,
        fk_test_id TEXT,
        create_time DATETIME DEFAULT (datetime(CURRENT_TIMESTAMP, 'localtime')),
        FOREIGN KEY (fk_test_id) REFERENCES tests(id)
      );''')
    # conn.commit()
    # conn.close()

  def testsFindMany(self, startTime, endTime):
    # with self.engine.connect() as connect:
    #   data = connect.execute(
    #     select(self.testsTable)
    #     .where(self.testsTable.columns['create_time'].between(startTime, endTime))
    #   )
    #   return data.mappings().all()
    self.__connectDB()
    print(f"SELECT * FROM tests WHERE create_time BETWEEN '{startTime}' AND '{endTime}'")
    self.cursorObj.execute(f"SELECT * FROM tests WHERE create_time BETWEEN '{startTime}' AND '{endTime}'")
    names = [description[0] for description in self.cursorObj.description]
    data = self.cursorObj.fetchall()
    print('tests data:', data)
    dataList = []
    for item in data:
      newItem = zip(names, item)
      dataList.append(dict((x, y) for x, y in newItem))

    self.__disconnectDB()
    return dataList
  
  def resultsFindMany(self, startTime, endTime):
    # with self.engine.connect() as connect:
    #   data = connect.execute(
    #     select(self.resultsTable)
    #     .where(self.testsTable.columns['create_time'].between(startTime, endTime))
    #   )
    #   return data.mappings().all()
    self.__connectDB()
    self.cursorObj.execute(f"SELECT * FROM results WHERE create_time BETWEEN '{startTime}' AND '{endTime}'")
    names = [description[0] for description in self.cursorObj.description]
    data = self.cursorObj.fetchall()
    dataList = []
    for item in data:
      newItem = zip(names, item)
      dataList.append(dict((x, y) for x, y in newItem))

    self.__disconnectDB()
    return dataList

  def insertTests(self, data):
    # with self.engine.connect() as connect:
    #   connect.execute(self.testsTable.insert(), data)
    #   connect.commit()
    self.__connectDB()
    columns = "','".join(data.keys())
    values = "','".join(data.values())
    self.cursorObj.execute(f'''
      INSERT INTO tests ('{columns}')
      VALUES ('{values}');
    ''')
    self.__disconnectDB()
  
  def insertResults(self, data):
    # print('insert results', data)
    # resultsTable = Table("results", self.metadata)
    # columnNamesList = resultsTable.columns.keys()
    # print(columnNamesList)
    # insertDict = {}
    # for name in columnNamesList:
    #   if name in ['id']:
    #     pass
    #   insertDict[name] = data[name]
    
    # print('insert data', insertDict)

    # with self.engine.connect() as connect:
    #   print(resultsTable.insert().values(insertDict))
    #   connect.execute(resultsTable.insert(), insertDict)
    #   connect.commit()
    self.__connectDB()
    columns = "','".join(data.keys())
    values = "','".join(data.values())
    sqlStr = f'''
      INSERT INTO results ('{columns}')
      VALUES ('{values}');
    '''
    self.cursorObj.execute(sqlStr)
    self.__disconnectDB()
  
if __name__ == '__main__':
  print('sqlite connection')
  sql = SqliteModel()
  sql.dbInit()
