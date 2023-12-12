import serial, time

class SerialHelper:
    
    def __init__(self):
        self.ser = serial.Serial()
        try:
            self.ser.open()
        except Exception as ex:
            print ("open serial port error " + str(ex))
            exit()

    def ser(self): 
        return self.ser if self.ser.isOpen() else False

if __name__ == '__main__':
    serialHelper = SerialHelper()
    ser = serialHelper.ser()
    if ser:
        try:
            ser.flushInput() #flush input buffer
            ser.flushOutput() #flush output buffer
    
            #write 8 byte data
            ser.write([78, 78, 78, 78, 78, 78, 78, 78])
            print("write 8 byte data: 78, 78, 78, 78, 78, 78, 78, 78")
    
            time.sleep(0.5)  #wait 0.5s
    
            #read 8 byte data
            response = ser.read(8)
            print("read 8 byte data:")
            print(response)
    
            ser.close()
        except Exception as e1:
            print ("communicating error " + str(e1))
    else:
        print ("open serial port error")