import scipy,numpy

def lowpassfilter(raw_readings):
    fft = scipy.fft(raw_readings)
    bp=fft[:]
    for i in range(len(bp)):
        if 590<i<910: bp[i]=0

    filtered_readings = scipy.ifft(bp)
    return filtered_readings

def Notch50hzFs100(oData):
    filtered=[]
    NOTCH_LENGTH_AVERAGE_FS100 = 100/50
    for i in range(len(oData)):
        filtered.append((sum(oData[i:(i+2)])/NOTCH_LENGTH_AVERAGE_FS100))

    return filtered

def bandpass(oData):

    fft = scipy.fft(oData)
    bp=fft[:]
    for i in range(len(bp)):
        if 375<i<1125 or i<0.75 or i>1499.25: bp[i]=0
               
    filtered =scipy.ifft(bp)

    return filtered

def Notchfilter(oData):
    
    fft = scipy.fft(oData)
    bp=fft[:]
    for i in range(len(bp)):
        if 590<i<620 or 880<i<910: bp[i]=0
               
    filtered =scipy.ifft(bp)

    return filtered

def hanning(oData):
    smoothed=[]
    filtered=oData[:]
    for i in range(len(filtered)):
         smoothed.append((filtered[i]+2*filtered[i-1]+filtered[i-2])/4)
    return smoothed

def smoothListTriangle(list,strippedXs=False,degree=5): #original degree=5
    weight=[]
    window=degree*2-1
    smoothed=[0.0]*(len(list)-window)
    for x in range(1,2*degree):weight.append(degree-abs(degree-x))
    w=numpy.array(weight)
    for i in range(len(smoothed)):
        smoothed[i]=sum(numpy.array(list[i:i+window])*w)/float(sum(w))
    return smoothed


