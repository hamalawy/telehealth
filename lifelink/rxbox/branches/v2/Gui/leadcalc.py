#function to calculate lead I
def calcLI(leadII,leadIII):

    leadI=[]
    for i in range(len(leadII)):
    
        leadI.append((-leadIII[i])+leadII[i])
    return leadI


#function to calculate lead VL
def calcLVL(leadII,leadIII):

    leadaVL = []
    for i in range(len(leadII)):
        leadaVL.append((-leadIII[i])+(0.5*leadII[i]))
    return leadaVL                  

#function to calculate lead VF
def calcLVF(leadII,leadIII):

    leadaVF = []
    for i in range(len(leadII)):
        leadaVF.append(0.5*(leadIII[i]+leadII[i]))

    return leadaVF
#function to calculate lead VR
def calcLVR(leadII,leadIII):

    leadaVR = []
    for i in range(len(leadII)):
        leadaVR.append(0.5*(leadIII[i]-leadII[i]))

    return leadaVR


