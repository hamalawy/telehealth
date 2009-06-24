Using the program:
1) initialization
    cd <path to>/MsgHandler/trunk/bin
    cp init_sc.template init_sc
    vim init_sc (then modify the MHPATH variable)
    :wq
    chmod 755 init_sc
    ./init_sc
    cp mhdaemon <desired path>
2) add configuration
    cd <path to>/MsgHandler/trunk/config
    cp triage.conf.template triage.conf
    vim triage.conf (then modify values)
    :wq
2) run
    <path to>/mhdaemon start

Known Issues:
1) To update WSDL (web service connection error)
    wsdl2py --complexType <url_address or file_path>
2) Solution to the "/usr/bin/python^M: bad interpreter: No such file or directory" problem...
    vim -b <filename>
    :1,$s/^M//g
    :wq
