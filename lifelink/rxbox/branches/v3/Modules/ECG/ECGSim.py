
class ECG:
    def __init__(self, panel=False, port='/dev/ttyUSB0', baud=230400, timeout=0.01, daqdur=15, ecmcheck=3, debug=True):
        pass
    
    def device_ready(self):
        print 'ECG Simulated Device Ready'
        
    def stop(self):
        print 'ECG Simulated Stop'