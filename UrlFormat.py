'''
    Statistic tool for the psychometry (SAT) test in Israel collects
    Data from Yoel Geva's website and returns the most frequent answer for
    each question
    Author: Lior Furman
'''

from bs4 import BeautifulSoup
import requests
import datetime


class urlFormator: #Returns the formated url to collect the question Data from

    def __init__(self): #Defines the basic format for the url 
        self.baseUrl = 'https://campus.geva.co.il/mobile/read/public.php?page=bhinaPS_{month}{year}_{perekType}{perekNum}.html'


    @staticmethod
    def getPerekType(typeOfPerek, month, year): #Converts the chapter type to the format used in the url
        return 'perekmilulit' if typeOfPerek=='m' else \
                   'perekkamutit' if typeOfPerek == 'k' else \
                   'perekanglit' if typeOfPerek == 'a' else 'error'


    @staticmethod
    def getMonthChars(month, yearChar): #Converts month to the format used in the url
        if yearChar== 12:
            moed = 'oct' if month == 10 else 'dec' if month == 12 else 'Error'
        elif yearChar <= 17:
            if month == 7:
                moed = 'july' if yearChar > 13 and yearChar < 17 else 'jul'
            else:
                moed = 'feb' if month == 2 else\
                'apr' if month == 4 else\
                'oct' if month == 10 and yearChar == 14 else\
                'sep' if month == 10 else\
                'dec' if month == 12 else\
                'Error'
        else:
            moed = 'apr' if month == 4 else\
            'july' if month == 7 and yearChar == 20 else\
            'jul' if month == 7 else\
            'sep' if month == 9 else\
            'dec' if month== 12 else\
            'Error'
        return moed
        
    @staticmethod
    def getYear(year): #Converts the year to the format used in The url
        return year % 2000
        
    def formatUrl(self, perekType, perekNum, year, month):
            #if(month == 4 and year == 2015 and perekType == 'k'):
            #    return "Unable to check"
        lastCharOfYear = self.getYear(year)
        formatedPerekType = self.getPerekType(perekType, month, year)
        moed = self.getMonthChars(month, lastCharOfYear)
        #print(moed)
        url = self.validateUrl(formatedPerekType, perekNum, lastCharOfYear, moed)
        if url == 'Error':
            if perekType == 'k':
                formatedPerekType = 'perekkamuti'

            elif perekType == 'm':
                formatedPerekType = 'perekmiluli'
            return self.validateUrl(formatedPerekType, perekNum, lastCharOfYear, moed)
        else:
            return url
                    
    def validateUrl(self, perekType, perekNum, year, month):
        url = self.baseUrl.format(month = month, year = year, perekType = perekType, perekNum = perekNum)
        content = requests.get(url).text
        if not content == 'Unable to connect to the site':
            return url
        return 'Error'

                
                
        
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
            
class Question:
        
    convertAnswer = {'1\n': '1', '1\r\n': '1', '2\n':'2', '2\r\n': '2', '3\n':'3', '3\r\n':'3', '4\n': '4', '4\r\n': '4'}
        
    def __init__(self, subject, number):
        self.subject = subject
        self.number = number
        self.maxAnswer = 0
        self.answerSum = {'1': 0, '2': 0, '3': 0, '4': 0}
        self.inNumber = None

    def getAnswer(self, year, month, perekNum, answer):
        converted = self.convertAnswerFromHtml(answer)
        if not converted == 0:
            self.answerSum[converted] += 1

    def calcMax(self):
        sum1 = self.answerSum['1']
        sum2 = self.answerSum['2']
        sum3 = self.answerSum['3']
        sum4 = self.answerSum['4']

        maxSum = max(sum1, sum2, sum3, sum4)
        mostFrequent = 'Most Frequent Answer:'
        if sum1 == maxSum:
            mostFrequent += " 1"
            self.inNumber = 1 
        if sum2 == maxSum:
            mostFrequent += " 2"
        if sum3 == maxSum:
            mostFrequent +=  " 3"
        if sum4 == maxSum:
            mostFrequent += " 4"
        self.maxAnswer = mostFrequent
            
    def getAnswerSum(self):
        return self.answerSum
            
    def toString(self):
        return "For question number {num} in perek {subject} {max} \r\n {answerSum}".format(num
            = self.number, subject = self.subject, max = self.maxAnswer, answerSum = self.answerSum)
                
            
    def convertAnswerFromHtml(self, answer):
        try:
            return self.convertAnswer[answer]
        except:
            return 0
        
