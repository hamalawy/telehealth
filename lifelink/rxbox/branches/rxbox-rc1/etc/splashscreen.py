import os
import wx
import wx.html

MAIN_WINDOW_DEFAULT_SIZE = (300,200)
ABOUT_DIALOG_SIZE = (400,280)
SPLASH_SCREEN_FILENAME = 'luke.png'
SPLASH_SCREEN_TIMEOUT = 5000

class ImageViewerAbout(wx.Dialog):
    """This AboutBox is built from Robin Dunn and Noel Rappin's
    excellent wxPython in Action book, see page 178+ for the About HTML box
    and page 174+ for a short discussion on BoxSizers"""
    
    text = '''<html>
    <h1>ShowMeDo Image Viewer</h1>
    <p>The ShowMeDo Image Viewer is a demonstration application for the ShowMeDo
    wxPython 'image viewing' tutorial.</p>
    <p>More information is available at <a href="http://showmedo.com">ShowMeDo.com</a>.<p>
    <p>Created February 2008, Copyright &copy; ShowMeDo Ltd.</p>
    </html>'''
    
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, -1, 'About the ShowMeDo Image Viewer...',
                           size=ABOUT_DIALOG_SIZE)
        
        html = wx.html.HtmlWindow(self)
        html.SetPage(self.text)
        # If a button has an ID of wx.ID_OK it will automatically close a wx.Dialog when pressed
        # create a 'button' object from wx.Button, give it the ID wx.ID_OK and text 'Okay'
        button = wx.Button(self, wx.ID_OK, 'Okay')

        # Create a BoxSizer which grows in the vertical direction
        sizer = wx.BoxSizer(wx.VERTICAL)
        # Add the html window, tell it to take a 100% portion of the *available* area
        # and to EXPAND in ALL directions.  Use a border of 5 pixels around ALL sides of the button
        sizer.Add(html, 1, wx.EXPAND|wx.ALL, 5)

        # Add the button, ask it to grow by 0%
        #sizer.Add(button, 0)
        # also ask the button to align in the centre (my UK spelling!), with a 5 pixel border
        # around all sides
        sizer.Add(button, 0, wx.ALIGN_CENTER|wx.ALL, 5)

        # Tell our Dialog to use this new Sizer
        self.SetSizer(sizer)
        # Tell our Dialog to calculate the size of its items.  Good practice to always do this
        self.Layout()

