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
        
        try:
            con = urllib2.urlopen("http://www.google.com/")
            if not con.read(): return
            self._logger.info('Connection Established: Ready for Update')
        except:
            ERROR(logger=self._logger,comment='Internet Connection Error: Update Failed',frame=self._frame)
            return



        dlg = wx.MessageDialog(self._frame, 'Are you sure you want to Update?', 'Update', \
                                wx.YES_NO)
        responce = dlg.ShowModal()
        if responce == wx.ID_YES:
            try:
                updateinfo = subprocess.Popen("svn info",shell=True,stdout=subprocess.PIPE).stdout.read()
                version = int(updateinfo[updateinfo.find('Revision: ')+len('Revision: '):updateinfo.find('\nNode')])

                dlg = wx.ProgressDialog("Updating Rxbox",
                                       "Updating... Please Wait...",
                                       maximum = 8,
                                       parent=self._frame,
                                       style = wx.PD_APP_MODAL | wx.PD_AUTO_HIDE
                                        )

                dlg.Update(1,"Making Back Up")
                os.system('mv rxbox.cfg rxbox.bk')
                os.system('mv Logs Logsbk')
                dlg.Update(2,"Cleaning Up")
                os.system('svn cleanup')
                dlg.Update(3,"Updating Modules")
                os.system('svn update --accept theirs-full')
                dlg.Update(5,"Checking Config Files")
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
                dlg.Update(8,"Update Complete..Please Restart Rxbox to commit changes")

                updateinfo = subprocess.Popen("svn info",shell=True,stdout=subprocess.PIPE).stdout.read()
                fp = open('States/UpdateState/update.rxbox')
                record = 0
                inst = []

                for line in fp:
                    if not line.strip().isalnum() and record>version:
                        inst.append(line.strip())
                    elif line.strip().isalnum():
                        record = int(line)

                update = subprocess.Popen('gnome-terminal -x bash -c "%s"'%(';'.join(inst)),shell=True,stdout=subprocess.PIPE)
                update.wait()

                wx.MessageBox('%sUpdate Complete..Please Restart Rxbox..'%updateinfo, 'Info')
            except:
                ERROR(logger=self._logger,comment='Update Failed',frame=self._frame)
                dlg.Destroy()
            self._engine.change_state('ExitState')
        
    def stop(self):
        self._logger.info('State Machine: %s Stop'%self.__name__())
