from bs4 import BeautifulSoup

class Parser:
    def newBody(self, body):
        self.body = body
        self.soup = BeautifulSoup(body, 'html.parser')

    def getDiv(self, id):
        return self.soup.find('div', {'id': id})
        
    def getLiFomBody(self, body):
        return body.find_all('li')

    def getAllHrefFromDiv(self, div):
        body = self.getLiFomBody(div)
        allLinks = []
        for li in body:
            a = li.find('a', href=True)
            if(a.text):
                allLinks.append(a['href'])
        return allLinks

    