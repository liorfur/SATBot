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
