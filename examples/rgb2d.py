import sys

sys.path.append("..")
from automaton import Automaton
from display import Display2D
import numpy as np


RED = 1
BLUE = 100
GREEN = 10000


a = 5


kernel = np.full((a, a), 1)


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


size = 100


matrix = np.random.choice(
    [0, RED, GREEN, BLUE], size=(size, size), p=[0.25, 0.25, 0.25, 0.25]
)


n_iters = 300
automaton = Automaton(init_matrix=matrix, kernel=kernel, rule=rule, wrap=True)
record = automaton.run(n_iters)
record = np.array(record)

record = np.array(record)
record[record == BLUE] = 2
record[record == GREEN] = 3


record = record / 3

disp = Display2D(
    record,
    mode="alternative",
    filename="video.mp4",
    fps=10,
    cut_invariant=True,
)
disp.draw_all()


size = 30
