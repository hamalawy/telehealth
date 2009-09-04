"""
RxBox: Lead Calculator Module
Contains methods that computes for lead I and the three augmented leads

Authors: Dan Simone M. Cornillez
         ------------------------------------------------
         Instrumentation, Robotics and Control Laboratory
         University of the Philippines - Diliman
         ------------------------------------------------
         July 2009
"""

def LI(leadII,leadIII):
    """ function that computes for lead I

    Computes the lead I using the following equation:

    leadI = leadII - leadIII
           
    Parameters
    ----------
    leadII   : list of lead II values
    leadIII  : list of lead III values

    Returns
    -------
    leadI    : list of lead I values
    """

    leadI=[]
    for i in range(len(leadII)):
    
        leadI.append((-leadIII[i])+leadII[i])
    return leadI


def LVL(leadII,leadIII):
    """ function that computes for augmented lead VL

    Computes the lead aVL using the following equation:

    leadI = 0.5*leadII - leadIII
           
    Parameters
    ----------
    leadII   : list of lead II values
    leadIII  : list of lead III values

    Returns
    -------
    leadaVL    : list of lead aVL values
    """

    leadaVL = []
    for i in range(len(leadII)):
        leadaVL.append((-leadIII[i])+(0.5*leadII[i]))
    return leadaVL                  

def LVF(leadII,leadIII):
    """ function that computes for augmented lead VF

    Computes the lead aVF using the following equation:

    leadaVF = 0.5*(leadII + leadIII)
           
    Parameters
    ----------
    leadII   : list of lead II values
    leadIII  : list of lead III values

    Returns
    -------
    leadaVF    : list of lead aVF values
    """

    leadaVF = []
    for i in range(len(leadII)):
        leadaVF.append(0.5*(leadIII[i]+leadII[i]))

    return leadaVF

def LVR(leadII,leadIII):
    """ function that computes for augmented lead VR

    Computes the lead aVR using the following equation:

    leadaVR = 0.5*(leadIII - leadII)
           
    Parameters
    ----------
    leadII   : list of lead II values
    leadIII  : list of lead III values

    Returns
    -------
    leadaVR    : list of lead aVR values
    """

    leadaVR = []
    for i in range(len(leadII)):
        leadaVR.append(0.5*(leadIII[i]-leadII[i]))

    return leadaVR


