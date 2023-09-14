import sys

sys.path.append("..")
from automaton import Automaton
from display import Display2D
import numpy as np
from wire_classic import run
from time import perf_counter, sleep


WIRE = 1
HEAD = 2
TAIL = 3




T =  10
TR = 100
R =  1000
RB = 10000
B =  100000
BL = 1000000
L =  10000000
LT = 100000000
C =  1000000000

kernel = [[LT, T, TR], 
          [L, C, R], 
          [BL, B, RB]]

def rule(x):
    center = x // C % 10

    if center==HEAD:
        return TAIL
    if center==TAIL:
        return WIRE
    if center==WIRE:
        t = x // T % 10
        tr = x // TR % 10

        r = x // R % 10
        rb = x // RB % 10

        b = x // B % 10
        bl = x // BL % 10

        l = x // L % 10
        lt = x // LT % 10
    
        head = [t,tr,r,rb,b,bl,l,lt].count(HEAD)
        if head == 1 or head ==2:
            return HEAD
        else: return center
    else:
        return center

size = 400
n_iters = 1

matrix = np.zeros((size, size))
matrix[4:size//3,size//2]=WIRE
matrix[1:4,size//2+1]=WIRE
matrix[1:4,size//2-1]=WIRE
matrix[0,size//2]=WIRE
matrix[5:,:]=WIRE
matrix[-size//3-1,:]=WIRE
matrix[1,size//2-1]=TAIL
matrix[2,size//2-1]=HEAD
matrix[2,size//2+1]=HEAD
matrix[3,size//2+1]=TAIL





record = []
times = []




automaton = Automaton(init_matrix=matrix, kernel=kernel, rule=rule, wrap=True)
record = automaton.run(n_iters)

disp = Display2D(np.array(record)/TAIL, mode="alternative", offscreen=True, color="g4", fps=10, filename="dense.mp4")
disp.draw_all()