from UrlFormat import UrlFormator
from Question import Question
import datetime
from QuestionDataFetcher import QuestionDataFetcher


class Chapter: # fetches Data for every question in the chapter.
    MONTHS_AT_2012 = ['10', '12']
    MONTHS_BEFORE_2017 = ['2', '4', '7', '10', '12']
    MONTHS_AFTER_2017 = ['4', '7', '9', '12']
            
    def __init__(self, num_of_questions, subject):
        self.url_formator = UrlFormator()
        self.num_of_questions = num_of_questions
        self.subject = subject
        self.questions = []
        self.create_questions()
        self.most_frequent = None
        self.answers_sum = None

    def create_questions(self):
        # creates a list of questions
        questions  = {}
        for i in range(self.num_of_questions):
            question = Question(self.subject, i+1)
            self.questions.append(question)
        return questions
                
    def convert_subject(self):
        # converts the chapter type 
        if self.subject == 'Miloli - Hebrew':
            return 'm'
        if self.subject == 'Kamuti - Math':
            return 'k'
        if self.subject == 'Anglit - English':
            return 'a'
        else:
            return 'Error'
            
    def get_questions(self):
        # feteches data for each question in the chapter from 2012 onwards
        start_year = 2012
        end_year = datetime.datetime.now().year
        start_question = 0;
        for year in range(start_year, end_year):
            self.all_test_dates(year)
            self.calc_most_frequent()
            self.calc_all_max()
            self.save_result()
                
    def all_test_dates(self, year):
        # fetches data for each question in all chapters and adds it to the total questions sum
        months = self.get_correct_month_list(year)
        for month in months:
            for j in range(2):
                try:
                    data = self.fetch_questions_data(j+1, year, month)
                    for a in range(len(data)):
                        self.questions[a].get_answer(data[a])
                except:
                    continue
                
    def fetch_questions_data(self, chapter_num, year, month):
        # fetches data from chapter
        try:
            url = self.url_formator.format_url(self.convert_subject(), chapter_num, year, month)
            question_data_fetcher = QuestionDataFetcher(url)
            return question_data_fetcher.get_answers()
        except:
            raise Exception('Could not fetch data!')
            
    def get_correct_month_list(self, year):
        # returns the correct list of months to use according to the year
        if year == 2012:
            return self.MONTHS_AT_2012
        if year <= 2017:
            return self.MONTHS_BEFORE_2017
        else:
            return self.MONTHS_AFTER_2017

    def calc_all_max(self):
        # calcuates the most frequent answer for each question
        for question in self.questions:
            question.calc_max_answers()
            
    def save_result(self):
        # saves the most frequent answers for each question to file
        with open("{subject}.txt".format(subject = self.subject), "w") as f:
            for question in self.questions:
                f.write(question.to_string())
                f.write('\r\n')
            f.write(self.most_frequent)
            f.write('\r\n')
            f.write(str(self.answers_total_sum))
            f.close()

    def calc_most_frequent(self):
        # claculates the most frequent answers overall
        self.calc_answers_sum()
        self.calc_most_frequent_answer(max(self.answers_total_sum.values()))
        
        
    def calc_answers_sum(self):
        #calculates the total number of answer apperances through the questions saved sum
        self.answers_total_sum = {'1': 0, '2': 0, '3': 0, '4': 0}
        
        for question in self.questions: # iterates through the question's saved answer sum
            answer_sum = question.get_answers_sum()
            self.answers_total_sum['1'] += answer_sum['1']
            self.answers_total_sum['2'] += answer_sum['2']
            self.answers_total_sum['3'] += answer_sum['3']
            self.answers_total_sum['4'] += answer_sum['4']
                
    def calc_most_frequent_answer(self, max_sum):
        # recieves the max value of the answer's sum and saves the most frequent answers in str format
        self.most_frequent = "Most frequent answer over all is: "
        
        if max_sum == self.answers_total_sum['1']:
            self.most_frequent += ' 1'
            
        if max_sum == self.answers_total_sum['2']:
            self.most_frequent += ' 2'
            
        if max_sum == self.answers_total_sum['3']:
            self.most_frequent += ' 3'
            
        if max_sum == self.answers_total_sum['4']:
            self.most_frequent += ' 4'    
            
