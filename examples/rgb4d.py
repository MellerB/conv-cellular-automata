import sys

sys.path.append("..")
from automaton import Automaton
from display import Display4D
import numpy as np


a = 3


kernel = np.full((a, a, a, a), 1)


RED = 1
BLUE = 100
GREEN = 10000


def rule(x):
    if x == 0:
        return 0

    green = x // GREEN % 100
    blue = x // BLUE % 100
    red = x // RED % 100

    a = [red, blue, green]
    a.sort(reverse=True)
    m = a[0]
    if m == a[1]:
        return 0
    if m == red:
        return RED
    if m == blue:
        return BLUE
    if m == green:
        return GREEN
    return 0


size = 20


n_iters = 200

matrix = np.random.choice(
    [0, RED, GREEN, BLUE], size=(size, size, size, size), p=[0.97, 0.01, 0.01, 0.01]
)
automaton = Automaton(init_matrix=matrix, kernel=kernel, rule=rule, wrap=True)
record = automaton.run(n_iters)

record = np.array(record)
record[record == GREEN] = 2
record[record == BLUE] = 3


record = record / 3


disp = Display4D(
    record,
    mode="regular",
    offscreen=False,
    filename="video.mp4",
    fps=10,
    cut_invariant=True,
)
disp.draw_all()
