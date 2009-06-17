Issues:
1) To update WSDL: wsdl2py --complexType <url_address or file_path>

Initialization:
1) "cd /path/to/MsgHandler/trunk/bin"
2) "cp init_sc.template init_sc"
2) modify MHPATH variable in init_sc
3) "chmod 755 init_sc"
4) "./init_sc"
4) copy mhdaemon to preferred location

How to run the program:
1) cd to path of mhdaemon

1) copy triage.conf.template to triage.conf and modify
2) copy MHPATH variable in init_sc.template and modify
3) solution to the "/usr/bin/python^M: bad interpreter: No such file or directory" problem...
   (a) open vi (vi -b <filename>)
   (b) type the following (:1,$s/^M//g)