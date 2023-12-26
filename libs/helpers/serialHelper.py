import logging

class SerialHelper:
  def __init__(self, serial):
    self.serial = serial

  def _formatOutput(self, dataStr):
    rawDataHex = dataStr.encode().hex()
    processedData = '02' + rawDataHex + '03'
    bcc = 0
    for i in range(0, len(processedData), 2):
      bcc = bcc ^ processedData[i, i + 1]

    return processedData + bcc

  def main(self, rawData):
    data = rawData.decode("UTF-8")
    logging.info(data)
    match data:
      case b'\\x05':
        self.serial.write(b'\\x06')
      case _:
        self.readComplicatedData(data)

  def readComplicatedData(self, data):
    dataList = data.split(' ')

    match dataList[0]:
      case 'R':
        print('R')
      case 'D':
        print('D')
      case 'S':
        print('S')
      case _:
        print('other')

  def sendRequestMsg(self, data = {}):
    messageBodyDict = {
      "messageId": "W",
      "analyzer_id": data['analyzerId'],
      "specimen_category": data['specimenCategory'],
      "sample_no": data['sampleNo'],
      "patient_id": data['patientId'], 
      "reck_id": data['reckId'], 
      "position": data['position'], 
      "sample_type": data['sampleType'],
      "control_lot": data['controlLot'],
      "manual_dilution": data['manualDilution'], 
      "comment": data['comment'],
      "analyte_no": data['analyteNo'],
      "auto_dilution_ratio": data['autoDilutionRatio']
    }

    messageBodyStr = ''.join(messageBodyDict.values())
    encodedStr = self._formatOutput(messageBodyStr)
    self.serial.write(bytes(encodedStr, 'ascii'))

  def sendStatusQuery(self): 
    self.serial.write(self._formatOutput('Q1'.encode().hex()))

  def receiveResult(self, data):
    keys = [
      'message_id', 'analyzer_id', 'specimen_category', 'sample_no', 'sequence_no', 
      'patient_id', 'reck_id', 'position', 'sample_type', 'control_lot',
      'manual_dilution', 'comment', 'analyte_no', 'count_value', 'concentration_value',
      'judgment', 'remark', 'auto_dilution_ratio', 'cartridge_lot_no', 'substrate_lot_no',
      'measurement_date', 'measuring_time'
    ]

if __name__ == '__main__':
    print('serial helper')