import time
import argparse
from scapy.all import *
from IPy import IP as IPTEST

ttlValues = {}
THRESH = 5


def checkTTL(ipsrc, ttl):
    if IPTEST(ipsrc).iptype() == 'PRIVATE':
        return

    if ipsrc not in ttlValues.keys():
        pkt = sr1(IP(dst=ipsrc) / ICMP(), retry=0, timeout=1, verbose=0)
        ttlValues[ipsrc] = pkt.ttl

    if abs(int(ttl) - int(ttlValues[ipsrc])) > THRESH:
        print('\n[!] Detected Possible Spoofed Packet From: ' + ipsrc)
        print('[!] TTL: ' + ttl + ', Actual TTL: ' + str(ttlValues[ipsrc]))


def testTTL(pkt):
    try:
        if pkt.haslayer(IP):
            ipsrc = pkt.getlayer(IP).src
            ttl = str(pkt.ttl)
            checkTTL(ipsrc, ttl)
    except:

        pass


def main():
    parser = argparse.ArgumentParser('sppof detector')
    parser.add_argument('-i', dest='iface', type=str, help='specify network interface')
    parser.add_argument('-t', dest='thresh', type=int, help='specify threshold count ')

    args = parser.parse_args()
    
    if args.iface == None:
        conf.iface = 'eth0'
    else:
        conf.iface = args.iface

    if args.thresh != None:
        THRESH = args.thresh
    else:
        THRESH = 5

    sniff(prn=testTTL, store=0)


if __name__ == '__main__':
    main()
