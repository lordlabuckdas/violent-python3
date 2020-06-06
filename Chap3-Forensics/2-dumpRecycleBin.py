import os
from winreg import *
import binascii

def sid2user(sid):
    try:
        key = OpenKey(HKEY_LOCAL_MACHINE,
       r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\ProfileList" + '\\' + sid)
        (value, type) = QueryValueEx(key, 'ProfileImagePath')
        user = value.split('\\')[-1]
        return user
    except:
        return sid


def returnDir():
    dirs=['C:\\Recycler\\','C:\\Recycled\\','C:\\$Recycle.Bin\\']
    for recycleDir in dirs:
        if os.path.isdir(recycleDir):
            return recycleDir
    return None


def findRecycled(recycleDir):
    dirList = os.listdir(recycleDir)
    for sid in dirList:
        files = os.listdir(recycleDir + sid)
        user = sid2user(sid)
        print('[*] Listing Recycle Bin Files For User: ' + str(user))
        for file in files:
            try:
                with open(recycleDir+sid+'\\'+file,'rb') as f:
                    hexVal=binascii.hexlify(f.read()).decode()[56:]
                fullName=str(binascii.a2b_hex(hexVal)).replace(r'\x00', '')[2:-1].replace('\\\\', '\\')
                if fullName[1]!=':':
                    continue
                print('[+] Found File: ' + fullName)
            except:
                pass


def main():
    recycledDir = returnDir()
    findRecycled(recycledDir)


if __name__ == '__main__':
    main()
