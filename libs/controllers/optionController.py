from ..helpers.serialHelper import SerialHelper
from PyQt6 import QtSerialPort, QtGui
from PyQt6.QtCore import QIODeviceBase, QDateTime, Qt
import os
import dotenv

class OptionController:
  def __init__(self, wigets = None):
    self._wigets = wigets
    availablePorts = QtSerialPort.QSerialPortInfo.availablePorts()
    for port in availablePorts:
      self._wigets.serialPortOption.addItem(port.portName())
    
    self._wigets.serialPortOption.setCurrentText(os.environ.get('SERIAL_PORT'))
    self.__connectBtns()
    self.serial = QtSerialPort.QSerialPort()
    self.serialHelper = SerialHelper(self.serial)
    self.serial.readyRead.connect(self.__serialReadyRead)
    self.__setSerialPortName(os.environ.get('SERIAL_PORT'))

  def __serialReadyRead(self):
    # buffer = self.serial.read(1024)
    buffer = self.serial.readAll().data()
    print('buffer: ', buffer)
    time = QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss  ")
    self._wigets.textBrowser.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    tc = self._wigets.textBrowser.textCursor()
    tc.movePosition(QtGui.QTextCursor.MoveOperation.End)
    tc.insertText(time + buffer.decode('utf-8'))
    self.serialHelper.main(buffer)

  def __setSerialPortName(self, port): 
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

    dotenv.set_key('.env', 'SERIAL_PORT', port)

  def __sendENQ(self):
    print('send enq')
    self.serialHelper.sendSingle('ENQ')

  def __sendACK(self):
    print('send ack')
    self.serialHelper.sendSingle('ACK')

  def __sendEOT(self):
    print('send eot')
    self.serialHelper.sendSingle('EOT')

  def __queryStatus(self):
    self.serialHelper.sendStatusQuery()
    
  def __connectBtns(self):
    self._wigets.enqBtn.clicked.connect(lambda:self.__sendENQ())
    self._wigets.ackBtn.clicked.connect(lambda:self.__sendACK())
    self._wigets.eotBtn.clicked.connect(lambda:self.__sendEOT())
    self._wigets.statusBtn.clicked.connect(lambda:self.__queryStatus())
    self._wigets.selectPort.clicked.connect(lambda:self.__setSerialPortName(self._wigets.serialPortOption.currentText()))

  def setWiget(self, newWigets):
    self._wigets = newWigets
