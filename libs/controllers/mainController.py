import os
from .optionController import OptionController
from ..helpers.serialHelper import SerialHelper
from ..model import mdbModel, sqliteModel
from ..view.option import Ui_Dialog as optionDialog
from datetime import date, timedelta
from PyQt6.QtWidgets import  QTableWidgetItem, QDialog

class MainController:
  def __init__(self, wigets):
    self.mdbModel = mdbModel.MdbModel()
    self.sqliteModel = sqliteModel.SqliteModel()    
    self.wigets = wigets
    self.funcInit()

  def __searchResults(self):
    startDate = self.wigets.testsStartDate.date().toString('yyyy-MM-dd')
    endDate = self.wigets.testsEndDate.date().toString('yyyy-MM-dd')
    resultData = self.mdbModel.resultFindMany(startDate, endDate)
    self.wigets.resultsTable.setRowCount(len(resultData))
    for index, data in enumerate(resultData):
      self.wigets.resultsTable.setItem(index, 0, QTableWidgetItem(data['SECT_NO'] + data['SPEC_KIND'] + data['SPEC_NO']))	
      self.wigets.resultsTable.setItem(index, 1, QTableWidgetItem(data['TEST_VALUE']))
      self.wigets.resultsTable.setItem(index, 2, QTableWidgetItem(data['CompletedTime'].strftime('%Y/%m/%d %H:%M:%S')))

  def __searchTests(self):
    startDate = self.wigets.testsStartDate.date().toString('yyyy-MM-dd')
    endDate = self.wigets.testsEndDate.date().toString('yyyy-MM-dd')
    testData = self.mdbModel.testFindMany(startDate, endDate)
    self.wigets.testsTable.setRowCount(len(testData))
    for index, data in enumerate(testData):
      print(data)
      self.wigets.testsTable.setItem(index, 0, QTableWidgetItem(data['SECT_NO'] + data['SPEC_KIND'] + data['SPEC_NO']))
      self.wigets.testsTable.setItem(index, 1, QTableWidgetItem(data['TX_TIME'].strftime('%Y/%m/%d %H:%M:%S')))
      self.wigets.testsTable.setItem(index, 2, QTableWidgetItem(data['REQUEST_NO']))
      self.wigets.testsTable.setItem(index, 3, QTableWidgetItem(data['CHART_NO']))
      self.wigets.testsTable.setItem(index, 4, QTableWidgetItem(data['BEDNO']))

  def __queryDateTimeInit(self):
    startDate = date.today()
    endDate = date.today() + timedelta(days=1)
    self.wigets.testsStartDate.setDate(startDate)
    self.wigets.testsEndDate.setDate(endDate)

  def onClickConfirmBtn(self):
    for item in self.wigets.resultsTable.selectedItems():
      print(item.text())
    print('clicked')

  def onClickSearchBtn(self):
    self.__searchTests()
    self.__searchResults()

  def showOption(self):
    print('open option dialog')
    self.window = QDialog()
    dialog = optionDialog()
    dialog.setupUi(self.window)
    self.window.show()   
    OptionController(dialog)

  def funcInit(self): 
    print('func init')
    self.__queryDateTimeInit()
    # self.wigets.confirmBtn.clicked.connect(self.onClickConfirmBtn)
    self.wigets.searchBtn.clicked.connect(lambda:self.onClickSearchBtn())
    self.wigets.option.clicked.connect(lambda:self.showOption())
