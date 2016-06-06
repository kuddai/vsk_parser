import numpy as np
import sys

class Transform(object):
    def __init__(self, m4x4 = None):
        if m4x4 is None:
            m4x4 = Transform.default_m4x4()
        self.m4x4 = m4x4

    @staticmethod
    def default_m4x4():
        m4x4 = np.zeros((4,4))
        m4x4[3,3] = 1
        return m4x4

    @staticmethod
    def from_euler(x,y,z):
        """
        return 3x3 rotation matrix
        >>> np.set_printoptions(precision=3, suppress=True)
        >>> Joint.from_euler( 90, 0, 0)
        array([[ 1.,  0.,  0.],
               [ 0.,  0., -1.],
               [ 0.,  1.,  0.]])

        >>> Joint.from_euler(180, 0, 0)        
        array([[ 1.,  0.,  0.],
               [ 0., -1., -0.],
               [ 0.,  0., -1.]])

        >>> Joint.from_euler(0, 30, 0) 
        array([[ 0.866,  0.   ,  0.5  ],
               [ 0.   ,  1.   ,  0.   ],
               [-0.5  ,  0.   ,  0.866]])

        >>> Joint.from_euler(0, 90, 0)
        array([[ 0.,  0.,  1.],
               [ 0.,  1.,  0.],
               [-1.,  0.,  0.]])

        >>> Joint.from_euler(0, 0, 90)  
        array([[ 0., -1.,  0.],
               [ 1.,  0.,  0.],
               [ 0.,  0.,  1.]])
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

        calc_glob_trans = self.calc_global_transform
        global_transforms = [calc_glob_trans(joint_id) for joint_id in xrange(len(joints))]
        self.global_transforms = global_transforms
        
    def calc_global_transform(self, joint_id):
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


if __name__ == "__main__":
    transform = Transform()
    print transform.translation
    transform.translation = np.array([1.01, 2.02, 3.03])
    print transform.translation, "\n"
    print transform


