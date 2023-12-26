import pyodbc
import datetime

class MdbModel:
    def __init__(self):
        try:
            connStr = (
                r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};"
                r"DBQ=C:\\Program Files\\G1200\\dbs\\Automation.mdb;"
            )
            self.conn = pyodbc.connect(connStr)
            self.cursor = self.conn.cursor()
        except Exception:
            print('Exception', Exception)

    def 

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
    # mdbModel.testUpdate(213439)
    # mdbModel.resultInsert({
    #     'a': '一',
    #     'b': '二',
    #     'c': '三'
    # })
    # print(mdbModel.testFindMany(query={"startDate": "2021-10-14", "endDate": "2021-10-16"}))