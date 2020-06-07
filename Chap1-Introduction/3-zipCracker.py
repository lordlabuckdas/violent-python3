import zipfile
import argparse
from threading import Thread

def extractFile(zFile,password):
	try:
		zFile.extractall(pwd=password.encode())
		print('[+] Found password: ' + password)
	except:
		pass

def main():
	ap=argparse.ArgumentParser(description='Crack Zipfiles with Password list')
	ap.add_argument('-f',dest='zname',type=str,help='specify zip file',required=True)
	ap.add_argument('-d',dest='dname',type=str,help='specify dictionary file',required=True)
	args = ap.parse_args()
	zname=args.zname
	dname=args.dname
	try:
		zFile=zipfile.ZipFile(zname)
	except FileNotFoundError:
		print('Zip File Not Found!')
		exit(0)
	try:
		with open(dname) as passFile:
			for password in passFile.read().splitlines():
				t=Thread(target=extractFile,args=(zFile,password))
				t.start()
	except FileNotFoundError:
		print('Dictionary File Not Found')
		exit(0)

if __name__ == '__main__':
	main()