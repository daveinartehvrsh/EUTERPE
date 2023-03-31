import random
from lib.datastructs import *

def random_round(list):
    rnd = [0.1, 0.2, 0.3, 0.4, 0.5]
    out_list = []
    for x in list:
        y = x + random.choice(rnd)
        out_list.append(int(y))
    return out_list

def create_rantune_scheme(len):
    scheme = []
    for i in range(len):
        value = random.randint(0, 1)
        scheme.append(value*-12)
    return scheme