class Reader:

    def __init__(self):
        pass

    def OpenFile(self, sample):

        opener=open(sample,'r')
        return opener
        
    def ReadLine(self,opener):

        reply=opener.readline()
        reply=reply[:len(reply)-1]

        return reply
