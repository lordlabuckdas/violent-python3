import socket
import os
import sys

def retBanner(ip,port):
	try:
		socket.setdefaulttimeout(2)
		s=socket.socket()
		s.connect((ip,port))
		banner=s.recv(1024).decode().strip('\n')
		s.close()
		return banner
	except Exception as e:
		print('[-] ' + ip + ':' + str(port) + ' - ' + str(e))
		return

def checkVulns(banner, filename):
	with open(filename,'r') as f:
		for line in f.read().splitlines():
			if line in banner:
				print('[+] Server is vulnerable: ' + banner)

def main():
	if len(sys.argv) == 2:
		filename=sys.argv[1]
		if not os.path.isfile(filename):
			print('[-] ' + filename + ' does not exist')
			exit(0)
		if not os.access(filename,os.R_OK):
			print('[-] ' + filename + ' access denied')
			exit(0)
	else:
		print('[-] Usage: ' + str(sys.argv[0]) + ' <vuln filename>')
		exit(0)
	portList = [21,22,25,80,110,443]
	for x in range(1,255):
		ip = '10.0.2.' + str(x)
		for port in portList:
			banner = retBanner(ip, port)
			if banner:
				print('[+] ' + ip + ':'+ str(port) + ' - ' + banner)
				checkVulns(banner, filename)

if __name__ == '__main__':
	main()

