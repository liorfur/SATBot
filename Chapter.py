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
            
            
