import sqlite3

class SqliteModel:
    def __init__(self):
        try:
            conn = sqlite3.connect('/Users/lukechu/projects/nckuh_machine_connection/db/g1200.db')
            self.conn = conn
            self.cursorObj = conn.cursor()
        except sqlite3.Error:
            print('error!!!')
            print(sqlite3.Error)

    def dbInit(self):
        self.cursorObj.execute('''
            CREATE TABLE tests(
                id INTEGER PRIMARY KEY,
                name TEXT,
                serial_no TEXT,
                create_time DATETIME DEFAULT (datetime(CURRENT_TIMESTAMP, 'localtime'))
            );
            CREATE TABLE results(
                id INTEGER PRIMARY KEY,
                data TEXT,
                fk_test_id INTEGER,
                create_time DATETIME DEFAULT (datetime(CURRENT_TIMESTAMP, 'localtime')),
                FOREIGN KEY (fk_test_id) REFERENCES tests(id)
            )
        ''')
        self.conn.commit()

    def testFindMany(self):
        self.cursorObj.execute('SELECT * FROM test')
        data = self.cursorObj.fetchall()
        return data
    
    def listTables(self):
        self.cursorObj.execute('SELECT name FROM sqlite_schema WHERE type ="table" AND name NOT LIKE "sqlite_%";')
        tables = self.cursorObj.fetchall()
        return tables
    
if __name__ == '__main__':
    print('sqlite connection')
    sql = SqliteModel()
    if len(sql.listTables()) == 0:
        sql.dbInit()
    
    print(sql.testFindMany())
