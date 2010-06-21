from ECG2 import *

x = open('data','r')
for i in x:
    print list(i)
x.close()
#x = ECG()
#x.patient_ready()
#print x.lead_ecg['II']