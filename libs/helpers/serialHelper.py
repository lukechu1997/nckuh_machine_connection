import datetime

class SerialHelper:
  def __init__(self, serial):
    self.serial = serial

  def main(self, rawData):
    data = rawData.decode("UTF-8")
    match data:
      case "ENQ":
        self.serial.write("ACK".encode("UTF-8"))

if __name__ == '__main__':
    print('serial helper')