import ftplib

def anonLogin(hostname):
    try:
        ftp = ftplib.FTP(hostname)
        ftp.login('anonymous', 'me@your.com')
        print('[*] ' + str(hostname) +' FTP Anonymous Login Succeeded.')
        ftp.quit()
        return True
    except:
        print('[-] ' + str(hostname) + ' FTP Anonymous Login Failed.')
        return False

if __name__ == '__main__' :
    host = '10.0.2.6'
    anonLogin(host)