"""
RxBox Lead Calculator Module: contains methods that computes for lead I and
the three augmented leads

Authors: Dan Simone M. Cornillez
		 Luis Sison, PhD
         ------------------------------------------------
         Instrumentation, Robotics and Control Laboratory
         University of the Philippines - Diliman
         ------------------------------------------------
         October 2009		 
		 
"""
#function to calculate lead I
def LI(leadII,leadIII):
    """
    function that computes for lead I. Computes the lead I using the following
    equations: lead I = lead II - lead III
    Parameters:
    lead II: list of lead II values
    lead III: list of lead III values
    Returns:
    lead I: list of lead I values
    """
    leadI=[]
    for i in xrange(len(leadII)):
        leadI.append((-leadIII[i])+leadII[i])
    return leadI


#function to calculate lead VL
def LVL(leadII,leadIII):
    """
    function that computes for augmented lead VL. Computes for lead aVL using the following
    equations: lead aVL = 0.5*lead II - lead III
    Parameters:
    lead II: list of lead II values
    lead III: list of lead III values
    Returns:
    lead aVL: list of lead aVL values
    """
    leadaVL = []
    for i in xrange(len(leadII)):
        leadaVL.append((-leadIII[i])+(0.5*leadII[i]))
    return leadaVL                  

#function to calculate lead VF
def LVF(leadII,leadIII):
    """
    function that computes for augmented lead VF. Computes for lead aVF using the following
    equations: lead aVF = 0.5*(lead II + lead III)
    Parameters:
    lead II: list of lead II values
    lead III: list of lead III values
    Returns:
    lead aVF: list of lead aVF values
    """
    leadaVF = []
    for i in xrange(len(leadII)):
        leadaVF.append(0.5*(leadIII[i]+leadII[i]))

    return leadaVF
#function to calculate lead VR
def LVR(leadII,leadIII):
    """
    function that computes for augmented lead VR. Computes for lead aVR using the following
    equations: lead aVR = 0.5*(lead III - lead II)
    Parameters:
    lead II: list of lead II values
    lead III: list of lead III values
    Returns:
    lead aVR: list of lead aVR values
    """
    leadaVR = []
    for i in xrange(len(leadII)):
        leadaVR.append(0.5*(leadIII[i]-leadII[i]))

    return leadaVR


