import requests
from Question import Question

class UrlFormator:
    #Returns the formated url to collect the question Data from

    def __init__(self):
        #Defines the basic format for the url 
        self.base_url = 'https://campus.geva.co.il/mobile/read/public.php?page=bhinaPS_{month}{year}_{chapter_type}{chapter_num}.html'


    @staticmethod
    def get_chapter_type(chapter_type, month, year):
        #Converts the chapter type to the format used in the url
        if chapter_type == 'm':
            return 'perekmilulit'
        if chapter_type == 'k':
            return 'perekkamutit'
        if chapter_type == 'a':
            return 'perekanglit'
        raise Exception('Chapter type is invalid!')

    @staticmethod
    def get_month_chars(month, year_chars):
        #Converts month to the format used in the url
        #print(month)
        if month == '7':
            return UrlFormator.handle_july(year_chars)
        elif month == '10':
            return UrlFormator.handle_october(year_chars)
        else:
            if month == '2':
                return 'feb'
            if month == '4':
                return 'apr'
            if month == '9':
                return 'spt'
            if month == '12':
                return 'dec'

            raise Exception('Unable to convert month!')
        
    @staticmethod
    def get_year_chars(year):
        #Converts the year to the format used in The url
        return year % 2000
    
    @staticmethod
    def handle_july(year):
        #handles the month of July to avoid exceptions
        if year > 13 and year < 17 or year == 20:
            return 'july'
        return 'jul'
    
    @staticmethod
    def handle_october(year):
        #handles the month of October to avoid exceptions
        if year == 14 or year == 12:
            return 'oct'
        else:
            return 'spt'
        
    def format_url(self, chapter_type, chapter_num, year, month):
        # returns the valid form of the url if possible
        try:
            year_chars = self.get_year_chars(year)
            formated_chapter_type = self.get_chapter_type(chapter_type, month, year)
            test_date = self.get_month_chars(month, year)
            url = self.validate_url(formated_chapter_type, chapter_num, year_chars, test_date)
            return url
        except:
            raise Exception('Unable to create url!')
                    
    def validate_url(self, chapter_type, chapter_num, year, month):
        #throws exception if the url is invalid
        url = self.base_url.format(month = month, year = year, chapter_type = chapter_type, chapter_num = chapter_num)
        content = requests.get(url).text
        if not content == 'Unable to connect to the site':
            return url
        if chapter_type[-1] == "t":
            # tries to shorten the chapter type if the url is incorrect
            return self.validate_url(chapter_type[:-1], chapter_num, year, month)
        raise Exception('Unable to connect to the site')


