import pyodbc
import datetime

class Odbc:
    def __init__(self):
        connStr = (
            r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};"
            r"DBQ=C:\\Projects\\新增資料夾\\test\\Automation.mdb;"
        )
        self.conn = pyodbc.connect(connStr)
        self.cursor = self.conn.cursor()

    def testFindMany(
        self, 
        query = {
            "startDate": (datetime.date.today() - datetime.timedelta(days=1)).strftime('%Y-%m-%d'),
            "endDate": datetime.date.today()
        }
    ):
        queryStr = f'SELECT * FROM Test WHERE TX_TIME BETWEEN {query["startTime"]} AND {query["startTime"]}'
        print(queryStr)
        
    def test(self):
        cursor = self.conn.cursor()
        for tableInfo in cursor.tables(tableType='TABLE'):
            print(tableInfo.table_name)

if __name__ == '__main__':
    print('mdb connection')