1) edit logging.conf (section: handler_consoleHandler, option: args)
   (a) from ('mylog.txt', 'a') to ('/path-to/mylog.txt', 'a')
2) solution to the "/usr/bin/python^M: bad interpreter: No such file or directory" problem...
   (a) open vi (vi -b <filename>)
   (b) type the following (:1,$s/^M//g)