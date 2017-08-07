import numpy as np

def state_ones(state):
    z = np.zeros(18)
    for i, s in enumerate(state):
        if s == 1:
            z[i] = 1
        elif s == -1:
            z[i+9] = 1
    return z

def ones_state(ones):
    z = np.zeros(9)
    for i, s in enumerate(ones):
        if s == 1:
            if i < 9:
                z[i] = 1
            else:
                z[i-9] = -1
    return z

k = {0: "- ", -1: "O ", 1: "X "}
def vis(state):
    s = ""
    for i in range(9):
        if i%3 == 0:
            s += "\n"
        s += k[state[i]]
        
    print(s)