from SPO2DAQLive import *

class Spo2_check:
    def __init__(self,list_ports):
        self.ports=list_ports
        print self.ports
        self.correctport=None

    def check(self):
        for x in self.ports:
            print x
            self.spo2 = SPO2DAQ(self,port =x)
            status=self.spo2.port_check()
            if status==True:
                self.correctport=x       
                print 'The correct port is: '+self.correctport
                break
            else:
                continue

port2check=['COM1','COM2','COM3','COM4','COM5','COM6','COM7']

c=Spo2_check(port2check)
c.check()
