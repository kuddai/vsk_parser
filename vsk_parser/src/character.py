import numpy as np
from numbers import Real

class Transform(object):
    def __init__(self, m4x4 = None):
        if m4x4 is None:
            m4x4 = np.eye(4)
        assert m4x4.shape == (4,4)
        self.m4x4 = m4x4

    @staticmethod
    def from_euler(x,y,z):
        """
        return 3x3 rotation matrix
        """

        from math import radians
        x = radians(x)
        y = radians(y)
        z = radians(z)
        return Transform.from_euler_rad(x, y, z)

    @staticmethod
    def from_euler_rad(x, y, z):
        """
        return 3x3 rotation matrix
        """
        from math import cos, sin
        Rx = np.array([[ 1,       0,       0     ],
                       [ 0,       cos(x), -sin(x)],
                       [ 0,       sin(x),  cos(x)]])

        Ry = np.array([[ cos(y),  0,       sin(y)],
                       [ 0,       1,            0],
                       [-sin(y),  0,       cos(y)]])

        Rz = np.array([[ cos(z), -sin(z),       0],
                       [ sin(z),  cos(z),       0],
                       [ 0,       0,            1]])

        return np.dot(Rz, np.dot(Ry, Rx))

    @staticmethod
    def rotate_around_rad(axis, angle):
        """
        http://inside.mines.edu/fs_home/gmurray/ArbitraryAxisRotation/
        :param axis: vector 3
        :param angle: angle in radians
        :return: rotation by angle around axis
        """
        from math import cos, sin
        from numpy import linalg as LA
        axis = axis / LA.norm(axis)
        u, v, w = axis

        u2 = u*u
        v2 = v*v
        w2 = w*w

        uv = u*v
        uw = u*w
        vw = v*w

        cos_t = cos(angle)
        sin_t = sin(angle)

        return np.array([[u2 + (1-u2)*cos_t,      uv*(1-cos_t) - w*sin_t, uw*(1-cos_t) + v*sin_t],
                         [uv*(1-cos_t) + w*sin_t, v2 + (1-v2)*cos_t,      vw*(1-cos_t) - u*sin_t],
                         [uw*(1-cos_t) - v*sin_t, vw*(1-cos_t) + u*sin_t, w2 + (1-w2)*cos_t     ]])

    @staticmethod
    def rotate_around(axis, angle):
        from math import radians
        return Transform.rotate_around_rad(axis, radians(angle))

    @property
    def rotation(self):
        return self.m4x4[0:3, 0:3]

    @rotation.setter    
    def rotation(self, m3x3):
        self.m4x4[0:3, 0:3] = m3x3

    @property
    def translation(self):
        return self.m4x4[0:3, 3]

    @translation.setter
    def translation(self, value):
        self.m4x4[0:3, 3] = value

    def __mul__(self, other):
        return Transform(np.dot(self.m4x4, other.m4x4))

    def __str__(self):
        return str(self.m4x4)


class Joint(object):
    def __init__(self, current_id, parent_id):

        self.transform = Transform()
        self.current_id = current_id
        self.parent_id = parent_id
        self.name = ""

    def is_root(self):
        return self.current_id == 0

class JointHinge(Joint):

    def store_params(self, *args):
        assert len(args) == 3
        assert all(isinstance(arg, Real) for arg in args)

        self.axis = np.array(args)

    def move(self, angle):
        assert isinstance(angle, Real)

        # rot_trn = Transform()
        # rot_trn.rotation = Transform.rotate_around(self.axis, angle)
        rot = Transform.rotate_around(self.axis, angle)
        rot = np.dot(rot, self.transform.rotation)

        self.transform.rotation = rot

class Skeleton(object):
    def __init__(self, joints):
        self.joints = joints
        self.update_global_transform()

    def update_global_transform(self):
        joints = self.joints
        calc_glob_trans = self._calc_global_transform
        global_transforms = [calc_glob_trans(joint_id) for joint_id in xrange(len(joints))]
        self.global_transforms = global_transforms
        
    def _calc_global_transform(self, joint_id):
        joint = self.joints[joint_id]
        result = joint.transform

        while not joint.is_root():
            joint = self.joints[joint.parent_id]
            result = joint.transform * result

        return result

    def get_num_joints(self):
        return len(self.joints)






