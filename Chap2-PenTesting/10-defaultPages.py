import ftplib

def returnDefault(ftp):
    try:
        dirList = ftp.nlst()
    except:
        dirList = []
        print('[-] Could not list directory contents.')
        print('[-] Skipping To Next Target.')
        return

    retList = []
    for fileName in dirList:
        fn = fileName.lower()
        if '.php' in fn or '.htm' in fn or '.asp' in fn:
            print('[+] Found default page: ' + fileName)
            retList.append(fileName)
    return retList

if __name__ == '__main__':
    host = '10.0.2.6'
    userName = 'guest'
    passWord = 'guest'
    ftp = ftplib.FTP(host)
    try:
        ftp.login(userName, passWord)
        returnDefault(ftp)
    except:
        print('[-] Error logging in.')
    
