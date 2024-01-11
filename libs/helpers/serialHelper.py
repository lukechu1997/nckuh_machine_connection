import logging
from ..model.sqliteModel import SqliteModel
from ..model.mdbModel import MdbModel

class SerialHelper:
  def __init__(self, serial):
    self.serial = serial
    self.sqlite = SqliteModel()
    self.mdb = MdbModel()
    self.tempData = b''
    self.tempRequestData = {}
    self.status = 'IDLE'

  def __formatOutput(self, dataStr):
    rawDataHex = dataStr.encode('ascii').hex()
    processedData = rawDataHex + '03'
    bcc = hex(0)
    for i in range(0, len(processedData), 2):
      bcc = hex(int(bcc, 16) ^ int(processedData[i:i + 2], 16))

    return bytearray.fromhex('02' + processedData + bcc[2:].encode('ascii').hex())

  def __trimIncomingData(self, rawData):
    data = rawData.replace(b'\x02', b'').split(b'\x03')[0]
    return data.decode('utf-8')

  def main(self, rawData):
    # estabilish connection
    match rawData:
      case b'\x04':
        logging.info('[EOT]')
        if self.status == 'REQUEST':
          self.sendSingle('ENQ')
          
        return
      case b'\x05':
        self.sendSingle('ACK')
        logging.info('[ENQ]')
        return
      case b'\x06':
        if self.status == 'REQUEST':
          self.sendRequestMsg(self.tempRequestData)
        else:
          self.sendSingle('EOT')

        logging.info('[ACK]')
      case _:
        self.tempData = self.tempData + rawData
        if b'\x03' in self.tempData:
          self.readComplicatedData(self.tempData)

  def readComplicatedData(self, rawData):
    data = self.__trimIncomingData(rawData)
    match data[0]:
      case 'R':
        self.status = 'QUERY'
        self.receiveQuery(data)
      case 'D':
        self.status = 'RESULT'
        self.receiveResult(data)
      case 'S':
        self.status = 'STATUS'
        self.receiveStatus(data)
      case _:
        print('other')

  def sendRequestMsg(self, data = {}):
    # write assay request
    messageBodyDict = {
      "messageId": 'W',
      "analyzer_id": 1,
      "specimen_category": 'N',
      "sample_no": data['sampleNo'].rjust(4, ' '),
      "patient_id": data['patientId'].ljust(26, ' '), 
      "rack_id": ' ' * 4, 
      "position": ' ', 
      "sample_type": data['sampleType'],
      "control_lot": ' ' * 8,
      "manual_dilution": data['manualDilution'].ljust(4, ' '), 
      # "comment": data['comment'],
      "num_of_analytes": '',
      "analyte_no": '11',
      "auto_dilution_ratio": data['autoDilutionRatio']
    }

    messageBodyStr = ''.join(messageBodyDict.values())
    encodedStr = self.__formatOutput(messageBodyStr)
    self.serial.write(bytes(encodedStr, 'ascii'))

    # reset status and temp data
    self.status = 'IDLE'
    self.tempRequestData = {}

  def sendStatusQuery(self): 
    if self.status == 'STATUS':
      self.serial.write(self.__formatOutput('Q1'))
    else:
      self.status = 'STATUS'
      self.sendSingle('ENQ')
    
  def receiveQuery(self, data):
    dataDict = {
      'message_id': data[1],
      'analyzer_id': data[2],
      'patient_id': data[3:29],
      'rack_id': data[29:35],
      'sample_no': data[35:38],
      # 'sample_category': data[1]
    }
    logging.info(data)

    barCode = dataDict['patient_id'].replace(' ', '')

    self.tempRequestData = self.mdb.testFindUnique({
      'specKind': barCode[0:2],
      'specYear': barCode[2:4],
      'specNo': barCode[4:]
    })
    self.sendSingle('ACK')
    self.status = 'REQUEST'

  def receiveResult(self, data):
    self.sendSingle('ACK')
    dataDict = {
      # 'message_id': data[0],
      # 'analyzer_id': data[1],
      'category': data[2],
      'sample_no': data[3:7],
      'sequence_no': data[7:11],
      'patient_id': data[11:37],
      'rack_id': data[37:41],
      'position': data[41],
      'sample_type': data[42],
      'control_lot': data[43:51],
      'manual_dilution': data[51:55],
      # 'comment': data[],
      'analyte_no': data[55:57],
      'count_value': data[57:65],
      'concentration_value': data[65:75],
      'judgment': data[75:85],
      'remark': data[85:101],
      'auto_dilution_ratio': data[101],
      'cartridge_lot_no': data[102:106],
      'substrate_lot_no': data[106:110],
      'measurement_date': data[110:118],
      'measuring_time': data[118:]
    }

    for key, value in dataDict.items():
      dataDict[key] = value.replace(' ', '')
    logging.info(data)
    self.sqlite.insertResults(dataDict)
    # reset tempData and status
    self.tempData = b''
    self.status = 'IDLE'

  def receiveStatus(self, data):
    dataDect = {
      'message_id': data[0], 
      'analyzer_id': data[1], 
      'status': data[2]
    }
    logging.info(dataDect)
    self.sendSingle('ACK')
    self.status = 'IDLE'

  def sendSingle(self, type):
    match type:
      case 'ACK':
        self.serial.write(b'\x06')
      case 'EOT':
        self.serial.write(b'\x04')
      case 'ENQ':
        self.serial.write(b'\x05')

if __name__ == '__main__':
    print('serial helper')