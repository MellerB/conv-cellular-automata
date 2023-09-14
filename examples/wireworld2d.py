import sys

sys.path.append("..")
from automaton import Automaton
from display import Display2D
import numpy as np


WIRE = 1
HEAD = 2
TAIL = 3


T = 10
TR = 100
R = 1000
RB = 10000
B = 100000
BL = 1000000
L = 10000000
LT = 100000000
C = 1000000000

kernel = [[LT, T, TR], [L, C, R], [BL, B, RB]]


def rule(x):
    t = x // T % 10
    tr = x // TR % 10

    r = x // R % 10
    rb = x // RB % 10

    b = x // B % 10
    bl = x // BL % 10

    l = x // L % 10
    lt = x // LT % 10

    center = x // C % 10
    head = [t, tr, r, rb, b, bl, l, lt].count(HEAD)

    if center == HEAD:
        return TAIL
    if center == TAIL:
        return WIRE
    if center == WIRE and head > 0 and head <= 2:
        return HEAD
    else:
        return center


size = 35


matrix = np.zeros((size, size))
matrix[4 : size // 3, size // 2] = WIRE
matrix[1:4, size // 2 + 1] = WIRE
matrix[1:4, size // 2 - 1] = WIRE
matrix[0, size // 2] = WIRE
matrix[size // 3 : -size // 3, size // 3 : -size // 3] = WIRE
matrix[-size // 3 - 1, :] = WIRE
matrix[size // 3 + 1 : -size // 3, size // 3 + 1 : -size // 3 - 1] = 0
matrix[16:18, 10:13] = WIRE
matrix[16, 11] = 0
matrix[16:18, 21:24] = WIRE
matrix[17, 22] = 0
matrix[1, size // 2 - 1] = TAIL
matrix[2, size // 2 - 1] = HEAD
matrix[2, size // 2 + 1] = HEAD
matrix[3, size // 2 + 1] = TAIL

n_iters = 50
automaton = Automaton(init_matrix=matrix, kernel=kernel, rule=rule, wrap=True)
record = automaton.run(n_iters)
record = np.array(record) / 3
print(np.max(record))


disp = Display2D(record, mode="alternative", offscreen=False, color="o4", fps=5)
disp.draw_all()
