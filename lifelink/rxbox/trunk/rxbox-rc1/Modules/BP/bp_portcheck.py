from BPDAQLive import BPDAQ

class Bp_check:
    def __init__(self,list_ports):
        self.ports=list_ports
        #print self.ports
        self.correctport=None

    def check(self):
        for x in self.ports:
            #print x
            self.bp = BPDAQ(self,port =x,timeout=1,coeff=(1,0,0,0,1,0))
            status=self.bp.port_check()
            if status==True:
                self.correctport=x       
                #print 'The correct BP port is: '+self.correctport
                return x
            else:
                continue
        return None
            
            
if __name__== "__main__":
    port2check=['/dev/ttyUSB0','/dev/ttyUSB1','/dev/ttyUSB2']

    c=Bp_check(port2check)
    c.check()
