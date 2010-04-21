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
    try:
        nECG = ECG.ECG(port=3,daqdur=3)
        nECG.device_ready()
        i = 0
        later = time.time()+20
        
        while i < 10:
            nECG.patient_ready()
            nECG.pop(0,1000)
            i = i + 1
        nECG.config_analog()
        nECG.start_ecg()
        nECG.start_flag = 1
        while later > time.time():
			nECG.ecg.readline(size=100,eol=0xfd)
    except Exception:
        pass
        raise
    nECG.stop_ecg()
    nECG.ecg.close()
