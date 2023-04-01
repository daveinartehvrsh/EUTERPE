import random
from lib.datastructs import *

def random_round(list):
    rnd = [0.1, 0.2, 0.3, 0.4, 0.5]
    out_list = []
    for x in list:
        y = x + random.choice(rnd)
        out_list.append(int(y))
    return out_list

def load_from_str(scheme_str):
    data = []
    for value in scheme_str.split(', '):
        data.append(float(value))
    return data

def convert_to_len(data, lenght, raw=False):
    rate = int(lenght/len(data) + 0.9)
    longer = np.repeat(data, rate)
    resized = np.resize(longer, lenght)
    if raw:
        return resized, longer
    else:
        return resized
    
def make_rantune(len, prob=0.5):        
    return random.choices([0, -12], [prob, 1-prob], k=len)

def make_ranbinary(len, prob=0.5):
    return random.choices([1, 0], [prob, 1-prob], k=len)

def make_ones(len):
    scheme = []
    for i in range(len):
        scheme.append(1)
    return scheme