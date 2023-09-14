import sys

sys.path.append("..")
from automaton import Automaton
from display import Display2D
import numpy as np

T = 100
R = 1000
B = 10000
L = 100000
C = 1000000

kernel = [[0, T, 0], [L, C, R], [0, B, 0]]

tt = 1
tr = 2
tb = 3
tl = 4
one = 5


def rule(x):
    t = x // T % 10
    r = x // R % 10
    b = x // B % 10
    l = x // L % 10
    c = x // C % 10
    fullBox = False
    if c >= one:
        fullBox = True
        c -= one
    if c in [tt, tr, tb, tl]:
        return fullBox * one

    gofrom = 0

    if t % one == tb:
        gofrom = t
    if r % one == tl:
        gofrom = r
    if b % one == tt:
        gofrom = b
    if l % one == tr:
        gofrom = l

    if gofrom >= one:
        gofrom -= one

    if gofrom != 0:
        if fullBox:  # central is one
            if gofrom == 4:
                return 1
            else:
                return gofrom + 1

        else:  # central is zero
            if gofrom == 1:
                return 4 + one
            else:
                return gofrom - 1 + one
    return fullBox * one


size = 100


matrix = np.zeros((size, size))
matrix[size // 2, size // 2] = tl


n_iters = 20000
automaton = Automaton(init_matrix=matrix, kernel=kernel, rule=rule, wrap=True)
record = automaton.run(n_iters)
record = np.array(record) / one


disp = Display2D(record, offscreen=False, color="g4", fps=200)
disp.draw_all()
