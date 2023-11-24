from ..model import mdbModel, sqliteModel
from PyQt6.QtWidgets import  QTableWidgetItem

class UiFunc:
  def __init__(self, wigets):
    self.mdbModel = mdbModel.MdbModel()
    self.sqliteModel = sqliteModel.SqliteModel()    
    self.wigets = wigets
    self.funcInit()
    

  def onClickConfirmBtn(self):
    print('clicked')

  def onClickSearchTests(self):
    startDate = self.wigets.testsStartDate.date().toString('yyyy/MM/dd')
    endDate = self.wigets.testsEndDate.date().toString('yyyy/MM/dd')
    testData = self.mdbModel.testFindMany(startDate, endDate)
    self.wigets.testsTable.setRowCount(len(testData))
    for index, data in enumerate(testData):
      self.wigets.testsTable.setItem(index, 0, QTableWidgetItem(str(data['SUID'])))
      self.wigets.testsTable.setItem(index, 1, QTableWidgetItem(data['TX_TIME'].strftime('%Y/%m/%d %H:%M:%S')))
      print({
        'id': data['SUID'],
        'txTime': data['TX_TIME'].strftime('%Y/%m/%d %H:%M:%S')
      })

  def funcInit(self): 
    self.wigets.confirmBtn.clicked.connect(lambda:self.onClickConfirmBtn())
    self.wigets.searchTests.clicked.connect(lambda:self.onClickSearchTests())