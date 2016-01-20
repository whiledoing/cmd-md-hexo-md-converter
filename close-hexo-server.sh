#!/bin/bash
# need grep -v conver-hexo-server.sh this name
HEXO_PS_ID=$(ps aux | grep hexo | egrep -v "grep|$0" | awk '{print $2}') 

# close it if found
if [[ $HEXO_PS_ID == "" ]]; then
    echo 'no hexo server found'
    exit 1
else
    kill -9 $HEXO_PS_ID
    echo "success shutdown hexo local server - pid $HEXO_PS_ID"
    exit 0
fi
