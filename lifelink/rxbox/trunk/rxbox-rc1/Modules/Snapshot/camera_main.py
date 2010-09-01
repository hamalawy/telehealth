"""
camera_main.py

A module used by RxBox to display video stream and capturing an image

Dependencies:
- wx
- linphone
- xawtv

2010
"""



if __name__ == "__main__":
    app = wx.App()
    snapshot_frame = Snap(None, -1, "")
    snapshot_frame.Show()
    app.MainLoop()
