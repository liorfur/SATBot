from UrlFormat import urlFormator
from Question import Question
import datetime
from QuestionDataFetcher import getQuestionData


class Perek: # fetches Data for every question in the chapter.
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

    def createQuestions(self): # creates a list of questions
        questions  = {}
        for i in range(self.questionNum):
            question = Question(self.subject, i+1)
            self.questions.append(question)
        return questions
                
    def convertSubject(self): # converts the chapter type 
        if self.subject == 'Miloli - Hebrew':
            return 'm'
        if self.subject == 'Kamuti - Math':
            return 'k'
        if self.subject == 'Anglit - English':
            return 'a'
        else:
            return 'Error'
            
    def getQuestions(self): # feteches data for each question in the chapter from 2012 onwards
        startYear = 2012
        endYear = datetime.datetime.now().year
        startQuestion = 0;
        for year in range(startYear, endYear):
            self.allMoeds(year)
            self.MostFrequent()
            self.calcAllMax()
            self.saveResult()
                
    def allMoeds(self, year): # for each year fetches data for each question and adds it to the question's sum
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

    def calcAllMax(self): # calcuates the most frequent answer for each question
        for question in self.questions:
            question.calcMax()
            
    def saveResult(self): # saves the most frequent question to file
        with open("{subject}.txt".format(subject = self.subject), "w") as f:
            for question in self.questions:
                f.write(question.toString())
                f.write('\r\n')
            f.write(self.mostFrequent)
            f.write('\r\n')
            f.write(str(self.answersTotalSum))
            f.close()

    def MostFrequent(self): # claculates the most frequent question overall
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
            
            
