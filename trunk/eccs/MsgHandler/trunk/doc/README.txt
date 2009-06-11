1) copy triage.conf.template to triage.conf and modify
2) copy MHPATH variable in init_sc.template and modify
3) solution to the "/usr/bin/python^M: bad interpreter: No such file or directory" problem...
   (a) open vi (vi -b <filename>)
   (b) type the following (:1,$s/^M//g)