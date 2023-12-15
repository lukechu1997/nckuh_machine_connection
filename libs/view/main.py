from ..model import mdbModel, sqliteModel
from PyQt6.QtWidgets import  QTableWidgetItem, QDialog
from PyQt6 import QtSerialPort
from PyQt6.QtCore import QIODeviceBase
# import libs.option as option

class UiFunc:
  def __init__(self, wigets):
    # self.mdbModel = mdbModel.MdbModel()
    # self.sqliteModel = sqliteModel.SqliteModel()    
    self.wigets = wigets
    self.funcInit()
    
  def serialInit(self, uiWigets):
    availablePorts = QtSerialPort.QSerialPortInfo.availablePorts()
    for port in availablePorts:
      uiWigets.serialPortOption.addItem(port.portName())
    
    self.serial = QtSerialPort.QSerialPort()

    # serialPortName = uiWigets.serialPortOption.currentText()
    uiWigets.buttonBox.accepted.connect(lambda:self.changeSerialPortName(uiWigets.serialPortOption.currentText()))
    
  def changeSerialPortName(self, port): 
    print(f'change serial port to {port}')
    if(self.serial.isOpen()):
      self.serial.close()

    self.serial.setPortName(port)

    self.serial.setBaudRate(9600)
    self.serial.setDataBits(QtSerialPort.QSerialPort.DataBits.Data8)
    self.serial.setParity(QtSerialPort.QSerialPort.Parity.NoParity)
    self.serial.setStopBits(QtSerialPort.QSerialPort.StopBits.OneStop)
    self.serial.setFlowControl(QtSerialPort.QSerialPort.FlowControl.NoFlowControl)

    if not self.serial.open(QIODeviceBase.OpenModeFlag.ReadWrite):
      print("错误", "打开串口失败:" + self.serial.errorString())

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

  # def onClickOptionBtn(self):
  #   # print('open option dialog')
  #   # self.wigets.optionUi.setupUi(self)
  #   # self.exec_()
  #   dialog = QDialog()
  #   dialog.ui = option.Ui_Dialog()
  #   dialog.ui.setupUi(dialog)
  #   dialog.exec_()

  def funcInit(self): 
    print('func init')
    # self.wigets.option.clicked.connect(lambda:self.onClickOptionBtn())
    # self.wigets.confirmBtn.clicked.connect(lambda:self.onClickConfirmBtn())
    # self.wigets.searchTests.clicked.connect(lambda:self.onClickSearchTests())