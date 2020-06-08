import dpkt
import socket
import pygeoip
import argparse
gi = pygeoip.GeoIP('/opt/GeoIP/Geo.dat')


def retGeoStr(ip):
    try:
        rec = gi.record_by_name(ip)
        city = rec['city']
        country = rec['country_code3']
        if city != '':
            geoLoc = city + ', ' + country
        else:
            geoLoc = country
        return geoLoc
    except:
        return 'Unregistered'


def printPcap(pcap):
    for (ts, buf) in pcap:
        try:
            eth = dpkt.ethernet.Ethernet(buf)
            ip = eth.data
            src = socket.inet_ntoa(ip.src)
            dst = socket.inet_ntoa(ip.dst)
            print('[+] Src: ' + src + ' --> Dst: ' + dst)
            print('[+] Src: ' + retGeoStr(src) + '--> Dst: ' + retGeoStr(dst) + '\n')
        except:
            pass


def main():
    parser = argparse.ArgumentParser(description='ip and address')
    parser.add_argument('-p', dest='pcapFile', type=str, help='specify pcap filename', required=True)
    args = parser.parse_args()
    pcapFile = args.pcapFile
    f = open(pcapFile,'rb')
    pcap = dpkt.pcap.Reader(f)
    printPcap(pcap)
    f.close()


if __name__ == '__main__':
    main()

