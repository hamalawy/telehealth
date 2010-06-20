import ECG
import time
import serial

if __name__ == '__main__':
    interval = 1
#    print 'Pyserial'
#    ecg = serial.Serial('/dev/ttyUSB0', baudrate=230400)
#    later = time.time()+interval
#    cnt = 0
#    while later > time.time():
#        ecg.read()
#        cnt = cnt + 1
#    print cnt
#    print 'File'
#    ecg = file('/dev/ttyUSB0')
#    later = time.time()+interval
#    past = time.time()
#    cnt = 0
#    time.sleep(1)
#    print len(list(ecg.read(4000)))
#    while later > time.time():
#        print 
#        cnt = cnt + 1
#    print cnt
    data = open('data','w')
    try:
        nECG = ECG.ECG(port='/dev/ttyUSB0',daqdur=3)
        i = 0
        later = time.time()+20
        nECG.config_analog()
        nECG.start_ecg()
        nECG.start_flag = 1
        while later > time.time():
    		data.write(nECG.ecg.readline(size=None,eol=0xfd))
        nECG.stop_ecg()
        nECG.ecg.close()
    except Exception:
        pass
    data.close()
