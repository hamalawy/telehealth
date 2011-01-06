from BPDAQLive import BPDAQ

class Bp_check:
    def __init__(self,list_ports):
        self.ports=list_ports
        print self.ports
        self.correctport=None

    def check(self):
        for x in self.ports:
            print x
            self.bp = BPDAQ(self,port =x,coeff=(1,0,0,0,1,0))
            status=self.bp.port_check()
            if status==True:
                self.correctport=x       
                print 'The correct port is: '+self.correctport
                break
            else:
                continue
        
            
            

port2check=['COM1','COM2','COM3','COM4','COM5','COM6','COM7','COM8']

c=Bp_check(port2check)
c.check()
