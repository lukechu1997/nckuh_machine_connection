import logging

class SerialHelper:
  def __init__(self, serial):
    self.serial = serial

  def __formatOutput(self, dataStr):
    rawDataHex = dataStr.encode('ascii').hex()
    processedData = '02' + rawDataHex + '03'
    bcc = int('00', 16)
    for i in range(0, len(processedData), 2):
      bcc = bcc ^ int(processedData[i:i + 1], 16)

    return bytearray.fromhex(processedData + str(bcc).rjust(2, '0'))

  def __trimIncomingData(self, rawData):
    data = rawData.replace(b'\x02', b'').split(b'\x03')[0]
    return data.decode('utf-8')

  def main(self, rawData):
    data = rawData.decode("UTF-8")
    logging.info(data)
    match rawData:
      case b'\x04':
        logging.info('[EOT]')
      case b'\x05':
        self.sendSingle('ACK')
        logging.info('[ENQ]')
      case b'\x06':
        # self.sendSingle('EOT')
        logging.info('[ACK]')
      case _:
        self.readComplicatedData(rawData)

  def readComplicatedData(self, rawData):
    data = self.__trimIncomingData(rawData)
    match data[0]:
      case 'R':
        self.receiveQuery(data)
      case 'D':
        self.receiveResult(data)
      case 'S':
        self.receiveStatus(data)
      case _:
        print('other')

  def sendRequestMsg(self, data = {}):
    self.sendSingle('ENQ')
    # wait for ack

    # write assay request
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
    encodedStr = self.__formatOutput(messageBodyStr)
    self.serial.write(bytes(encodedStr, 'ascii'))

    # self.serial.write(encodedStr)

    # wait ack

    # send eot

  def sendStatusQuery(self): 
    self.sendSingle('ENQ')
    # wait for ack
    if self.serial.read(1024) == b'\x06':
      print('receive ack')
    # while True:
    #     break
    self.serial.write(self.__formatOutput('Q1'.encode().hex()))

  def receiveQuery(self, data):
    keys = [
      'message_id', 'analyzer_id', 'patient_id', 'reck_id', 'sample_no', 'sample_category'
    ]
    print('query data:', data)
    logging.info(data)
    self.sendSingle('ACK')
    # wait eot (?)

    # send request
    # self.sendRequest

  def receiveResult(self, data):
    keys = [
      'message_id', 'analyzer_id', 'specimen_category', 'sample_no', 'sequence_no', 
      'patient_id', 'reck_id', 'position', 'sample_type', 'control_lot',
      'manual_dilution', 'comment', 'analyte_no', 'count_value', 'concentration_value',
      'judgment', 'remark', 'auto_dilution_ratio', 'cartridge_lot_no', 'substrate_lot_no',
      'measurement_date', 'measuring_time'
    ]
    print('result data:', data)
    logging.info(data)
    self.sendSingle('ACK')
    # wait eot (?)

  def receiveStatus(self, data):
    dataDect = {
      'message_id': data[0], 
      'analyzer_id': data[1], 
      'status': data[2]
    }
    logging.info(data)
    self.sendSingle('ACK')
    # wait eot (?)

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