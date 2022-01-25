#!/usr/bin/python3
from doctest import TestResults
from Crawler import Crawler

BASE_URL = input("BASE_URL: ")
PAYLOAD_PATH = input("PAYLOAD_PATH: ")

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
    
CrawlerObj = Crawler(BASE_URL, PAYLOAD_PATH)
CrawlerObj.initTree()
CrawlerObj.fillTree(CrawlerObj.tree.root)
listFilesRecursively(CrawlerObj.tree.root)