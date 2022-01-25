class DirectoryTree:
    def __init__(self, rootObj):
        self.root = self.createNodeFromObj(rootObj)

    def createNodeFromObj(self, obj):
        return Node(obj['url'], obj['parent'], obj['files'], obj['childDir'])

class Node:
    def __init__(self, url, parent, files, childDir):
        self.dir = childDir
        self.child = []
        self.whoami = url
        self.parent = parent
        self.files = files
    
    def addChild(self, node):
        self.child.append(node)