import sqlite3
import os

class SqliteModel:
    def __init__(self):
        try:
            conn = sqlite3.connect(os.environ.get('SQLITE_PATH'))
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
            );
        ''')
        self.cursorObj.execute('''
            CREATE TABLE if not exists results(
                id INTEGER PRIMARY KEY,
                category TEXT,
                sample_no INTEGER,
                sequence_no INTEGER,
                patient_id INTEGER,
                rack_id INTEGER,
                position INTEGER,
                sample_type TEXT,
                control_lot INTEGER,
                manual_dilution INTEGER,
                comment TEXT,
                analyte_no INTEGER,
                count_value INTEGER,
                concentration_value INTEGER,
                judgment TEXT,
                remark TEXT,
                auto_dilution_ratio INTEGER,
                cartridge_lot_no INTEGER,
                substrate_lot_no INTEGER,
                measurement_date TEXT,
                measuring_time TEXT,
                uploaded NUMERIC DEFAULT 0,
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
    
    def updateResults(self, id, data):
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

    def insertTests(self, data):
        columns = ','.join(data.keys())
        values = ','.join(data.vakyes())
        self.cursorObj.execute(f'''
            INSERT INTO tests ({columns})
            VALUES ({values});
        ''')
    
    def insertResults(self, data):
        columns = ','.join(data.keys())
        values = ','.join(data.vakyes())
        self.cursorObj.execute(f'''
            INSERT INTO results ({columns})
            VALUES ({values});
        ''')
    
    def listTables(self):
        self.cursorObj.execute('SELECT name FROM sqlite_schema WHERE type ="table" AND name NOT LIKE "sqlite_%";')
        tables = self.cursorObj.fetchall()
        return tables
    
if __name__ == '__main__':
    print('sqlite connection')
    sql = SqliteModel()
    sql.dbInit()
