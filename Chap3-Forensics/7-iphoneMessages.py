import os
import sqlite3
import argparse


def isMessageTable(iphoneDB):
    try:
        conn = sqlite3.connect(iphoneDB)
        c = conn.cursor()
        c.execute('SELECT tbl_name FROM sqlite_master \
          WHERE type==\"table\";')
        for row in c:
            if 'message' in str(row):
                return True
    except:
        return False


def printMessage(msgDB):
    try:
        conn = sqlite3.connect(msgDB)
        c = conn.cursor()
        c.execute('select datetime(date,\'unixepoch\'),\
          address, text from message WHERE address>0;')
        for row in c:
            date = str(row[0])
            addr = str(row[1])
            text = row[2]
            print('\n[+] Date: '+date+', Addr: '+addr + ' Message: ' + text)
    except:
        pass


def main():
    parser = argparse.ArgumentParser(description='iphone db parser')
    parser.add_argument('-p', dest='pathName', type=str, help='specify skype profile path', required=True)
    args = parser.parse_args()
    
    pathName = args.pathName
    dirList = os.listdir(pathName)
    for fileName in dirList:
        iphoneDB = os.path.join(pathName, fileName)
        if isMessageTable(iphoneDB):
            try:
                print('\n[*] --- Found Messages ---')
                printMessage(iphoneDB)
            except:
                pass


if __name__ == '__main__':
    main()