class Perek:
    monthsAt2012 = [10, 12]
    monthsBefore2017 = [2, 4, 7, 10, 12]
    monthsAfter2017 = [4, 7, 9, 12]
            
    def __init__(self, questionNum, subject):
        self.formatUrl = urlFormator()
        self.questionNum = questionNum
        self.subject = subject
        self.questions = []
        self.createQuestions()
        self.mostFrequent = None
        self.answersTotalSum = None

    def createQuestions(self):
        questions  = {}
        for i in range(self.questionNum):
            self.questions.append(Question(self.subject, i+1))
        return questions
                
    def convertSubject(self):
        if self.subject == 'Miloli - Hebrew':
            return 'm'
        if self.subject == 'Kamuti - Math':
            return 'k'
        if self.subject == 'Anglit - English':
            return 'a'
        else:
            return 'Error'
            
    def getQuestions(self):
        startYear = 2016
        endYear = datetime.datetime.now().year
        startQuestion = 0;
        for year in range(startYear, endYear):
            self.allMoeds(year)
            self.MostFrequent()
            self.calcAllMax()
            self.printResult()
                
    def allMoeds(self, year):
        months = self.monthsAt2012 if year % 2000 == 12 else self.monthsBefore2017 if year%2000 <= 17 else self.monthsAfter2017
        for month in months:
            for j in range(2):
                url = self.formatUrl.formatUrl(self.convertSubject(), j+1, year, month)
                if url == "Error":
                    continue
                questionDataFetcher = getQuestionData(url)
                data = questionDataFetcher.getAnswers()
                for a in range(len(data)):
                    self.questions[a].getAnswer(year, month, j, data[a])

    def calcAllMax(self):
        for question in self.questions:
            question.calcMax()
            
    def printResult(self):
        with open("{subject}.txt".format(subject = self.subject), "w") as f:
            for question in self.questions:
                f.write(question.toString())
                f.write('\r\n')
            f.write(self.mostFrequent)
            f.write('\r\n')
            f.write(str(self.answersTotalSum))
            f.close()

    def MostFrequent(self):
        answers = {'1': 0, '2': 0, '3': 0, '4': 0}
        for a in self.questions:
            sum = a.getAnswerSum()
            answers['1'] += sum['1']
            answers['2'] += sum['2']
            answers['3'] += sum['3']
            answers['4'] += sum['4']
        maxOfPerek = max(answers['1'], answers['2'], answers['3'], answers['4'])
        mostFrequent = "Most frequent answer over all is: "
        if maxOfPerek == answers['1']:
            mostFrequent += ' 1'
        if maxOfPerek == answers['2']:
            mostFrequent += ' 2'
        if maxOfPerek == answers['3']:
            mostFrequent += ' 3'
        if maxOfPerek == answers['4']:
            mostFrequent += ' 4'
        self.mostFrequent = mostFrequent
        self.answersTotalSum = answers
            
            
    def getOne(self):
        return self.questions[0]

class Miloli(Perek):
    def __init__(self):
        super().__init__(23, 'Miloli - Hebrew')

class Kamuti(Perek):
    def __init__(self):
        super().__init__(20, 'Kamuti - Math')
            
class Anglit(Perek):
    def __init__(self):
        super().__init__(22, 'Anglit - English')

class FullTest():
    def __init__(self):
        self.Miloli = Miloli()
        self.Kamuti = Kamuti()
        self.Anglit = Anglit()
            
    def runAll(self):
        self.Miloli.getQuestions()
        self.Kamuti.getQuestions()
        self.Anglit.getQuestions()
                    
FullTest = FullTest()
FullTest.runAll()


