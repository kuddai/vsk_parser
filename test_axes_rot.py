from math import radians, degrees
from transforms3d import euler, axangles
import matplotlib.pyplot as plt
#this import is necessary for plt.figure().gca(projection='3d') line
#without it there will be exception here:
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
import numpy as np
from math import degrees, radians

fig = plt.figure()
ax = fig.gca(projection='3d')

LENGTH = 200

def show_frame(R, style, msize):
    NR = R * LENGTH
    #
    ax.plot([0, NR[0,0]],  [0, NR[0,1]],  [0, NR[0,2]], style, c="r", markersize=msize)
    ax.plot([0, NR[1,0]],  [0, NR[1,1]],  [0, NR[1,2]], style, c="g", markersize=msize)
    ax.plot([0, NR[2,0]],  [0, NR[2,1]],  [0, NR[2,2]], style, c="b", markersize=msize)
    # point = np.dot(R.T, [0, 169.14, 0])
    # line = zip(point, [0, 0, 0])
    # ax.plot(line[0], line[1], line[2], style, c="r", markersize=msize)

ax.set_xlim3d(-LENGTH, LENGTH)
ax.set_ylim3d(-LENGTH, LENGTH)
ax.set_zlim3d(-LENGTH, LENGTH)

x1, y1, z1 = map(radians, [179.98,  24.13, -157.42])#map(radians, [177.78,	26.0141,	-156.548])
x2, y2, z2 = map(radians, [89.63,  -11.93, 78.65])

print radians(180)

origin = np.array([0,   0, 0])
stick  = np.array([LENGTH, 0, 0])

axes = "rxyz"

def get_angles_rad(x, y, z, axes):
    l2a = {"x": x, "y": y, "z": z}
    angles_rad = []
    for letter in axes[1:]:
        angles_rad.append(l2a[letter])
    return angles_rad

print map(degrees, get_angles_rad(x1, y1, z1, axes))

# R1 = euler.euler2mat(*get_angles_rad(x1, y1, z1, axes), axes=axes)
# R2 = euler.euler2mat(*get_angles_rad(x2, y2, z2, axes), axes=axes)

R1 = euler.euler2mat(x1, y1, z1, axes=axes)
R2 = euler.euler2mat(x2, y2, z2, axes=axes)

show_frame(R1, '-o', 5)
show_frame(R2, '-d', 15)

plt.xlabel('x')
plt.ylabel('y')
plt.show()




