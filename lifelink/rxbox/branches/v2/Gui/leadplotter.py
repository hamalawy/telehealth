from ecglogfile import ECG
import pylab
from pylab import *
import leadcalc
import numpy

def Plot12Lead():
    a = ECG().ecg_lead()

    h,w=4,4
    pylab.subplots_adjust(hspace=0.7)

    pylab.subplot(h,w,1);pylab.title("Lead I")
    pylab.xticks(numpy.arange(0,1000,10))
    pylab.grid(color='lightgrey', linestyle=':', linewidth=0.05)
    pylab.plot(a[0][:300])

    pylab.subplot(h,w,5);pylab.title("Lead II")
    pylab.xticks(numpy.arange(0,1000,10))
    pylab.grid(color='lightgrey', linestyle=':', linewidth=0.05)
    pylab.plot(a[1][:300])

    pylab.subplot(h,w,9);pylab.title("Lead III")
    pylab.xticks(numpy.arange(0,1000,10))
    pylab.grid(color='lightgrey', linestyle=':', linewidth=0.05)
    pylab.plot(a[2][:300])

    pylab.subplot(h,w,2);pylab.title("Lead aVR")
    pylab.xticks(numpy.arange(0,1000,10))
    pylab.grid(color='lightgrey', linestyle=':', linewidth=0.05)
    pylab.plot(a[3][:300])

    pylab.subplot(h,w,6);pylab.title("Lead aVL")
    pylab.xticks(numpy.arange(0,1000,10))
    pylab.grid(color='lightgrey', linestyle=':', linewidth=0.05)
    pylab.plot(a[4][:300])

    pylab.subplot(h,w,10);pylab.title("Lead aVF")
    pylab.xticks(numpy.arange(0,1000,10))
    pylab.grid(color='lightgrey', linestyle=':', linewidth=0.05)
    pylab.plot(a[5][:300])

    pylab.subplot(h,w,3);pylab.title("Lead V1")
    pylab.xticks(numpy.arange(0,1000,10))
    pylab.grid(color='lightgrey', linestyle=':', linewidth=0.05)
    pylab.plot(a[6][:300])

    pylab.subplot(h,w,7);pylab.title("Lead V2")
    pylab.xticks(numpy.arange(0,1000,10))
    pylab.grid(color='lightgrey', linestyle=':', linewidth=0.05)
    pylab.plot(a[7][:300])

    pylab.subplot(h,w,11);pylab.title("Lead V3")
    pylab.xticks(numpy.arange(0,1000,10))
    pylab.grid(color='lightgrey', linestyle=':', linewidth=0.05)
    pylab.plot(a[8][:300])

    pylab.subplot(h,w,4);pylab.title("Lead V4")
    pylab.xticks(numpy.arange(0,1000,10))
    pylab.grid(color='lightgrey', linestyle=':', linewidth=0.05)
    pylab.plot(a[9][:300])

    pylab.subplot(h,w,8);pylab.title("Lead V5")
    pylab.xticks(numpy.arange(0,1000,10))
    pylab.grid(color='lightgrey', linestyle=':', linewidth=0.05)
    pylab.plot(a[10][:300])

    pylab.subplot(h,w,12);pylab.title("Lead V6")
    pylab.xticks(numpy.arange(0,1000,10))
    pylab.grid(color='lightgrey', linestyle=':', linewidth=0.05)
    pylab.plot(a[11][:300])

    pylab.subplot(414);pylab.title("Lead II")
    pylab.xticks(numpy.arange(0,1000,10))
    pylab.grid(color='lightgrey', linestyle=':', linewidth=0.05)
    pylab.plot(a[1])

    pylab.show()
