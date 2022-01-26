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
        else:
            print('Login Failed')
                
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
                allHref = self.listDir(url, False)
                nodeObj = self.getNodeObj(allHref, url, parent_node)
                actual_node = self.tree.createNodeFromObj(nodeObj)
                parent_node.addChild(actual_node)
                self.fillTree(actual_node)
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
                if(tailElem != '..'):
                    dir.append(tailElem + '/')
        return files, dir

    def listDir(self, url, isRoot):
        if(isRoot):
            self.rootUrl = url
        body = self.get(url, self.headers).text
        self.parser.newBody(body)
        div = self.parser.getDiv('main')
        childRef = self.parser.getAllHrefFromDiv(div)
        return childRef

    def listFilesRecursively(self, parent):
        if parent.child != []:
            print(parent.whoami)
            print("folder: " + str(parent.dir))
            print('files : ' + str(parent.files))
            for node in parent.child:
                self.listFilesRecursively(node)
            return True
        else:
            print(parent.whoami)
            print('files : ' + str(parent.files))
            return True

    def dumpAllFilesRecursively(self, parent, isRoot):
        if(isRoot):
            ""
            # os.mkdir('root/')
        if(parent.child != []):
            for index in range(0, len(parent.dir)):
                dir = parent.dir[index]
                pathDir = self.getLocalPath(parent, dir)
                index = parent.dir.index(dir)
                node = parent.child[index]
                # os.mkdir(path)
                for file in parent.files:
                    pathFile = self.getLocalPath(parent, file)
                self.dumpAllFilesRecursively(node, False)
        return True

    def getLocalPath(self, parent, elem):
        whoami_path = parent.whoami.replace(self.base_url, '')
        whomai_local_path = whoami_path.replace(self.RootPath, 'root/')
        return os.path.join(whomai_local_path, elem)

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

    