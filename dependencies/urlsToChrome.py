import sys
import subprocess
import optparse
import os
import pdb

def openCount():
    while True:
        a = raw_input('How many tabs?: ')
        return a

def main():
    parser = optparse.OptionParser('usage%prog ' + '-u <url list>')
    parser.add_option('-u', dest='listLoc', type='string', help='specifies url list')
    (options, args) = parser.parse_args()
    if not (options.listLoc):
        parser.error("-u <url list> --- is required")

    #basic file checks
    try:
        urlList = open(options.listLoc, 'r')
    except:
        print "urlList (-u) could not open"
        exit()

    sdata = urlList.readlines()
    data = [data.replace('\n', '') for data in sdata]
    print "Length: " + str(len(data))
    #data = list(set(data))
    length = len(data)
    lineReader = 0

    #Apologize for this code.. haha I'm so used to 'loop do'

    while True:
        count = openCount()
        cur = lineReader
        lineReader += int(count)
        print 'Count: '+str(lineReader)+'/'+str(length)
        devnull = open(os.devnull, 'r')
        for x in xrange(len(data[cur:lineReader])):
            subprocess.call("chromium-browser " + data[cur+x], shell=True)
        if cur>length-1:
            print "Finished"
            exit()

if __name__ == '__main__':
    main()
