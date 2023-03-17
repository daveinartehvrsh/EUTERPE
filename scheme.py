from classes import Component
class Scheme(Component):
    def __init__(self, name='scheme'):
        self.name = name
        self.data = []
    
    def load_scheme(self, scheme):
        self.data = scheme
        self.steps = len(self.data)
        #print(self.data, self.steps)
    
    def load_from_str(self, scheme_str):
        data = []
        for value in scheme_str.split(', '):
            data.append(value)
        self.load_scheme(data)
    
    def getInfo():
        ...

