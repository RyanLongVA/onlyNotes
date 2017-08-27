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
    parser.add_option('-n', dest='notesLoc', type='string', help='location new/old notes')
    (options, args) = parser.parse_args()
    if not (options.listLoc and options.notesLoc):
        parser.error("-u <url list> && -n <notes> -- are required")

    #basic file checks
    try:
        urlList = open(options.listLoc, 'r')
    except:
        print "urlList (-u) could not open"
        exit()
    try:
        notesLoc = open(options.notesLoc, 'r+')
        print "--> Notes file exists... trying to load"
        pdb.set_trace()
    except IOError:
        print "--> File doesn't exist... creating"
        notesLoc = open(options.notesLoc, 'w+')
    
    sdata = urlList.readlines()
    data = [data.replace('\n', '') for data in sdata]
    print "Length: " + str(len(data))
    #data = list(set(data))
    length = len(data)
    lineReader = 0

    #Apologize for this code.. haha I'm so used to 'loop do'

    while True:
        count = openCount()
        os.system('clear')
        cur = lineReader
        lineReader += int(count)
        print 'Count: '+str(lineReader)+'/'+str(length)
        devnull = open(os.devnull, 'r')
        for x in xrange(len(data[cur:lineReader])):
            subprocess.call("chromium-browser " + data[cur+x], shell=True, stdout=devnull, stderr=devnull)
        if cur>length-1:
            print "Finished"
            exit()

def cleanInput(data):
    print 'data.endswith()'

if __name__ == '__main__':
    main()
