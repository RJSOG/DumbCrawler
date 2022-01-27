#!/usr/bin/python3
from Crawler import Crawler

BASE_URL = input("BASE_URL: ")
PAYLOAD_PATH = input("PAYLOAD_PATH: ")

CrawlerObj = Crawler(BASE_URL, PAYLOAD_PATH)
CrawlerObj.initTree()
CrawlerObj.fillTree(CrawlerObj.tree.root)
# CrawlerObj.listFilesRecursively(CrawlerObj.tree.root)
CrawlerObj.dumpAllFilesRecursively(CrawlerObj.tree.root, True)