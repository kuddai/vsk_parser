from transforms3d import euler
from math import radians, degrees
from vicon_anim_parser.src.character import Transform
from numpy.testing import assert_almost_equal
import numpy as np

args = map(radians, [0, 90, -45])
a = euler.euler2mat(*args, axes='rxyz')
b = Transform.from_euler_rad(*args)

np.set_printoptions(precision=3, suppress=True)

print a
print map(degrees, euler.mat2euler(a, axes="rxyz"))
print b
print assert_almost_equal(a, b)
