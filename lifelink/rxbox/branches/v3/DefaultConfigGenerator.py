import ConfigParser

config = ConfigParser.ConfigParser()

config.add_section('Perspective')
config.set('Perspective','default','layout2|name=patientinfopanel;caption=Patient Info;state=2044;dir=1;layer=4;row=0;pos=0;prop=233043;bestw=635;besth=100;minw=50;minh=50;maxw=-1;maxh=-1;floatx=208;floaty=245;floatw=643;floath=124|name=commpanel;caption=;state=1020;dir=4;layer=2;row=1;pos=0;prop=31696;bestw=756;besth=68;minw=50;minh=50;maxw=-1;maxh=-1;floatx=-1;floaty=-1;floatw=-1;floath=-1|name=videopanel;caption=Video;state=2044;dir=1;layer=4;row=0;pos=1;prop=54150;bestw=50;besth=50;minw=50;minh=50;maxw=-1;maxh=-1;floatx=213;floaty=182;floatw=58;floath=74|name=snapshotpanel;caption=Snapshot;state=2044;dir=1;layer=4;row=0;pos=2;prop=53518;bestw=120;besth=120;minw=50;minh=50;maxw=-1;maxh=-1;floatx=213;floaty=181;floatw=128;floath=144|name=stethpanel;caption=Stethoscope;state=2044;dir=1;layer=4;row=0;pos=3;prop=59289;bestw=180;besth=100;minw=50;minh=50;maxw=-1;maxh=-1;floatx=491;floaty=565;floatw=188;floath=124|name=bppanel;caption=BP;state=2044;dir=3;layer=3;row=0;pos=0;prop=87843;bestw=784;besth=120;minw=50;minh=50;maxw=-1;maxh=-1;floatx=82;floaty=575;floatw=792;floath=144|name=spo2panel;caption=SPO2;state=2044;dir=3;layer=3;row=0;pos=1;prop=112157;bestw=862;besth=78;minw=50;minh=50;maxw=-1;maxh=-1;floatx=213;floaty=181;floatw=870;floath=102|name=ecgpanel;caption=ECG;state=2044;dir=4;layer=2;row=1;pos=1;prop=168304;bestw=681;besth=380;minw=50;minh=50;maxw=-1;maxh=-1;floatx=464;floaty=395;floatw=689;floath=404|dock_size(4,2,1)=1265|dock_size(3,3,0)=85|dock_size(1,4,0)=134|')
config.set('Perspective','onoff','')

config.add_section('ECG')
config.set('ECG','simulated','true')
config.set('ECG','port','/dev/ttyUSB0')
config.set('ECG','baud','230400')
config.set('ECG','daqdur','1')
config.set('ECG','ecmcheck','0')

config.add_section('Database')
config.set('Database','password','luke1025')

config.write(open('rxbox.cfg', 'wb'))