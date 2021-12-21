class FullTest():
    def __init__(self):
        self.Miloli = Miloli()
        self.Kamuti = Kamuti()
        self.Anglit = Anglit()
            
    def runAll(self):
        self.Miloli.getQuestions()
        self.Kamuti.getQuestions()
        self.Anglit.getQuestions()
