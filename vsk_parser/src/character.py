import numpy as np

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

class Skeleton(object):
    def __init__(self, joints):
        self.joints = joints

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

class Joint(object):
    def __init__(self, current_id, parent_id):

        self.transform = Transform()
        self.current_id = current_id
        self.parent_id = parent_id
        self.name = ""

    def is_root(self):
        return self.current_id == 0



