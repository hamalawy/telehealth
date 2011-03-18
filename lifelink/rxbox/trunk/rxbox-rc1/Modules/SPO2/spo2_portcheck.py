from SPO2DAQLive import *

class Spo2_check:
    def __init__(self,list_ports):
        self.ports=list_ports
        #print self.ports
        self.correctport=None

    def check(self):
        for x in self.ports:
            #print x
            self.spo2 = SPO2DAQ(self,port =x,timeout=1)
            status=self.spo2.port_check()
            if status==True:
                self.correctport=x       
                #print 'The correct spo2 port is: '+self.correctport
                return x
            else:
                continue
        return None

if __name__== "__main__":
    port2check=['/dev/ttyUSB0','/dev/ttyUSB1','/dev/ttyUSB2']

    c=Spo2_check(port2check)
    c.check()
