from classes import Component
import numpy as np
import random

def random_round(list):
    rnd = [0.1, 0.2, 0.3, 0.4, 0.5]
    out_list = []
    for x in list:
        y = x + random.choice(rnd)
        out_list.append(int(y))
    return out_list

class Scheme(Component):
    def __init__(self, name='scheme'):
        self.name = name
        self.data = np.array([])
    
    def load_scheme(self, scheme):
        self.data = np.array(scheme)
        self.steps = len(self.data)
    
    def load_from_str(self, scheme_str):
        data = []
        for value in scheme_str.split(', '):
            data.append(float(value))
        self.load_scheme(data)

    def convert_to_len(self, lenght, raw=False):
        rate = int(lenght/self.steps + 0.9)
        longer = np.repeat(self.data, rate)
        resized = np.resize(longer, lenght)
        if raw:
            return resized, longer
        else:
            return resized

    
    
    def getInfo():
        ...

def main():
    scheme = Scheme()
    scheme.load_from_str('1, 0, 1')
    print(scheme.convert_to_len(19))

if __name__ == '__main__':
    main()
