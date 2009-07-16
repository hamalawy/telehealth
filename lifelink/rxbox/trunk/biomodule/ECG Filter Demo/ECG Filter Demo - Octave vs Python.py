import EDF_extractor
import numpy
import matplotlib.pyplot
from scipy.signal import butter, bessel, lfilter

def getListFromFile(File):
    """ getListFromFile(File) -> returns a list of float from File

        Method that reads the data on "File" per line and convert
        each to float then store it to a list. """
    myFile = open(File,'r')
    data = []
    for i in range(7500):
        line = myFile.readline()
        data.append(float(line))
    myFile.close()
    return data

# Get leadII from an EDF file
leadII = EDF_extractor.ExtractECG('Sison, Luis.edf','output.txt','II',15,20)
n = 4 # filter order
f = 35.0000 # cutoff frequency
fs = 500 # sampling frequency

# Apply Butterworth filter to raw signal
[b,a] = butter(n,f/fs,'low') # Get Butterworth Filter Coefficients
signal = lfilter(b,a,leadII) # Filter the signal using extracted coefficients

# Read the butterworth filtered data stored in an octave file
octavedata = getListFromFile('filteroutput.txt')

t = numpy.arange(0,4,4.0000/2000)

# Plot Raw Data
matplotlib.pyplot.subplot(311)
matplotlib.pyplot.title("Raw Data")
matplotlib.pyplot.plot(t,leadII[200:2200])

# Plot Python Butterworth Filter
matplotlib.pyplot.subplot(312)
matplotlib.pyplot.title("Python Butterworth n=4")
matplotlib.pyplot.plot(t,signal[200:2200])

# Plot Octave Butterworth Filter
matplotlib.pyplot.subplot(313)
matplotlib.pyplot.title("Octave Butterworth n=4")
matplotlib.pyplot.plot(t,octavedata[200:2200])

matplotlib.pyplot.show()

