import sys

sys.path.append("..")
from automaton import Automaton
from display import Display3D
import numpy as np


RED = 1
BLUE = 100
GREEN = 10000


a = 3


kernel = np.full((a, a, a), 1)


def rule(x):
    if x == 0:
        return 0

    green = x // GREEN % 100
    blue = x // BLUE % 100
    red = x // RED % 100

    m = np.max([red, blue, green])
    if m == red:
        return RED
    if m == blue:
        return BLUE
    if m == green:
        return GREEN
    return 0


size = 30


n_iters = 200

matrix = np.random.choice(
    [0, RED, GREEN, BLUE], size=(size, size, size), p=[0.97, 0.01, 0.01, 0.01]
)
automaton = Automaton(init_matrix=matrix, kernel=kernel, rule=rule, wrap=True)
record = automaton.run(n_iters)

record = np.array(record)
record[record == GREEN] = 2
record[record == BLUE] = 3


record = record / 3


disp = Display3D(
    record,
    offscreen=False,
    mode="alternative",
    filename=f"video.mp4",
    color="b4",
    fps=10,
    cut_invariant=True,
)
disp.draw_all()
