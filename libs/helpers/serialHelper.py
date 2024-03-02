import logging
import sys
from ..model.sqliteModel import SqliteModel
from ..model.mdbModel import MdbModel
from datetime import datetime

class SerialHelper:
  def __init__(self, serial):
    print('serial helper init')
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
    data = rawData.split(b'\x02')[1].split(b'\x03')[0]

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
        elif self.status == 'STATUS':
          self.sendStatusQuery()
        else:
          self.sendSingle('EOT')
        logging.info('[ACK]')
      case _:
        if self.tempData == '' and b'\x02' not in rawData:
          return
        self.tempData = self.tempData + rawData
        if b'\x03' in self.tempData:
          self.readComplicatedData(self.tempData)
          self.tempData = b''

  def readComplicatedData(self, rawData):
    logging.info(rawData)
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
      self.status = 'IDLE'
    else:
      self.status = 'STATUS'
      self.sendSingle('ENQ')
    
  def receiveQuery(self, data):
    dataDict = {
      'message_id': data[0],
      'analyzer_id': data[1],
      'patient_id': data[2:28],
      # 'rack_id': data[29:35],
      # 'sample_no': data[-1],
      # 'sample_category': data[-1]
    }
    logging.info(data)

    barCode = dataDict['patient_id'].replace(' ', '')

    self.tempRequestData = self.mdb.testFindUnique({
      'specNo': barCode[2:8]
    })

    self.sendSingle('ACK')
    self.status = 'REQUEST'
    # self.tempData = b''
    
    if len(self.tempRequestData.keys()) == 0:
      return
    
    self.mdb.testUpdate(self.tempRequestData['SUID'], 
                        {
                          'TX_TIME': datetime.now(),
                          'DOWNLOAD_TIME': datetime.now(),
                          'STATE': 'P'
                        })

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
      'measuring_time': data[118:],
      'spec_year': datetime.now().strftime('%y'),
    }

    for key, value in dataDict.items():
      dataDict[key] = value.replace(' ', '')
    logging.info(dataDict)
    self.sqlite.insertResults(dataDict)
    if dataDict['category'] == 'C':
      specNo = 1 if int(dataDict['position']) % 2 == 1 else 2
      testData = {
        'SECT_NO': 'QC',
        'SAMPLE_TYPE': 'Q',
        'CHART_NO': dataDict['control_lot'],
        'SPEC_NO': f'PIVKA-ⅡL{specNo}'
      }
    else:
      testData = self.mdb.testFindUnique({
        'specNo': dataDict['patient_id'][2:8]
      }) 

    if dataDict['concentration_value'] == '75000' and (dataDict['remark'] == '0000020004000000' or dataDict['remark'] == '0000000004000000' ):
      dataDict['concentration_value'] = '>75000'

    try:
      self.mdb.resultInsert({
        'SECT_NO': testData['SECT_NO'] if 'SECT_NO' in testData else dataDict['patient_id'][0:2],
        'SPEC_KIND': testData['SPEC_KIND'] if 'SPEC_KIND' in testData else '',
        'SPEC_YEAR': testData['SPEC_YEAR'] if 'SPEC_YEAR' in testData else datetime.now().strftime('%y'),
        'SPEC_NO': dataDict['patient_id'][2:8] if dataDict['category'] != 'C' else testData['SPEC_NO'],
        'SAMPLE_TYPE': testData['SAMPLE_TYPE'] if 'SAMPLE_TYPE' in testData else '',
        'RERUN_COUNT': testData['RERUN_COUNT'] if 'RERUN_COUNT' in testData else 0,
        'TX_TIME': testData['TX_TIME'] if 'TX_TIME' in testData else datetime.fromisoformat(dataDict['measurement_date'] + 'T' + dataDict['measuring_time']),
        'REQUEST_NO': testData['REQUEST_NO'] if 'REQUEST_NO' in testData else '',
        'CHART_NO': testData['CHART_NO'] if 'CHART_NO' in testData else '',
        'NAME': testData['NAME'] if 'NAME' in testData else '',
        'SNO': testData['SNO'] if 'SNO' in testData else '',
        'BOTTLE_ID': '',
        'TEST_NAME': '8210PIVKA-Ⅱ',
        'TEST_VALUE': dataDict['concentration_value'],
        'TRANS_VALUE': testData['TRANS_VALUE'] if 'TRANS_VALUE' in testData else '',
        # 'MIC_VALUE': '',
        'DILUTION': 1, 
        'DILUTION_VALUE': '1',
        'RACK_NO': dataDict['rack_id'],
        'TUBE_NO': dataDict['position'],
        # 'MACHINE_SNO': dataDict[],
        'MACHINE_ID': 'G1200',
        'ERROR_CODE': '',
        'ERROR_MSG': '',
        'TEST_CODE': 'PIVKA-Ⅱ',
        'TEST_CODE_NAME': 'PIVKA-Ⅱ',
        'STATE': 'P',
        'UPLOAD_TIME': datetime.now(),
        'StartedTime': datetime.fromisoformat(dataDict['measurement_date'] + 'T' + dataDict['measuring_time']),
        'CompletedTime': datetime.now()
      })
      if dataDict['category'] != 'C' and (len(testData.keys()) != 0 and not testData['DOWNLOAD_TIME']):
        self.mdb.testUpdate(testData['SUID'], {'STATE': 'P','DOWNLOAD_TIME': datetime.now()})
    except Exception as e:
      logging.critical('[serial helper] mdb insert fail')
      logging.critical(e)
      logging.critical(sys.exc_info())
    # reset tempData and status
    # self.tempData = b''
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
    # self.tempData = b''

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