class Frame(wx.Frame):
    
    def __init__(self, parent, id, title):
        style=wx.DEFAULT_FRAME_STYLE ^ (wx.RESIZE_BORDER) # XOR to remove the resizeable border        
        wx.Frame.__init__(self, parent, id, title=title, size=MAIN_WINDOW_DEFAULT_SIZE, style=style)
        self.Center() # open in the centre of the screen
        self.panel = wx.Panel(self)
        self.panel.SetBackgroundColour('White') # make the background of the window white

        self.CreateMenuBar()
        
        # create a StatusBar and give it 2 columns
        self.statusBar = self.CreateStatusBar()
        self.statusBar.SetFieldsCount(2)
        self.statusBar.SetStatusText('No image specified', 1)
        
        self.bitmap = None # set to None as we refer to it in ShowBitmap before we instantiate it
        
    def CreateMenuBar(self):
        "Create a menu bar with Open, Exit items"
        menuBar = wx.MenuBar()
        # Tell our Frame about this MenuBar
        self.SetMenuBar(menuBar)
        menuFile = wx.Menu()
        menuBar.Append(menuFile, '&File')
        # NOTE on wx ids - they're used everywhere, we don't care about them
        # Used to handle events and other things
        # An id can be -1 or wx.ID_ANY, wx.NewId(), your own id
        # Get the id using object.GetId()
        fileOpenMenuItem = menuFile.Append(-1, '&Open Image', 'Open a picture')
        #print "fileOpenMenuItem.GetId()", fileOpenMenuItem.GetId()
        self.Bind(wx.EVT_MENU, self.OnOpen, fileOpenMenuItem)

        # add a 'mirror' option, disable it for now
        # we add mirrorMenuItem to self so that we can reference it later
        self.mirrorMenuItem = menuFile.Append(-1, '&Mirror Image', 'Mirror the image horizontally')
        self.mirrorMenuItem.Enable(False) # we can't mirror an image until we've loaded one in, so start with 'mirror' disabled
        self.Bind(wx.EVT_MENU, self.OnMirrorImage, self.mirrorMenuItem)
        
        # create a menu item for Exit and bind it to the OnExit function       
        exitMenuItem = menuFile.Append(-1, 'E&xit', 'Exit the viewer')        
        self.Bind(wx.EVT_MENU, self.OnExit, exitMenuItem)
        
        # add a Help menu with an About item
        menuHelp = wx.Menu()
        menuBar.Append(menuHelp, '&Help')
        helpMenuItem = menuHelp.Append(-1, '&About', 'About screen')
        self.Bind(wx.EVT_MENU, self.OnAbout, helpMenuItem)

    def OnAbout(self, event):
        dlg = ImageViewerAbout(self)
        dlg.ShowModal()
        dlg.Destroy()

    def OnMirrorImage(self, event):
        # ask the Image to mirror itself on the x-axis
        self.image = self.image.Mirror()
        # whilst we mirror it and show it, we haven't yet forced a repaint so we won't see it unless we hide the window
        self.ShowBitmap()
        # now we can ask for a refresh which repaints the image
        self.Refresh()

    def OnOpen(self, event):
        "Open an image file, set title if successful"
        # Create a file-open dialog in the current directory
        
        filters = 'Image files (*.gif;*.png;*.jpg)|*.gif;*.png;*.jpg'
        dlg = wx.FileDialog(self, message="Open an Image...", defaultDir=os.getcwd(), 
                            defaultFile="", wildcard=filters, style=wx.OPEN)
        
        # Call the dialog as a model-dialog so we're required to choose Ok or Cancel
        if dlg.ShowModal() == wx.ID_OK:
            # User has selected something, get the path, set the window's title to the path
            filename = dlg.GetPath()
            self.SetTitle(filename)
            wx.BeginBusyCursor()            
            # load the image from the filename
            self.image = wx.Image(filename, wx.BITMAP_TYPE_ANY, -1) # auto-detect file type        
            # set the StatusBar to show the image's size
            self.statusBar.SetStatusText('Size = %s' % (str(self.image.GetSize())) , 1)
            # display the image inside the panel
            self.ShowBitmap()
            # enable the 'Mirror' menu item, it only makes sense to enable it when we've loaded
            # an image as before there would be no image to mirror
            self.mirrorMenuItem.Enable(True)
            wx.EndBusyCursor()
                        
        dlg.Destroy() # we don't need the dialog any more so we ask it to clean-up

    def ShowBitmap(self):
        if self.bitmap is not None:
            self.bitmap.Destroy()
        
        # Convert to Bitmap for wxPython to draw it to screen
        self.bitmap = wx.StaticBitmap(self.panel, -1, wx.BitmapFromImage(self.image))       
        # Make the application's window as large as the image
        self.SetClientSize(self.bitmap.GetSize())
        self.Center() # open in the centre of the screen
        
    def OnExit(self, event):
        "Close the application by Destroying the object"
        self.Destroy() 
        
    
class App(wx.App):
    
    def OnInit(self):
        self.frame = Frame(parent=None, id=-1, title='Image Viewer')
        self.frame.Show()
        self.SetTopWindow(self.frame)
        return True
    
if __name__ == "__main__":       
    # make an App object, set stdout to the console so we can see errors
    app = App(redirect=False)
        
    # open a splash screen if it exists
    if os.path.exists(SPLASH_SCREEN_FILENAME):
        splash_image = wx.Image(SPLASH_SCREEN_FILENAME, wx.BITMAP_TYPE_ANY, -1)        
        wx.SplashScreen(splash_image.ConvertToBitmap(), 
                        wx.SPLASH_CENTRE_ON_SCREEN | wx.SPLASH_TIMEOUT, 
                        SPLASH_SCREEN_TIMEOUT, 
                        None, -1)
        
    app.MainLoop()
