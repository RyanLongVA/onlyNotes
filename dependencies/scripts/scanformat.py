#This is just a ugly but compact (enough) and full output meant for me to iterate through

import sys
import os
import pdb
import re

class BreakIt(Exception): pass

def main():
    if len(sys.argv) <= 1:
        print "\nSpecify the arguments:\n"
        print "python scanformat.py <dataDestination/target>"
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
    # scanFile formatting
    scanContent = scanFile.readlines()
    scanContent = [x.strip() for x in scanContent]
    for a in scanContent:
        if a.startswith('Host:'):
            a = a.split('()')
            fhost = a[0].replace('Host: ', '').replace(' ', '')
            fports = a[1].replace('Ports: ', '').replace('Port: ', '')
            # looking if the hosts exists
            if fhost not in hosts:
                hosts[fhost] = {'ports': [fports], 'cnames': []}
            else:
                # looking if the port exists

                # Note: Yes I'm negating some of the longer banners or 
                # service returns, but most of the information is just 
                # repetitive and destroys what cleanliness I have

                cports = re.findall(r'([\d]*[\d])', fports)[0]
                try:
                    for b in hosts[fhost]['ports']:
                        if cports == re.findall(r'([\d]*[\d])', fports)[0]:
                            raise BreakIt
                    hosts[fhost]['ports'] += [fports]
                except BreakIt:
                    pass

    # ipformatting
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
                    hosts[b]['cnames'] += [a[0]]
                    break
    # for now we're just going to assume this is creating everything from afresh, and not checking for existing notes and modifying them... future plan
    for a in hosts:
        ab = a.split('&&')
        ip = ab[-1]
        resolver = a[0]
        cnames = hosts[a]['cnames']
        port = hosts[a]['ports']
        print '> IP: ' + ip
        print '> A Record: ' + ab[0]
        print 'CNAMES: '
        for b in hosts[a]['cnames']:
            print '\t ->' + b
        print 'Ports: '
        for b in hosts[a]['ports']:
            print '\t ->' + b

        print '\n'
main()
