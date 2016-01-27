#!/bin/bash
 
    ## LOCAL/FTP/SCP/MAIL PARAMETERS
    SERVER="192.168.1.1"         # IP of Network disk, used for: ftp mail scp
    USERNAME="freebox"         # FTP username of Network disk used for: ftp mail scp
    PASSWORD="hf6ns7hv"               # FTP password of Network disk used for: ftp mail scp
    DESTDIR="/opt/backup"      # used for: local
    DOMO_IP="127.0.0.1"      # Domoticz IP used for all
    DOMO_PORT="8080"         # Domoticz port used for all
    ## END OF USER CONFIGURABLE PARAMETERS
 
    TIMESTAMP=`/bin/date +%Y%m%d%H%M%S`
    BACKUPFILEDIR="domoticz_$TIMESTAMP.tar.gz" # Change the xxx to yours
 
    ### Create backup and ZIP it
    tar -zcvf /tmp/$BACKUPFILEDIR /home/pi/git/domoticz.git/   # Change the xxx to yours    # Or try /home/pi/domoticz/
 
    ### Send to Network disk through FTP
    curl -s --disable-epsv -v -T"/tmp/$BACKUPFILEDIR" -u"$USERNAME:$PASSWORD" "ftp://$SERVER/Disque%20dur/domoticz/"  # Change the ftp to yours !!!
 
    ### Remove temp backup file
    /bin/rm /tmp/$BACKUPFILEDIR
 
    ### Done!
