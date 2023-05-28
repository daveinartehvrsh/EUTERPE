import random
import numpy as np
from lib.components.abstract.abstract import ValueComponent

class Scheme(ValueComponent):
    
    def load_from_str(self, scheme_str):
        temp = []
        for value in scheme_str.split(','):
            temp.append(float(value))
        self.data = temp

    def convert_to_len(self, lenght):
        rate = int(lenght/len(self.data) + 0.9)
        longer = np.repeat(self.data, rate)
        resized = np.resize(longer, lenght)
        self.data = resized

    def get_info(self):
        return super().get_info()

def load_from_str(scheme_str):
    data = []
    for value in scheme_str.split(', '):
        data.append(float(value))
    return data

def convert_to_len(data, lenght):
    rate = int(lenght/len(data) + 0.9)
    longer = np.repeat(data, rate)
    resized = np.resize(longer, lenght)
    return resized
    
def make_rantune(len, prob=0.5):
    temp = random.choices([0, -12], [prob, 1-prob], k=len)
    scheme = Scheme()
    scheme.set_data(temp)
    return scheme

def make_ranbinary(len, prob=0.5):
    temp = []
    if isinstance(prob, float):
        prob = np.repeat(prob, len)
    else:
        prob = load_from_str(prob)
        prob = convert_to_len(prob, len)
    for i in range(len):
        temp.append(random.choices([1, 0], [prob[i], 1-prob[i]], k=1)[0])
    scheme = Scheme()
    scheme.set_data(temp)
    return scheme

def make_ones(len):
    temp = []
    for i in range(len):
        temp.append(1)
    scheme = Scheme()
    scheme.set_data(temp)
    return scheme

def make_zeros(len):
    temp = []
    for i in range(len):
        temp.append(0)
    scheme = Scheme()
    scheme.set_data(temp)
    return scheme