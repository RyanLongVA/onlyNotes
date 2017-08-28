import sys
import os
import pdb
import re

def main():
    if len(sys.argv) <= 1:
        print "\nSpecify the arguments:\n"
        print "python scanformat.py dataDestination/target"
        exit()
    try:
        ipFile = open(sys.argv[1]+'.ips', 'r')
        cnameFile = open(sys.argv[1]+'.cnames', 'r')
        scanFile = open(sys.argv[1]+'.ips.scan', 'r')
    except IOError as err:
        print "\n\n[-] Something went wrong loading the scanformat.py files"
        print "{0}".format(err)
        exit()

    hosts = {}
    # scan formatting
    scanContent = scanFile.readlines()
    scanContent = [x.strip() for x in scanContent]
    print "Formatting scan"
    for a in scanContent:
        if a.startswith('Host:'):
            a = a.split('()')
            fhost = a[0].replace('Host: ', '').replace(' ', '')
            fports = a[1].replace('Ports: ', '').replace('Port: ', '')
            print "[+] Host Found: " + fhost
            print "\t\t Port: " + fports
            if fhost not in hosts:
                hosts[fhost] = {'ports': [fports], 'cnames': []}
            else:
                hosts[fhost]['ports'] += [fports]

    #  ipformatting
    # for the keys in the host dictionary iterate through to find cnames and continue up to correlate other cnames (chains)
    for a in ipFile:
        a = a.split(':')
        a = [x.strip() for x in a]
        if a[1] in hosts:
            hosts[a[0]+'&&'+a[1]] = hosts.pop(a[1])

    # looking for cnames
    should_restart = True
    while should_restart:
        should_restart = False
        for a in cnameFile:
            a = a.split(':')
            a = [x.strip() for x in a]
            for b in hosts:
                ba = b.split('&&')
                if a[1] == ba[0]:
                    # pdb.set_trace()
                    should_restart = True
                    hosts[b]['cnames'] += a[0]
                    break
    for a in hosts:
        print "\n\n"
        print hosts.keys()

main()
