import argparse, socket, threading

screenLock = threading.Semaphore(value=1)

def connScan(tgtHost, tgtPort):
	try:
		connSkt=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		connSkt.connect((tgtHost, tgtPort))
		connSkt.send(b'ViolentPython\r\n')
		results = connSkt.recv(1024).decode().strip('\n')
		screenLock.acquire()
		print('[+] %d/tcp open' % tgtPort)
		print('[+] ' + results)
	except:
		screenLock.acquire()
		print('[-] %d/tcp closed' % tgtPort)
	finally:
		screenLock.release()
		connSkt.close()

def portScan(tgtHost,tgtPorts):
	try:
	    tgtIP = socket.gethostbyname(tgtHost)
	except:
	    print("[-] Cannot resolve '%s': Unknown host" % tgtHost)
	    return

	try:
	    tgtName = socket.gethostbyaddr(tgtIP)
	    print('[+] Scan Results for: ' + tgtName[0])
	except:
	    print('[+] Scan Results for: ' + tgtIP)

	socket.setdefaulttimeout(1)
	for tgtPort in tgtPorts:
	    t=threading.Thread(target=connScan,args=(tgtHost, int(tgtPort)))
	    t.start()


def main():
	parser=argparse.ArgumentParser(description="Port Scanner")
	parser.add_argument('-H',dest='tgtHost',type=str,help='specify target host',required=True)
	parser.add_argument('-p',dest='tgtPorts',type=str,help='specify target port(s) separated by commas w/o spaces',required=True)
	args=parser.parse_args()
	tgtPorts = args.tgtPorts.split(',')
	tgtHost = args.tgtHost
	portScan(tgtHost, tgtPorts)

if __name__ == '__main__':
	main()
