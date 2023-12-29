import os
from .optionController import OptionController
from ..helpers.serialHelper import SerialHelper
from ..model import mdbModel, sqliteModel
from ..view.option import Ui_Dialog as optionDialog
from datetime import date, timedelta
from PyQt6.QtWidgets import  QTableWidgetItem, QDialog
from PyQt6 import QtSerialPort, QtGui
from PyQt6.QtCore import QIODeviceBase, QDateTime, Qt

class MainController:
  def __init__(self, wigets):
    # self.mdbModel = mdbModel.MdbModel()
    self.sqliteModel = sqliteModel.SqliteModel()    
    self.wigets = wigets
    self.funcInit()
    # print('current time: ', QDateTime.currentDateTime())

  def __searchResults(self):
    startDate = self.wigets.testsStartDate.date().toString('yyyy-MM-dd')
    endDate = self.wigets.testsEndDate.date().toString('yyyy-MM-dd')
    resultData = self.sqliteModel.resultsFindMany(startDate, endDate)
    print('result data:', resultData)
    self.wigets.resultsTable.setRowCount(len(resultData))
    for index, data in enumerate(resultData):
      self.wigets.resultsTable.setItem(index, 0, QTableWidgetItem(str(data['id'])))
      self.wigets.resultsTable.setItem(index, 1, QTableWidgetItem(data['data']))

  def __searchTests(self):
    startDate = self.wigets.testsStartDate.date().toString('yyyy-MM-dd')
    endDate = self.wigets.testsEndDate.date().toString('yyyy-MM-dd')
    # testData = self.mdbModel.testFindMany(startDate, endDate)
    testData = self.sqliteModel.testsFindMany(startDate, endDate)
    print('test data:', testData)
    self.wigets.testsTable.setRowCount(len(testData))
    for index, data in enumerate(testData):
      self.wigets.testsTable.setItem(index, 0, QTableWidgetItem(str(data['id'])))
      self.wigets.testsTable.setItem(index, 1, QTableWidgetItem(data['create_time']))
    # for index, data in enumerate(testData):
    #   self.wigets.testsTable.setItem(index, 0, QTableWidgetItem(str(data['SUID'])))
    #   self.wigets.testsTable.setItem(index, 1, QTableWidgetItem(data['TX_TIME'].strftime('%Y/%m/%d %H:%M:%S')))
    #   print({
    #     'id': data['SUID'],
    #     'txTime': data['TX_TIME'].strftime('%Y/%m/%d %H:%M:%S')
    #   })

  # def __serialReadyRead(self):
  #   # buffer = self.serial.read(1024)
  #   buffer = self.serial.readAll()
  #   # buffer = buffer.decode("ascii")
  #   print('msg type: ', type(buffer))
  #   # buffer = str(buffer)
  #   print('buffer: ', buffer)
  #   print('decode to utf-8: ', buffer.decode('utf-8'))
  #   time = QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss  ")
  #   self.optionWigets.textBrowser.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
  #   tc = self.optionWigets.textBrowser.textCursor()
  #   tc.movePosition(QtGui.QTextCursor.MoveOperation.End)
  #   tc.insertText(time + buffer.decode('utf-8'))
  #   serialHelper = SerialHelper(self.serial)
  #   serialHelper.main(buffer)

  def __queryDateTimeInit(self):
    startDate = date.today()
    endDate = date.today() + timedelta(days=1)
    self.wigets.testsStartDate.setDate(startDate)
    self.wigets.testsEndDate.setDate(endDate)
    
  # def serialInit(self, wigets):
  #   availablePorts = QtSerialPort.QSerialPortInfo.availablePorts()
  #   for port in availablePorts:
  #     wigets.serialPortOption.addItem(port.portName())
    
  #   self.serial = QtSerialPort.QSerialPort()
  #   self.optionWigets = wigets
  #   wigets.selectPort.clicked.connect(lambda:self.changeSerialPortName(wigets.serialPortOption.currentText()))
  #   self.serial.readyRead.connect(self.__serialReadyRead)

  # def changeSerialPortName(self, port): 
  #   if(self.serial.isOpen()):
  #     self.serial.close()

  #   self.serial.setPortName(port)

  #   self.serial.setBaudRate(9600)
  #   self.serial.setDataBits(QtSerialPort.QSerialPort.DataBits.Data8)
  #   self.serial.setParity(QtSerialPort.QSerialPort.Parity.NoParity)
  #   self.serial.setStopBits(QtSerialPort.QSerialPort.StopBits.OneStop)
  #   self.serial.setFlowControl(QtSerialPort.QSerialPort.FlowControl.NoFlowControl)

  #   if not self.serial.open(QIODeviceBase.OpenModeFlag.ReadWrite):
  #     print("错误", "打开串口失败:" + self.serial.errorString())

  def onClickConfirmBtn(self):
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
    # self.wigets.confirmBtn.clicked.connect(lambda:self.onClickConfirmBtn())
    self.wigets.searchBtn.clicked.connect(lambda:self.onClickSearchBtn())
    self.wigets.option.clicked.connect(lambda:self.showOption())