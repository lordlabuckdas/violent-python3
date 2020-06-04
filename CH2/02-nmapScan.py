import nmap, argparse

def nmapScan(tgtHost,tgtPort):
    nmScan = nmap.PortScanner()
    nmScan.scan(tgtHost,tgtPort)
    state=nmScan[tgtHost]['tcp'][int(tgtPort)]['state']
    print("[*] " + tgtHost + " tcp/" + tgtPort + " " + state)

def main():
    parser = argparse.ArgumentParser(description='nmap scanner')
    parser.add_argument('-H', dest='tgtHost', type=str,help='specify target host',required=True)
    parser.add_argument('-p', dest='tgtPort', type=str,help='specify target port[s] separated by comma',required=True)
    args = parser.parse_args()
    tgtHost = args.tgtHost
    tgtPorts = args.tgtPort.split(',')
    
    for tgtPort in tgtPorts:
        nmapScan(tgtHost, tgtPort)


if __name__ == '__main__':
    main()
