from math import radians, degrees
from transforms3d import euler, axangles
from vicon_anim_parser.src.character import Transform, JointFree
import matplotlib.pyplot as plt
#this import is necessary for plt.figure().gca(projection='3d') line
#without it there will be exception here:
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
import numpy as np


fig = plt.figure()
ax = fig.gca(projection='3d')

LENGTH = 200

def show_frame(R, style, msize):
    NR = R * LENGTH

    ax.plot([0, NR[0,0]],  [0, NR[0,1]],  [0, NR[0,2]], style, c="r", markersize=msize)
    ax.plot([0, NR[1,0]],  [0, NR[1,1]],  [0, NR[1,2]], style, c="g", markersize=msize)
    ax.plot([0, NR[2,0]],  [0, NR[2,1]],  [0, NR[2,2]], style, c="b", markersize=msize)

ax.set_xlim3d(-LENGTH, LENGTH)
ax.set_ylim3d(-LENGTH, LENGTH)
ax.set_zlim3d(-LENGTH, LENGTH)

x1, y1, z1 = [82.41,  -14.24, -4.23]
x2, y2, z2 = [146.15,  51.11, 118.59]

origin = np.array([0,   0, 0])
stick  = np.array([LENGTH, 0, 0])

axes = "rxyz"

R1 = euler.euler2mat(x1, y1, z1, axes=axes)
R2 = euler.euler2mat(x2, y2, z2, axes=axes)

show_frame(R1, '-o', 5)
show_frame(R2, '-d', 15)

plt.xlabel('x')
plt.ylabel('y')
plt.show()




