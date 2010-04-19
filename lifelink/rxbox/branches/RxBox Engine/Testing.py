import ECG
import time

if __name__ == '__main__':
    try:
        nECG = ECG.ECG(daqdur=3)
        nECG.device_ready()
        i = 0
        later = time.time()+20
        
        while i < 10:
            nECG.patient_ready()
            nECG.Pop(0,7000)
            i = i + 1
        """
        nECG.config_analog()
        nECG.start_ecg()
        nECG.start_flag = 1
        while later > time.time():
			nECG.ecg.readline(size=100,eol=0xfd)
		"""
    except Exception:
        pass
        raise
    nECG.stop_ecg()
    nECG.ecg.close()
