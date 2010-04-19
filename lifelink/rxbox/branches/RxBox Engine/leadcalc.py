#function to calculate lead I
def LI(leadII,leadIII):

    leadI=[]
    for i in range(len(leadII)):
        leadI.append((-leadIII[i])+leadII[i])
    return leadI

#function to calculate lead VL
def LVL(leadII,leadIII):
    leadaVL = []
    for i in range(len(leadII)):
        leadaVL.append((-leadIII[i])+(0.5*leadII[i]))
    return leadaVL                  

#function to calculate lead VF
def LVF(leadII,leadIII):
    leadaVF = []
    for i in range(len(leadII)):
        leadaVF.append(0.5*(leadIII[i]+leadII[i]))
    return leadaVF

#function to calculate lead VR
def LVR(leadII,leadIII):
    leadaVR = []
    for i in range(len(leadII)):
        leadaVR.append(0.5*(leadIII[i]-leadII[i]))
    return leadaVR