import argparse
from urllib.parse import urlsplit
from urllib.request import urlopen
from os.path import basename
from bs4 import BeautifulSoup
from PIL import Image
from PIL.ExifTags import TAGS


def findImages(url):
    print('[+] Finding images on ' + url)
    urlContent = urlopen(url).read()
    soup = BeautifulSoup(urlContent,'html5lib')
    imgTags = soup.find_all('img')
    return imgTags


def downloadImage(imgTag):
    try:
        print('[+] Dowloading image...')
        imgSrc = imgTag['src']
        imgContent = urlopen(imgSrc).read()
        imgFileName = basename(urlsplit(imgSrc)[2])
        imgFile = open(imgFileName, 'wb')
        imgFile.write(imgContent)
        imgFile.close()
        return imgFileName
    except:
        return ''


def testForExif(imgFileName):
    try:
        exifData = {}
        imgFile = Image.open(imgFileName)
        info = imgFile._getexif()
        if info:
            for (tag, value) in info.items():
                decoded = TAGS.get(tag, tag)
                exifData[decoded] = value
            exifGPS = exifData['GPSInfo']
            if exifGPS:
                print('[*] ' + imgFileName + ' contains GPS MetaData')
    except:
        pass


def main():
    parser = argparse.ArgumentParser(description='exif extractor')
    parser.add_argument('-u', dest='url', type=str, help='specify url address', required=True)

    args = parser.parse_args()
    url = args.url
    imgTags = findImages(url)
    for imgTag in imgTags:
        imgFileName = downloadImage(imgTag)
        testForExif(imgFileName)


if __name__ == '__main__':
    main()
