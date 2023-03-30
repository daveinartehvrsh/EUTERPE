import random

def random_round(list):
    rnd = [0.1, 0.2, 0.3, 0.4, 0.5]
    out_list = []
    for x in list:
        y = x + random.choice(rnd)
        out_list.append(int(y))
    return out_list