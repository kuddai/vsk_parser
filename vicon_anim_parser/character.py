import numpy as np
from numbers import Real
from transforms3d import euler

"""
module to represent character skeleton
Standalone probes can be represented by single free joint.
"""

class Transform(object):
    """
    4x4 matrix which contains current position and rotation of element (joint).
    Useful intermediate representation for rendering and storing.
    """

    def __init__(self, m4x4 = None):
        if m4x4 is None:
            m4x4 = np.eye(4)
        assert m4x4.shape == (4,4)
        self.m4x4 = m4x4

    @staticmethod
    def create_hom_mat(rot, trans=np.zeros(3)):
        m4x4 = np.eye(4)
        m4x4[0:3, 0:3] = rot
        m4x4[0:3, 3] = trans
        return  m4x4

    @staticmethod
    def create_transform(rot, trans=np.zeros(3)):
        result = Transform()
        result.rotation = rot
        result.translation = trans
        return result


    @staticmethod
    def from_euler(x,y,z):
        """
        return 3x3 rotation matrix
        """
        return Transform.from_euler2(x, y, z)
        # from math import radians
        # x = radians(x)
        # y = radians(y)
        # z = radians(z)
        # return Transform.from_euler_rad(x, y, z)

    @staticmethod
    def from_euler2(x,y,z):
        """
        just to check whether transforms3d library is right or not
        return 3x3 rotation matrix
        """

        from math import radians, cos, sin
        x = radians(x)
        y = radians(y)
        z = radians(z)


        Rx = np.array([[ 1,       0,       0     ],
                        [ 0,       cos(x), -sin(x)],
                        [ 0,       sin(x),  cos(x)]])

        Ry = np.array([[ cos(y),  0,       sin(y)],
                        [ 0,       1,            0],
                        [-sin(y),  0,       cos(y)]])

        Rz = np.array([[ cos(z), -sin(z),       0],
                        [ sin(z),  cos(z),       0],
                        [ 0,       0,            1]])

        return np.dot(Rx, np.dot(Ry, Rz))

    @staticmethod
    def from_euler_rad(x, y, z):
        """
        return 3x3 rotation matrix
        rotation is intrinsic xyz rotation
        (rotations around axes of rotating coordinate system).
        """
        return euler.euler2mat(x, y, z, axes="rxyz")

    @staticmethod
    def from_axis_pair(*rot_deg):
        from math import radians
        rot_rad = map(radians, rot_deg)
        axis = np.array(map(float, rot_rad))
        magnitude = np.linalg.norm(axis)
        if abs(magnitude) < 0.0001:
            # magnitude = angle is too small -> rotation is just identity matrix
            return np.eye(3)
        else:
            axis = axis / magnitude
            return Transform.rotate_around_rad(axis, magnitude)

    @staticmethod
    def rotate_around_rad(axis, angle_rad):
        """
        http://inside.mines.edu/fs_home/gmurray/ArbitraryAxisRotation/
        :param axis: vector 3
        :param angle_rad: angle in radians
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

        cos_t = cos(angle_rad)
        sin_t = sin(angle_rad)

        return np.array([[u2 + (1-u2)*cos_t,      uv*(1-cos_t) - w*sin_t, uw*(1-cos_t) + v*sin_t],
                         [uv*(1-cos_t) + w*sin_t, v2 + (1-v2)*cos_t,      vw*(1-cos_t) - u*sin_t],
                         [uw*(1-cos_t) - v*sin_t, vw*(1-cos_t) + u*sin_t, w2 + (1-w2)*cos_t     ]])

    @staticmethod
    def rotate_around(axis, angle_deg):
        from math import radians
        return Transform.rotate_around_rad(axis, radians(angle_deg))

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
        self.segment_name = ""

    def is_root(self):
        return self.current_id == 0

    def store_params(self, *params):
        """
        save additional parameter specific for this joint
        (important for subclasses) fF
        """
        pass

    def move(self, *params):
        pass


class JointBall(Joint):

    def move(self, *rot_euler):
        """
        :param rot_euler: euler angles in degrees
        """
        assert len(rot_euler) == 3, rot_euler
        assert all(isinstance(arg, Real) for arg in rot_euler), rot_euler

        rx, ry, rz = rot_euler
        #rot = Transform.from_axis_pair(rx, ry, rz)
        #rot = Transform.from_euler(rx, ry, rz)
        rot = Transform.from_euler_rad(rx, ry, rz)
        #transf = Transform.create_transform(rot)
        self.transform.rotation = np.dot(self.transform.rotation, rot)
        #self.transform.rotation = np.dot(rot, self.transform.rotation)
        #self.transform.rotation = rot

class JointFree(Joint):

    def move(self, *rot_euler_pos):
        """
        :param rot_euler_pos: euler angles in degrees and positions
        """
        assert len(rot_euler_pos) == 6, rot_euler_pos
        assert all(isinstance(arg, Real) for arg in rot_euler_pos), rot_euler_pos

        rx, ry, rz, x, y, z = rot_euler_pos
        #do rotation

        #rot = Transform.from_axis_pair(rx, ry, rz)
        #rot = Transform.from_euler(rx, ry, rz)
        rot = Transform.from_euler_rad(rx, ry, rz)
        #translation
        trans = np.array([x, y, z])

        #in the file pre-orientation is 0 for all free joints and initial
        #self.transform.rotation is unit matrix  ->
        #self.transform * transf and transf * self.transform are the same
        transf = Transform.create_transform(rot, trans)
        self.transform = self.transform * transf
        #self.transform = transf


class JointHinge(Joint):

    def store_params(self, *axis):
        assert len(axis) == 3, len(axis)
        assert all(isinstance(arg, Real) for arg in axis)

        self.axis = np.array(axis)

    def move(self, *angle_deg):
        """
        :param angle_deg: angle in degrees
        """
        assert len(angle_deg) == 1, angle_deg
        assert all(isinstance(arg, Real) for arg in angle_deg), angle_deg
        angle_deg = angle_deg[0]

        #rot = Transform.rotate_around(self.axis, angle_deg)
        rot = Transform.rotate_around_rad(self.axis, angle_deg)
        #one degree of freedom ->
        #np.dot(self.transform.rotation, rot) and np.dot(rot, self.transform.rotation) are the same
        self.transform.rotation = np.dot(self.transform.rotation, rot)

        #transf = Transform.create_transform(rot)
        #self.transform = transf * self.transform

class JointUniversal(Joint):

    def store_params(self, *axis):
        assert len(axis) == 6, len(axis)
        assert all(isinstance(arg, Real) for arg in axis)

        self.axis1 = np.array(axis[:3])
        self.axis2 = np.array(axis[3:])

    def move(self, *angles):
        """
        :param angles: angles in degrees
        """
        assert len(angles) == 2, angles
        assert all(isinstance(arg, Real) for arg in angles), angles
        angle1, angle2 = angles

        rot1 = Transform.rotate_around_rad(self.axis1, angle1)
        rot2 = Transform.rotate_around_rad(self.axis2, angle2)
        # rot1 = Transform.rotate_around(self.axis1, angle1)
        # rot2 = Transform.rotate_around(self.axis2, angle2)

        rot = np.dot(rot1, rot2)

        #in the file pre-orientation is 0 for unversal joints and initial
        #self.transform.rotation is unit matrix  ->
        #np.dot(self.transform.rotation, rot) and np.dot(rot, self.transform.rotation) are the same
        self.transform.rotation = np.dot(self.transform.rotation, rot)
        #
        # transf = Transform.create_transform(rot)
        # self.transform = transf * self.transform



class Skeleton(object):
    def __init__(self, joints, name2joint_id=None, segment2joint_id=None, init_global_trans=True):
        self.joints = joints

        if init_global_trans:
            self.global_transforms = self._create_global_transforms()
        else:
            self.global_transforms = None

        if name2joint_id is None:
            name2joint_id = self._create_name2joint_id()
        self.name2joint_id = name2joint_id

        if segment2joint_id is None:
            segment2joint_id = self._create_segment2joint_id()
        self.segment2joint_id = segment2joint_id

    def get_joint_id2children(self):
        joint_id2children = [[]] * self.get_num_joints()
        for joint in self.joints:
            children_ids = [child.current_id for child in self.joints if child.parent_id == joint.current_id]
            joint_id2children[joint.current_id] = children_ids

        return joint_id2children

    def get_joints_names(self):
        return self.name2joint_id.keys()

    def get_joint_by_name(self, name):
        joint_id = self.name2joint_id[name]
        return self.joints[joint_id]

    def get_joint_by_segment_name(self, name):
        joint_id = self.segment2joint_id[name]
        return self.joints[joint_id]

    def get_global_transforms_by_name(self, name):
        joint_id = self.name2joint_id[name]
        return self.global_transforms[joint_id]

    def move_to_origin(self):
        root = self.get_root()
        root.transform.translation = np.zeros(3)
        self.update_global_transforms()

    def get_root(self):
        return self.joints[0]

    def get_num_joints(self):
        return len(self.joints)

    def update_global_transforms(self):
        """
        this function must be called after each change of skeleton's joints
        """
        self.global_transforms = self._create_global_transforms()

    def _create_global_transforms(self):
        joints = self.joints
        calc_glob_transf = self._calc_global_transform
        return [calc_glob_transf(joint_id) for joint_id in xrange(len(joints))]
        
    def _calc_global_transform(self, joint_id):
        joint = self.joints[joint_id]
        result = joint.transform.m4x4

        while not joint.is_root():
            joint = self.joints[joint.parent_id]
            result = np.dot(joint.transform.m4x4, result)

        return Transform(result)

    def _create_segment2joint_id(self):
        joints = self.joints
        return {joints[joint_id].segment_name: joint_id for joint_id in xrange(len(joints))}

    def _create_name2joint_id(self, joints=None):
        joints = self.joints
        return {joints[joint_id].name: joint_id for joint_id in xrange(len(joints))}

    def rescale_joints(self, factor):
        for joint in self.joints:
            joint.transform.translation = joint.transform.translation * factor

    def swap_axes(self, unitary_matrix):
        assert unitary_matrix.shape == (4, 4), "wrong shape %s" % unitary_matrix.shape
        for joint in self.joints:
            joint.transform.m4x4 = np.dot(np.dot(unitary_matrix, joint.transform.m4x4), unitary_matrix)

    def swap_Y_Z_axes(self):
        unitary_matrix_y2z = np.array([[1,0,0,0], [0,0,1,0], [0,1,0,0], [0,0,0,1]])
        self.swap_axes(unitary_matrix_y2z)

    def embed_rotations(self):
        from copy import deepcopy
        glob_transf = self._create_global_transforms()
        joints = deepcopy(self.joints)
        for joint in joints:
            if joint.is_root():
                joint.transform.rotation = np.eye(3)
                continue

            rot = glob_transf[joint.parent_id].rotation
            joint.transform.rotation = np.eye(3)
            joint.transform.translation = np.dot(rot, joint.transform.translation)

        self.joints = joints

    def clone(self):
        from copy import deepcopy
        joints = deepcopy(self.joints)
        skeleton = Skeleton(joints, self.name2joint_id, self.segment2joint_id, init_global_trans=False)
        return skeleton








