import requests
from Question import Question

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
        
    def formatUrl(self, perekType, perekNum, year, month): # returns the valid form of the url if possible
        lastCharOfYear = self.getYear(year)
        formatedPerekType = self.getPerekType(perekType, month, year)
        moed = self.getMonthChars(month, lastCharOfYear)
        url = self.validateUrl(formatedPerekType, perekNum, lastCharOfYear, moed)
        if url == 'Error':
            if perekType == 'k':
                formatedPerekType = 'perekkamuti'

            elif perekType == 'm':
                formatedPerekType = 'perekmiluli'
            return self.validateUrl(formatedPerekType, perekNum, lastCharOfYear, moed)
        else:
            return url
                    
    def validateUrl(self, perekType, perekNum, year, month): #returns 'error' if the url is invalid
        url = self.baseUrl.format(month = month, year = year, perekType = perekType, perekNum = perekNum)
        content = requests.get(url).text
        if not content == 'Unable to connect to the site':
            return url
        return 'Error'


