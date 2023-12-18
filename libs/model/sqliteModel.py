import sqlite3

class SqliteModel:
    def __init__(self):
        try:
            conn = sqlite3.connect('./db/g1200.db')
            self.conn = conn
            self.cursorObj = conn.cursor()
        except sqlite3.Error:
            print('error!!!')
            print(sqlite3.Error)
        
        self.dbInit()

    def dbInit(self):
        self.cursorObj.execute('''
            CREATE TABLE if not exists tests(
                id INTEGER PRIMARY KEY,
                name TEXT,
                serial_no TEXT,
                create_time DATETIME DEFAULT (datetime(CURRENT_TIMESTAMP, 'localtime'))
            );
        ''')
        # 將data拆分
        self.cursorObj.execute('''
            CREATE TABLE if not exists results(
                id INTEGER PRIMARY KEY,
                data TEXT,
                uploaded NUMERIC,
                fk_test_id INTEGER,
                create_time DATETIME DEFAULT (datetime(CURRENT_TIMESTAMP, 'localtime')),
                FOREIGN KEY (fk_test_id) REFERENCES tests(id)
            );
        ''')
        self.conn.commit()

    def testsFindMany(self, startDate, endDate):
        self.cursorObj.execute(f"SELECT * FROM tests WHERE create_time BETWEEN '{startDate}' AND '{endDate}'")
        names = [description[0] for description in self.cursorObj.description]
        data = self.cursorObj.fetchall()
        dataList = []
        for item in data:
            newItem = zip(names, item)
            dataList.append(dict((x, y) for x, y in newItem))

        self.conn.commit()
        return dataList
    
    def resultsFindMany(self, startDate, endDate):
        self.cursorObj.execute(f"SELECT * FROM results WHERE create_time BETWEEN '{startDate}' AND '{endDate}'")
        names = [description[0] for description in self.cursorObj.description]
        data = self.cursorObj.fetchall()
        dataList = []
        for item in data:
            newItem = zip(names, item)
            dataList.append(dict((x, y) for x, y in newItem))

        self.conn.commit()
        return dataList
    
    def listTables(self):
        self.cursorObj.execute('SELECT name FROM sqlite_schema WHERE type ="table" AND name NOT LIKE "sqlite_%";')
        tables = self.cursorObj.fetchall()
        return tables
    
if __name__ == '__main__':
    print('sqlite connection')
    sql = SqliteModel()
    sql.dbInit()