import wx
import urllib2
import os
import ConfigParser
import subprocess

from States.State import *

class UpdateState(State):
    def __init__(self, engine, *args, **kwds):
        State.__init__(self, engine, *args, **kwds)
    
    def __name__(self):
        return 'UpdateState'
        
    def start(self):
        self._logger.info('State Machine: %s Start'%self.__name__())
        
        dlg = wx.MessageDialog(self._frame, 'Are you sure you want to Update?', 'Update', \
                                wx.YES_NO)
        responce = dlg.ShowModal()
        if responce == wx.ID_YES:
            try:
                updateinfo = subprocess.Popen("svn info",shell=True,stdout=subprocess.PIPE).stdout.read()
                version = int(updateinfo[updateinfo.find('Revision: ')+len('Revision: '):updateinfo.find('\nNode')])

                dlg = wx.ProgressDialog("Updating Rxbox",
                                       "Updating... Please Wait...",
                                       maximum = 10,
                                       parent=self._frame,
                                       style = wx.PD_APP_MODAL | wx.PD_AUTO_HIDE
                                        )
                
                error_msg = 'Update Failed: Internet Connection Error'
                dlg.Update(1,"Checking Internet Connection")
                con = urllib2.urlopen("http://www.google.com/")
                if not con.read(): raise
                self._logger.info('Connection Established: Ready for Update')
                
                error_msg = 'Update Failed'
                dlg.Update(2,"Making Back Up")
                os.system('mv rxbox.cfg rxbox.bk')
                os.system('mv Logs Logsbk')
                dlg.Update(3,"Cleaning Up")
                os.system('svn cleanup')
                dlg.Update(4,"Updating Modules")
                os.system('svn update --accept theirs-full')
                dlg.Update(6,"Checking Config Files")
                configorig = ConfigParser.ConfigParser()
                confignew = ConfigParser.ConfigParser()
                configorig.read('rxbox.bk')
                confignew.read('rxbox.cfg')
                origsections = configorig.sections()
                for newsection in confignew.sections():
                    if newsection not in origsections:
                        self._logger.info('Added Section: %s'%newsection)
                        configorig.add_section(newsection)
                    origoptions = configorig.options(newsection)
                    for newoption in confignew.options(newsection):
                        if newoption not in origoptions:
                            self._logger.info('Added Option: %s'%newoption)
                            configorig.set(newsection,newoption,confignew.get(newsection, newoption))
                configorig.write(open('rxbox.bk', 'w'))
                dlg.Update(7,"Restoring Config Files")
                os.system('rm -rf Logs')
                os.system('mv Logsbk Logs')
                dlg.Update(8,"Installing dependencies")
                fp = open('States/UpdateState/update.rxbox')
                record = 0
                for line in fp:
                    if not line.strip().isalnum() and record>version:
                        TERMINAL('gksudo %s'%line.strip(),self._logger)
                    elif line.strip().isalnum():
                        record = int(line)
                dlg.Update(10,"Update Complete..Please Restart Rxbox to commit changes")

                updateinfo = subprocess.Popen("svn info",shell=True,stdout=subprocess.PIPE).stdout.read()
                wx.MessageBox('%sUpdate Complete..Please Restart Rxbox..'%updateinfo, 'Info')
                self._engine.change_state('ExitState')
            except:
                ERROR(logger=self._logger,comment=error_msg,frame=self._frame)
                dlg.Destroy()
            
        
    def stop(self):
        self._logger.info('State Machine: %s Stop'%self.__name__())
