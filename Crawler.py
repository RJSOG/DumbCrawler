import requests
from Directory import DirectoryTree, Node
from Parser import Parser
import os 

class Crawler:
    def __init__(self, base_url, path):
        self.base_url = base_url
        self.RootPath = path
        self.parser = Parser()
        if(self.login()):
            url = self.base_url+self.RootPath
            self.rootChild = self.listDir(url,True)
                
    def get(self, url, headers):
        return requests.get(url, headers=headers)

    def post(self, url, data):
        return requests.post(url, data=data, allow_redirects=True)

    def initTree(self):
        self.rootObj = self.getNodeObj(self.rootChild, self.rootUrl, None)
        self.tree = DirectoryTree(self.rootObj)    

    def fillTree(self, parent_node):
        parent_dir = parent_node.dir
        parent_url = parent_node.whoami
        if(parent_dir != []):
            for folder in parent_dir:
                url = parent_url + folder
                allChild = self.listDir(url, False)
                nodeObj = self.getNodeObj(allChild, url, parent_node)
                actual_node = self.tree.createNodeFromObj(nodeObj)
                parent_node.addChild(actual_node)
                parent_node = actual_node
                self.fillTree(parent_node)
            return True
        else:
            return True
            
    def getNodeObj(self, childArr, url, parent):
        files, childDir = self.getFilesAndDirFromChilds(childArr)
        NodeObj = {
            'url': url,
            'parent': parent,
            'files': files,
            'childDir': childDir
        }
        return NodeObj

    def getFilesAndDirFromChilds(self, childArr):
        files = []
        dir = []
        for pathElem in childArr:
            actual_path, tailElem = os.path.split(pathElem)
            elemSplit = tailElem.split('.')
            if(elemSplit[0] == '' or len(elemSplit) == 2):
                if(tailElem != '..'):
                    files.append(tailElem) 
            else:
                dir.append(tailElem)
        return files, dir

    def listDir(self, url, isRoot):
        if(isRoot):
            self.rootUrl = url
        body = self.get(url, self.headers).text
        self.parser.newBody(body)
        div = self.parser.getDiv('main')
        childRef = self.parser.getAllHrefFromDiv(div)
        return childRef

    def login(self):
        try:
            LOGIN_URL = f'{self.base_url}p=login'
            data = {
                'username':'test',
                'password':'test',
                'submitted':'ofcourse'
            }
            body = self.post(LOGIN_URL, data)
            cookie = body.headers['Set-Cookie']
            headers = {
                'Cookie': cookie
            }
            self.headers = headers
            return True
        except Exception as error:
            print('[X_X] - Error: ' + str(error))
            return False

    