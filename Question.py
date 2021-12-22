class Question:
    # creates question data
        
    CONVERT_ANSWER = {'1\n': '1', '1\r\n': '1', '2\n':'2', '2\r\n': '2', '3\n':'3', '3\r\n':'3', '4\n': '4', '4\r\n': '4'}
        
    def __init__(self, subject, number):
        # receives the details about the question 
        self.subject = subject
        self.number = number
        self.max_answers = ''
        self.answers_sum = {'1': 0, '2': 0, '3': 0, '4': 0}

    def get_answer(self, answer):
        # receives currect answer and adds to total sum
        converted = self.convert_answer_from_html(answer)
        if not converted == 0:
            self.answers_sum[converted] += 1

    def calc_max_answers(self):
        # calculates which answer is the most frequent
        all_answers_sum = self.answers_sum.values()
        max_sum = max(all_answers_sum)
        self.format_max_answers(max_sum)
        
    def format_max_answers(self, max_sum):
        # saves the most frequent answers
        most_frequent = 'Most Frequent Answers:'
        if self.answers_sum['1'] == max_sum:
            most_frequent += " 1"
        if self.answers_sum['2'] == max_sum:
            most_frequent += " 2"
        if self.answers_sum['3'] == max_sum:
            most_frequent +=  " 3"
        if self.answers_sum['4'] == max_sum:
            most_frequent += " 4"
        self.max_answers = most_frequent
        
    def get_answers_sum(self):
        # returns the total answer sum
        return self.answers_sum
            
    def to_string(self):
        # returns a string with the final details
        return "For question number {num} in chapter {subject} {max_answers} \r\n {answers_sum}".format(num
            = self.number, subject = self.subject, max_answers = self.max_answers, answers_sum = self.answers_sum)  
            
    def convert_answer_from_html(self, answer):
        # converts the form of the question recieved from the HTML file
        try:
            return self.CONVERT_ANSWER[answer]
        except:
            return 0
