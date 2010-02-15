import edfviewer

c_inst=edfviewer.EDF_File('Ebido_113056.edf')# edf file input
x=c_inst.parseDataRecords()

y = range(len(x[4]));
c = zip(y,x[4])

#patient info
print c_inst.LocalPatientID

#ecg
print [list(a) for a in c]

#Spo2
print x[0][len(x[0])-1]

#BP
print str(x[1][len(x[1])-1]) + '/' + str(x[2][len(x[2])-1])

#Heart rate
print x[3][len(x[3])-1]


