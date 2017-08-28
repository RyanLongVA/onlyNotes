import sys
import os

if (len(sys.argv) <= 2):
    print "The point is to take a directory full of url lists and spit out the ones that are actually unique"
    print "WARNING: THIS WILL PURGE THE DIRECTORY GIVEN"
    print "\nSyntax:"
    print "\tpython main.py directory_of_lists overall_file"
    exit()

def main():
    original = filter(None, open(sys.argv[2], 'r').read().split('\n'))
    flist = original
    for filename in os.listdir(sys.argv[1]):
        sfile = filter(None, open(str(sys.argv[1]+filename), 'r').read().split('\n'))
        flist = set(sfile + flist)
        os.remove(sys.argv[1]+filename)
    print len(flist)
    print len(original)
    if (len(flist) == len(original)):
        print "No duplicates were found\n\nPurging given directory"
        exit()
    else:
        unique = list(set(flist) - set(original))
        newOriginal = open(sys.argv[2], 'a')
        for un in unique:
            print un
            newOriginal.write('\n'+un)
main()
