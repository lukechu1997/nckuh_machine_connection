import sqlite3
import os

class SqliteModel:
  def __init__(self):
    # try:
    #     conn = sqlite3.connect(os.environ.get('SQLITE_PATH'))
    #     self.conn = conn
    #     self.cursorObj = conn.cursor()
    # except sqlite3.Error:
    #     print('error!!!')
    #     print(sqlite3.Error)
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
    self.cursorObj.execute('''
      CREATE TABLE if not exists tests(
        id INTEGER PRIMARY KEY,
        sect_no TEXT,
        spec_kind TEXT,
        spec_no TEXT,
        sample_type TEXT,
        request_no TEXT,
        chart_no TEXT,
        name TEXT,
        sno TEXT,
        bottle_id TEXT,
        create_time DATETIME DEFAULT (datetime(CURRENT_TIMESTAMP, 'localtime'))
      );''')
    self.cursorObj.execute('''
      CREATE TABLE if not exists results(
        id INTEGER PRIMARY KEY,
        category TEXT,
        sample_no TEXT,
        sequence_no TEXT,
        patient_id TEXT,
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
    self.conn.commit()

  def testsFindMany(self, startTime, endTime):
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
  
  def updateResults(self, id, data):
    self.__connectDB()
    setStr = ','.join(map(lambda items: '='.join(items), data.items()))
    self.cursorObj.execute(f'''
      UPDATE results
      SET {setStr}
      WHERE ID = {id}
    ''')
    print(f'''
      UPDATE results
      SET {setStr}              
    ''')
    self.__disconnectDB()

  def insertTests(self, data):
    self.__connectDB()
    columns = "','".join(data.keys())
    values = "','".join(data.values())
    self.cursorObj.execute(f'''
      INSERT INTO tests ('{columns}')
      VALUES ('{values}');
    ''')
    self.__disconnectDB()
  
  def insertResults(self, data):
    print(data)
    self.__connectDB()
    columns = "','".join(data.keys())
    values = "','".join(data.values())
    sqlStr = f'''
      INSERT INTO results ('{columns}')
      VALUES ('{values}');
    '''
    print('sql str:', sqlStr)
    self.cursorObj.execute(sqlStr)
    self.__disconnectDB()
  
  def listTables(self):
    self.__connectDB()
    self.cursorObj.execute('SELECT name FROM sqlite_schema WHERE type ="table" AND name NOT LIKE "sqlite_%";')
    tables = self.cursorObj.fetchall()
    self.__disconnectDB()
    return tables
  
if __name__ == '__main__':
  print('sqlite connection')
  sql = SqliteModel()
  sql.dbInit()
