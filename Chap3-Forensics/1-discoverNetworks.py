import os
import argparse
import mechanize
import urllib3
import re
import urllib.parse
from winreg import *


def val2addr(val):
    addr = ''
    for ch in val:
        addr += '%02x ' % ch
    addr = addr.strip(' ').replace(' ', ':')[0:17]
    return addr


def wiglePrint(username, password, netid):
    browser = mechanize.Browser()
    browser.addheaders = [('Accept', 'text/javascript, text/html, application/xml, text/xml, */*'),
    ('Content-type', 'application/x-www-form-urlencoded; charset=UTF-8'),
    ('User-Agent', 'Mozilla/5.0 (Windows NT 5.2; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.47 Safari/536.11r')]
    browser.open('http://wigle.net')
    reqData = urllib.parse.urlencode({'credential_0': username, 'credential_1': password})
    browser.open('https://wigle.net/login', reqData)
    params = {}
    params['netid'] = netid
    params['ssid'] = ''
    params['latrange1'] = ''
    params['latrange2'] = ''
    params['longrange1'] = ''
    params['longrange2'] = ''
    params['lastupdt'] = ''
    reqParams = urllib.parse.urlencode(params)
    respURL = 'https://api.wigle.net/api/v2/network/search?' + reqParams
    # following 3 lines to handle conversion from json to dictionary
    true=1
    false=0
    null=0
    resp = browser.open(respURL).read().decode()
    finData = eval(resp) # eval to convert string dict to dict
    if finData['totalResults']:
        print('Latitude: ' + finData['results'][0]['trilat'])
        print('Longitude: ' + finData['results'][0]['trilong'])
        print('SSID: ' + finData['results'][0]['ssid'])
        print('MAC Addr: ' + finData['results'][0]['netid'])
        print('House Number: ' + finData['results'][0]['housenumber'])
        print('Road: ' + finData['results'][0]['road'])
        print('City: ' + finData['results'][0]['city'])
        print('Region: ' + finData['results'][0]['region'])
        print('Postal Code: ' + finData['results'][0]['postalcode'])
        print('Country: ' + finData['results'][0]['country'])
    else:
        print("[-] Couldn't find accurate information, sorry.")    


def printNets(username, password):
    net = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\NetworkList\Signatures\Unmanaged"
    key = OpenKey(HKEY_LOCAL_MACHINE, net, 0, KEY_READ | KEY_WOW64_64KEY) # adjusted for 32bit python in 64bit windows
    print('[*] Networks You have Joined.')
    for i in range(100):
        try:
            guid = EnumKey(key, i)
            netKey = OpenKey(key, str(guid))
            (n, addr, t) = EnumValue(netKey, 5)
            (n, name, t) = EnumValue(netKey, 4)
            macAddr = val2addr(addr)
            netName = str(name)
            print('[+] ' + netName + '  ' + macAddr)
            wiglePrint(username, password, macAddr)
            CloseKey(netKey)
        except:
            pass
            

def main():
    parser = argparse.ArgumentParser(description='...')
    parser.add_argument('-u', dest='username', type=str, help='specify wigle password',required=True)
    parser.add_argument('-p', dest='password', type=str, help='specify wigle username',required=True)
    args = parser.parse_args()
    username = args.username
    password = args.password
    printNets(username, password)


if __name__ == '__main__':
    main()
