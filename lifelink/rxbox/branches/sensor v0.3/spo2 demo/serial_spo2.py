

import serial
import datetime
import pickle

SerialPort = '/dev/ttyUSB0'
SerialBaudRate = 9600
SerialTimeout = 5
DataPacket = []

command = [0x7f, 0xd1, 0x01, 0x01, 0x01, 0x02,\
                        0x01, 0x03, 0x01, 0x11, 0x01, 0x04, 0x0a]
SerPort = serial.Serial(port=SerialPort,baudrate=SerialBaudRate,timeout=SerialTimeout)
SerPort.flushInput()
SerPort.flushOutput()
list_spo2=[]
concatinate=[]
x=0
while x<400:
    byte = SerPort.read(1)
    byte_print=ord(byte)
    if byte_print==168:
        x=x+1
    list_spo2.append(byte_print)

print list_spo2
count=0
numeral=0
error_count=0

for i in range(len(list_spo2)):
    val=list_spo2[i]
    concatinate.append(val)
    if val == 168:
        count=count+1
    if count==2:
        print "\n"
        numeral=numeral+1
        print str(numeral)+"."+"Length"+":"+str(len(concatinate))
        print concatinate
        if len(concatinate)!=21:
            error_count=error_count+1         
        concatinate=[]
        count=0
percent=error_count*100/200.0    
print "\n"+"Number of errors:"+str(error_count)+"/200"+" "+str(percent)+"%"+"\n"

"""
Starttime = datetime.datetime.today() + datetime.timedelta(seconds = -15)
timestamp = Starttime.strftime("%H%M%S")
txtfile   = open("data/"+timestamp + '.txt', 'wb+')
txtfile.write(str(list_spo2))
txtfile.close()
"""        

        
