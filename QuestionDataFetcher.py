import requests
from bs4 import BeautifulSoup
 
class getQuestionData:

    def __init__(self, url):
        self.url = url
        self.data = None
        
    def getHtmlContent(self):
        htmlContent = requests.get(self.url).text
        self.data = BeautifulSoup(htmlContent, "lxml")
            
    def getAnswers(self):
        self.getHtmlContent()
        answerstbodys = self.data.find("div", attrs={"class": "datagrid"}).table.findAll("tbody")
        answerList = []
        for tbody in answerstbodys:
            for td in tbody.tr.findAll("td"):
                answerList.append(td.text)
        return answerList
