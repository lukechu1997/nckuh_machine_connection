from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6 import QtSerialPort
import PyQt6
from PyQt6.QtCore import QIODevice,QIODeviceBase
from PyQt6.QtCore import QDate, QTime, QDateTime, Qt

class Ui_Form(object):

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(791, 627)
        self.form = Form

        self.gridLayout_3 = QtWidgets.QGridLayout(Form)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.groupBox_2 = QtWidgets.QGroupBox(Form)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.textBrowser = QtWidgets.QTextBrowser(self.groupBox_2)
        self.textBrowser.setObjectName("textBrowser")
        self.gridLayout_4.addWidget(self.textBrowser, 0, 0, 1, 1)
        self.horizontalLayout_4.addWidget(self.groupBox_2)
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.comboBoxBaudrate = QtWidgets.QComboBox(self.groupBox)
        self.comboBoxBaudrate.setObjectName("comboBoxBaudrate")
        self.horizontalLayout_2.addWidget(self.comboBoxBaudrate)
        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 3)
        self.gridLayout.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.comboBoxSerialPort = QtWidgets.QComboBox(self.groupBox)
        self.comboBoxSerialPort.setObjectName("comboBoxSerialPort")
        self.horizontalLayout.addWidget(self.comboBoxSerialPort)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 3)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.btnOpenClose = QtWidgets.QPushButton(self.groupBox)
        self.btnOpenClose.setObjectName("btnOpenClose")
        self.horizontalLayout_3.addWidget(self.btnOpenClose)
        self.horizontalLayout_3.setStretch(0, 1)
        self.horizontalLayout_3.setStretch(1, 3)
        self.gridLayout.addLayout(self.horizontalLayout_3, 2, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.gridLayout.addItem(spacerItem, 3, 0, 1, 1)
        self.horizontalLayout_4.addWidget(self.groupBox)
        self.horizontalLayout_4.setStretch(0, 5)
        self.horizontalLayout_4.setStretch(1, 3)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.groupBox_3 = QtWidgets.QGroupBox(Form)
        self.groupBox_3.setObjectName("groupBox_3")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox_3)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.textEdit = QtWidgets.QTextEdit(self.groupBox_3)
        self.textEdit.setObjectName("textEdit")
        self.horizontalLayout_5.addWidget(self.textEdit)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.btnSend = QtWidgets.QPushButton(self.groupBox_3)
        self.btnSend.setMinimumSize(QtCore.QSize(0, 50))
        self.btnSend.setObjectName("btnSend")
        self.verticalLayout.addWidget(self.btnSend)
        self.btnClear = QtWidgets.QPushButton(self.groupBox_3)
        self.btnClear.setMinimumSize(QtCore.QSize(0, 50))
        self.btnClear.setObjectName("btnClear")
        self.verticalLayout.addWidget(self.btnClear)
        self.horizontalLayout_5.addLayout(self.verticalLayout)
        self.horizontalLayout_5.setStretch(0, 5)
        self.horizontalLayout_5.setStretch(1, 1)
        self.gridLayout_2.addLayout(self.horizontalLayout_5, 0, 0, 1, 1)
        self.verticalLayout_3.addWidget(self.groupBox_3)
        self.verticalLayout_3.setStretch(0, 4)
        self.verticalLayout_3.setStretch(1, 2)
        self.gridLayout_3.addLayout(self.verticalLayout_3, 0, 0, 1, 1)

        self.textBrowser.setLineWrapMode(QtWidgets.QTextBrowser.LineWrapMode.WidgetWidth)
        self.paraInit()

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
    def paraInit(self):
        availablePorts = QtSerialPort.QSerialPortInfo.availablePorts()
        self.comboBoxSerialPort.clear()
        for port in availablePorts:
            self.comboBoxSerialPort.addItem(port.portName())

        # 初始化波特率
        baudrates = QtSerialPort.QSerialPortInfo.standardBaudRates()
        self.comboBoxBaudrate.clear()
        for i in baudrates:
            self.comboBoxBaudrate.addItem(str(i))

        self.serial = QtSerialPort.QSerialPort()
        #连接信号与槽
        self.btnOpenClose.clicked.connect(self.btnOpenCloseClick)
        self.btnSend.clicked.connect(self.btnSendClick)
        self.btnClear.clicked.connect(self.btnClearClick)
        self.serial.readyRead.connect(self.serialReadyRead)
    def btnOpenCloseClick(self):
        if(self.serial.isOpen()):
            print("关闭串口")
            self.btnOpenClose.setText("打开串口")
            self.serial.close()
            self.comboBoxBaudrate.setEnabled(True)
            self.comboBoxSerialPort.setEnabled(True)
        else:
            print("打开串口")
            self.serial.setPortName(self.comboBoxSerialPort.currentText())
            self.serial.setBaudRate(int(self.comboBoxBaudrate.currentText()))
            self.serial.setDataBits(QtSerialPort.QSerialPort.DataBits.Data8)
            self.serial.setParity(QtSerialPort.QSerialPort.Parity.NoParity)
            self.serial.setStopBits(QtSerialPort.QSerialPort.StopBits.OneStop)
            self.serial.setFlowControl(QtSerialPort.QSerialPort.FlowControl.NoFlowControl)
            print(self.serial.portName())
            print(self.serial.baudRate())
            if(self.serial.open(QIODeviceBase.OpenModeFlag.ReadWrite)):
                self.btnOpenClose.setText("关闭串口")
                self.comboBoxBaudrate.setEnabled(False)
                self.comboBoxSerialPort.setEnabled(False)
            else:
                QtWidgets.QMessageBox.critical(self.form,"错误","打开串口失败:"+self.serial.errorString())




    def btnSendClick(self):
        text = self.textEdit.toPlainText()
        textByte = text.encode("UTF-8")
        self.serial.write(textByte)
    def btnClearClick(self):
        self.textEdit.clear()
    def serialReadyRead(self):
        print('serialReadyRead', self.serial)
        buffer = self.serial.read(1024)
        buffer = buffer.decode("UTF-8")
        time = QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss  ")
        # self.textBrowser.append(time+buffer)

        self.textBrowser.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        tc = self.textBrowser.textCursor()
        tc.movePosition(QtGui.QTextCursor.MoveOperation.End)
        tc.insertText(time+buffer)


    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.groupBox_2.setTitle(_translate("Form", "GroupBox"))
        self.groupBox.setTitle(_translate("Form", "GroupBox"))
        self.label_2.setText(_translate("Form", "波特率  ："))
        self.label.setText(_translate("Form", "串口选择："))
        self.label_3.setText(_translate("Form", "串口操作："))
        self.btnOpenClose.setText(_translate("Form", "打开串口"))
        self.groupBox_3.setTitle(_translate("Form", "GroupBox"))
        self.btnSend.setText(_translate("Form", "发送"))
        self.btnClear.setText(_translate("Form", "清空"))


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QWidget()

    ui = Ui_Form()  # 这个是类名，名字根据自定义的情况变化
    ui.setupUi(mainWindow)
    mainWindow.setWindowTitle("串口调试助手")
    mainWindow.show()
    sys.exit(app.exec())
