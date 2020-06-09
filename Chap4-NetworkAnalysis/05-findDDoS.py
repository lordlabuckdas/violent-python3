import dpkt
import argparse
import socket
THRESH = 1000


def findDownload(pcapFile):
    f = open(pcapFile, 'rb')
    pcap = dpkt.pcap.Reader(f)
    for (ts, buf) in pcap:
        try:
            eth = dpkt.ethernet.Ethernet(buf)
            ip = eth.data
            src = socket.inet_ntoa(ip.src)
            tcp = ip.data
            http = dpkt.http.Request(tcp.data)
            if http.method == 'GET':
                uri = http.uri.lower()
                if '.zip' in uri and 'loic' in uri:
                    print('[!] ' + src + ' Downloaded LOIC.')
        except:
            pass
    f.close()


def findHivemind(pcapFile):
    f = open(pcapFile, 'rb')
    pcap = dpkt.pcap.Reader(f)
    for (ts, buf) in pcap:
        try:
            eth = dpkt.ethernet.Ethernet(buf)
            ip = eth.data
            src = socket.inet_ntoa(ip.src)
            dst = socket.inet_ntoa(ip.dst)
            tcp = ip.data
            dport = tcp.dport
            sport = tcp.sport
            if dport == 6667:
                if '!lazor' in tcp.data.decode().lower():
                    print('[!] DDoS Hivemind issued by: '+src)
                    print('[+] Target CMD: ' + tcp.data.decode())
            if sport == 6667:
                if '!lazor' in tcp.data.decode().lower():
                    print('[!] DDoS Hivemind issued to: '+src)
                    print('[+] Target CMD: ' + tcp.data.decode())
        except:
            pass
    f.close()


def findAttack(pcapFile):
    f = open(pcapFile, 'rb')
    pcap = dpkt.pcap.Reader(f)
    pktCount = {}
    for (ts, buf) in pcap:
        try:
            eth = dpkt.ethernet.Ethernet(buf)
            ip = eth.data
            src = socket.inet_ntoa(ip.src)
            dst = socket.inet_ntoa(ip.dst)
            tcp = ip.data
            dport = tcp.dport
            if dport == 80:
                stream = src + ':' + dst
                if stream in pktCount.keys():
                    pktCount[stream] = pktCount[stream] + 1
                else:
                    pktCount[stream] = 1
        except:
            pass

    for stream in pktCount:
        pktsSent = pktCount[stream]
        if pktsSent > THRESH:
            src = stream.split(':')[0]
            dst = stream.split(':')[1]
            print('[+] '+src+' attacked '+dst+' with ' + str(pktsSent) + ' pkts.')
    
    f.close()


def main():
    parser = argparse.ArgumentParser(description='loic download checker')

    parser.add_argument('-p', dest='pcapFile', type=str, help='specify pcap filename', required=True)
    parser.add_argument('-t', dest='thresh', type=int, help='specify threshold count ')

    args = parser.parse_args()
    if args.thresh != None:
        THRESH = args.thresh
    pcapFile = args.pcapFile
    
    findDownload(pcapFile)
    findHivemind(pcapFile)
    findAttack(pcapFile)


if __name__ == '__main__':
    main()
