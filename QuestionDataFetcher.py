import requests
from bs4 import BeautifulSoup
 
class QuestionDataFetcher:
    #gets questions data from html

    def __init__(self, url):
        # defines the url to be used
        self.url = url
        self.data = None
        
    def get_html_content(self):
        # fetches and formats the html content and saves it to 'data' variable
        htmlContent = requests.get(self.url).text
        self.data = BeautifulSoup(htmlContent, "lxml")
            
    def get_answers(self):
        # extracts the answers from the html content
        self.get_html_content()
        answers_tbodys = self.data.find("div", attrs={"class": "datagrid"}).table.find_all("tbody")
        answer_list = []
        for tbody in answers_tbodys:
            for td in tbody.tr.findAll("td"):
                answer_list.append(td.text)
        return answer_list
