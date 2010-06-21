from CPlotter import *

mode = ['small','normal','extend']

for i in mode:
    x = CPlotter(panel=None, mode=i, sample_time=1, plot_timelength=3, cont=True, filterOn = True, data=False)
    x.Open()
    x.Calibrate()
    x.Close()
