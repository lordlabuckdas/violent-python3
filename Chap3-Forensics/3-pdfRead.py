import PyPDF2
import argparse


def printMeta(fileName):
    with open(fileName,'rb') as file:
        pdfFile = PyPDF2.PdfFileReader(file)
        docInfo = pdfFile.getDocumentInfo()
        print('[*] PDF MetaData For: ' + str(fileName))
        for metaItem in docInfo:
            print('[+] ' + metaItem + ': ' + docInfo[metaItem])


def main():
    parser = argparse.ArgumentParser(description='pdf file metadata')
    parser.add_argument('-F', dest='fileName', type=str, help='specify PDF file name',required=True)

    args = parser.parse_args()
    fileName = args.fileName
    printMeta(fileName)


if __name__ == '__main__':
    main()
