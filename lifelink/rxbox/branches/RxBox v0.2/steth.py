import wave
import struct
import numpy
import pylab
import scipy
import pyaudio
import wave
import scipy.io.wavfile as wavfile

def readwave(wavfilename):  
    """load raw data directly from a WAV file."""  
    global rate  
    w=wave.open(wavfilename,'rb')  
    (nchannel, width, rate, length, comptype, compname) = w.getparams()  
    print "[%s] %d HZ (%0.2fsec)" %(wavfilename, rate, length/float(rate))  
    frames = w.readframes(length)  
    return numpy.array(struct.unpack("%sh" %length*nchannel,frames))
    
def invert(data):  
    """inverts the signal"""  
    for i in range(len(data)): data[i]=-data[i]  
    return data

def bandStop(fft,fftx,low,high):
    """ remove frequency components from 'low' to 'high' Hz """
    for i in range(len(fft)):
        if abs(fftx[i])>low and abs(fftx[i])<high :
            fft[i]=0  
    return fft

def Hanning(oData):
    smoothed=[]
    for i in range(len(oData)):
        smoothed.append((oData[i]+2*oData[i-1]+oData[i-2])/4)
    return smoothed

def filter_wav(input_file, output_file = "filtered.wav"):
    """ filters input_file and save resulting data to output_file """
    raw = invert(readwave(input_file))  
    fftr = numpy.fft.fft(raw)  
    fft = fftr[:]  
    fftx= numpy.fft.fftfreq(len(raw), d=(1.0/(rate)))
    
    lowfreq = 58
    highfreq = 62
    lowspectrum = [(lowfreq+(item*60)) for item in range(5)]
    highspectrum = [(highfreq+(item*60)) for item in range(5)]

    fft=bandStop(fft,fftx,0,20)
    fft=bandStop(fft,fftx,-20,0)
    for i in range(5):
         fft = bandStop(fft,fftx,lowspectrum[i],highspectrum[i])
    fft=bandStop(fft,fftx,300,max(fftx))

    fix = scipy.ifft(fft)
    smoothed = Hanning(fix)
    gain = 1.0/max(numpy.absolute(smoothed))
    nsamples = len(smoothed)
    asamples = numpy.zeros(nsamples,dtype=numpy.int16)
    numpy.multiply(smoothed,32767.0 * gain,asamples)
    wavfile.write(output_file,rate,asamples)

class steth:
    def __init__(self,parent):
        self.chunk = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
        #self.RECORD_SECONDS = 30
        self.WAVE_OUTPUT_FILENAME = "Sounds/output.wav"
        self.parent = parent

    def init_record(self):
        self.steth_audio = pyaudio.PyAudio()
        self.steth_stream = self.steth_audio.open(format = self.FORMAT,
                channels = self.CHANNELS,
                rate = self.RATE,
                input = True,
                frames_per_buffer = self.chunk)
        self.steth_record = []

    def init_play(self, infile = "Sounds/output_filtered.wav"):
        self.steth_wave_file = wave.open(infile, 'rb')
        self.steth_audio = pyaudio.PyAudio()
        self.steth_stream = self.steth_audio.open(format = self.FORMAT,
                channels = self.CHANNELS,
                rate = self.RATE,
                frames_per_buffer = self.chunk,
                output = True)
        self.steth_wave_data = self.steth_wave_file.readframes(self.chunk)

    def stop_record(self, outfile = "Sounds/output_filtered.wav"):
        # write data to WAVE file
        self.steth_stream.close()
        self.steth_audio.terminate()
        data = ''.join(self.steth_record)
        wf = wave.open(self.WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(self.steth_audio.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(data)
        wf.close()
        print "Recording Stopped."
        print "Filtering Raw Signal..."
        #filter_wav(self.WAVE_OUTPUT_FILENAME,outfile)
        print "Filtered Signal Saved."

    def stop_play(self):
        self.steth_stream.close()
        self.steth_audio.terminate()
        print "Playback Stopped."
    

    
