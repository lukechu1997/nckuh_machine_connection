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
      case b'\x04':
        logging.info('[EOT]')
      case b'\x05':
        self.sendSingle('ACK')
        logging.info('[ENQ]')
      case b'\x06':
        self.sendSingle('EOT')
        logging.info('[ACK]')
      case _:
        self.readComplicatedData(data)

  def readComplicatedData(self, data):
    match data[0]:
      case 'R':
        self.receiveQuery(data)
      case 'D':
        self.receiveResult(data)
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

  def receiveQuery(self, data):
    keys = [
      'message_id', 'analyzer_id', 'patient_id', 'reck_id', 'sample_no', 'sample_category'
    ]

  def receiveResult(self, data):
    keys = [
      'message_id', 'analyzer_id', 'specimen_category', 'sample_no', 'sequence_no', 
      'patient_id', 'reck_id', 'position', 'sample_type', 'control_lot',
      'manual_dilution', 'comment', 'analyte_no', 'count_value', 'concentration_value',
      'judgment', 'remark', 'auto_dilution_ratio', 'cartridge_lot_no', 'substrate_lot_no',
      'measurement_date', 'measuring_time'
    ]

  def receiveStatus(self, data):
    dataDect = {
      'message_id': data[0], 
      'analyzer_id': data[1], 
      'status': data[2]
    }

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