import random
import numpy as np

def Scheme(ValueComponent):
    ...

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
    return random.choices([0, -12], [prob, 1-prob], k=len)

def make_ranbinary(len, prob=0.5):
    out = []
    if isinstance(prob, float):
        prob = np.repeat(prob, len)
    else:
        prob = load_from_str(prob)
        prob = convert_to_len(prob, len)
    for i in range(len):
        out.append(random.choices([1, 0], [prob[i], 1-prob[i]], k=1)[0])
    return out

def make_ones(len):
    scheme = []
    for i in range(len):
        scheme.append(1)
    return scheme

def make_zeros(len):
    scheme = []
    for i in range(len):
        scheme.append(0)
    return scheme