class Reader:

    def __init__(self):
        pass

    def OpenFile(self):

        opener=open('sample','rb')
        return opener
        
    def ReadLine(self,opener):

        reply=opener.readline()
        reply=reply[:len(reply)-1]

        return reply
