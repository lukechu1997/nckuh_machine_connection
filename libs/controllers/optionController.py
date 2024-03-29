from ..helpers.serialHelper import SerialHelper
from PyQt6 import QtSerialPort, QtGui, QtWidgets
from PyQt6.QtCore import QIODeviceBase, QDateTime, Qt
import os, sys
import dotenv
import logging

class OptionController:
  def __init__(self, wigets = None):
    self._wigets = wigets
    availablePorts = QtSerialPort.QSerialPortInfo.availablePorts()
    for port in availablePorts:
      self._wigets.serialPortOption.addItem(port.portName())
    
    try:
      self._wigets.serialPortOption.setCurrentText(os.environ.get('SERIAL_PORT', 'COM1'))
      self.__connectBtns()
      self.serial = QtSerialPort.QSerialPort()
      self.serialHelper = SerialHelper(self.serial)
      self.serial.readyRead.connect(self.__serialReadyRead)
      self.__setSerialPortName(os.environ.get('SERIAL_PORT', 'COM1'))
    except Exception as e:
      logging.debug('[optionController] init')
      logging.debug(e)
      logging.debug(sys.exc_info())

  def __serialReadyRead(self):
    buffer = self.serial.readAll().data()
    time = QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss  ")
    self._wigets.textBrowser.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    tc = self._wigets.textBrowser.textCursor()
    tc.movePosition(QtGui.QTextCursor.MoveOperation.End)
    if b'\x05' in buffer:
      tc.insertText(time + buffer.decode('utf-8'))
    self.serialHelper.main(buffer)

  def __setSerialPortName(self, port): 
    msgBox = QtWidgets.QMessageBox()
    if(self.serial.isOpen()):
      self.serial.close()

    self.serial.setPortName(port)
    self.serial.setBaudRate(9600)
    self.serial.setDataBits(QtSerialPort.QSerialPort.DataBits.Data8)
    self.serial.setParity(QtSerialPort.QSerialPort.Parity.NoParity)
    self.serial.setStopBits(QtSerialPort.QSerialPort.StopBits.OneStop)
    self.serial.setFlowControl(QtSerialPort.QSerialPort.FlowControl.NoFlowControl)

    if not self.serial.open(QIODeviceBase.OpenModeFlag.ReadWrite):
      msgBox.critical(None, '錯誤', '打開串口失敗: ' + self.serial.errorString())
      
    extDataDir = os.environ.get('EXT_DATA_DIR')
    dotenv.set_key(dotenv_path=os.path.join(extDataDir, '.env'), key_to_set='SERIAL_PORT', value_to_set=port)

  def __queryStatus(self):
    self.serialHelper.sendStatusQuery()
    
  def __connectBtns(self):
    # self._wigets.enqBtn.clicked.connect(lambda:self.__sendENQ())
    # self._wigets.ackBtn.clicked.connect(lambda:self.__sendACK())
    # self._wigets.eotBtn.clicked.connect(lambda:self.__sendEOT())
    self._wigets.statusBtn.clicked.connect(lambda:self.__queryStatus())
    self._wigets.selectPort.clicked.connect(lambda:self.__setSerialPortName(self._wigets.serialPortOption.currentText()))

  def setWiget(self, newWigets):
    self._wigets = newWigets
