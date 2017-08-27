#!/bin/bash

#Basic input check
if [ $# -eq 0 ]; then 
    echo "\nNo argument was provided.\n \nPlease specify list (urls) to push into the urlsToChrome.py" 
    exit 1
fi
FILE=$1
if [ ! -f $FILE ]; then 
    echo "The file you provided, apparently, does not exist: $FILE"
    exit 1
fi    

echo "Input file atleast exists... starting chrome" 
gnome-terminal -x sh -c 'chromium-browser --proxy-server="127.0.0.1:8080" --profile-directory="Profile 2"'
python dependencies/urlsToChrome.py -u $FILE
