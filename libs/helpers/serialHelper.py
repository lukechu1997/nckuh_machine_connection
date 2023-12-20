import logging

class SerialHelper:
  def __init__(self, serial):
    self.serial = serial

  def main(self, rawData):
    data = rawData.decode("UTF-8")
    match data:
      case "ENQ":
        self.serial.write("ACK".encode("UTF-8"))
      case _:
        self.readComplicatedData(data)

  def readComplicatedData(self, data):
    logging.info(data)
    print(data)
    dataList = str.split(' ')

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
      "messageId": "W"
    }

    messageBodyStr = ' '.join(messageBodyDict.values())
    self.serial.write(messageBodyStr.encode("UTF-8"))

  def sendStatusQuery(self): 
    self.serial.write('Q 1'.encode("UTF-8"))

  def receiveResult(self, data):
    keys = [
      'message_id', 'analyzer_id', 'specimen_category', 'sample_no', 'sequence_no', 
      'patient_id', 'reck_id', 'position', 'sample_type', 
    ]

if __name__ == '__main__':
    print('serial helper')