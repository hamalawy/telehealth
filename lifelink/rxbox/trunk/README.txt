==============================================

        R X B O X - S O F T W A R E
       Information about Version 2-1

==============================================

Installing the software
----------------------------

IMPORTANT: If you are running the RxBox for the first time, 
*********  please make sure you have the following python modules 
           before working with this version!

  1) Python 2.5 (download it from python.org/download/releases/2.5.4)
  2) wxGlade (download from wxglade.sourceforge.net)
  3) wxPython (download from www.wxpython.org)
  4) matplotlib-0.98.5.2.win32-py2.5 (download from matplotlib.sourceforge.net)
  5) pylab (download from www.scipy.org/PyLab or sourceforge.net/projects/pylab)
  6) scipy-0.7.0-win32-superpack-python2.5 (download from www.scipy.org/Download)
  7) opencv (download from sourceforge.net/projects/opencvlibrary/)
  8) pyserial-2.2.win32 (download from pyserial.sourceforge.net/)


After installing the necessary modules, copy the 
following python files from 

http://code.google.com/p/telehealth/source/

or use a subversion client to checkout the files

URL of repository:
https://telehealth.googlecode.com/svn/branches/v2-1

on your working directory:

  1) acquire.py
  2) ecgplotter.py
  3) edf.py
  4) filters.py
  5) Main.py
  6) makeEDF.py
  7) referpanel.py
  8) rxpanel.py
  9) rxsensor.py

The following dependency folders should also be included on the 
directory:

  10) EDF Files
  11) Icons
  12) Photos
  13) Videos

NOTE: You must have a google code account for the telehealth project
to be able to checkout from the repository.

Running the RxBox Software
---------------------------------------

  1) Open the directory where you installed the software and
     double click or the file Main.py.
  2) A user authorization window will then prompt. 
     Enter "lifelink" as username then click OK.
  3) After successful login, the main window will now be available on screen.
  4) Press the start button to acquire and display biomedical signals.
  5) Press the refer button for referral.
  6) Press stop button to stop data acquisition.


IMPORTANT: Before pressing the Start button make sure that the medical
devices are correctly placed.

==============================================================================================

Copyright (c) 2009 UP Instrumentation, Robotics, and Control Laboratory. - All rights reserved

