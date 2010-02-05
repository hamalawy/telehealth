
import edfviewer
from pylab import *

c_inst=edfviewer.EDF_File('Ebido_113056.edf')# edf file input
x=c_inst.parseDataRecords()
print c_inst.LocalPatientID

subplot(5,1,1);plot(r_[:len(x[0])],x[0]);grid(True);title(c_inst.BioSignals[0].TechInfolist[0]);
subplot(5,1,2);plot(r_[:len(x[1])],x[1]);grid(True);title("BPM"+c_inst.BioSignals[1].TechInfolist[0]);
subplot(5,1,3);plot(r_[:len(x[2])],x[2]);grid(True);title(c_inst.BioSignals[2].TechInfolist[0]);
subplot(5,1,4);plot(r_[:len(x[3])],x[3]);grid(True);title(c_inst.BioSignals[3].TechInfolist[0]);
subplot(5,1,5);plot(r_[:len(x[4])],x[4]);grid(True);title("ECG"+c_inst.BioSignals[4].TechInfolist[0]);
show()
