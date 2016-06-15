import matplotlib.pyplot as plt
#this import is necessary for plt.figure().gca(projection='3d') line
#without it there will be exception here:
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
import numpy as np

#3.5 meters in one direction (7 overall)
G17_SCENE_LENGTH = 3500

class SkeletonDrawer(object):

    def __init__(self, axis, rest_pose_skeleton, color="r", linewidth=4.0, show_joint_names=False):
        #minus root joint
        self.ax = axis
        self.show_joint_names = show_joint_names
        num_bones = rest_pose_skeleton.get_num_joints() - 1
        lines = sum([axis.plot([], [], [], '-', c=color, linewidth=linewidth)  for i in xrange(num_bones)], [])
        self.lines = lines

    def reinit(self):
        for line in self.lines:
            line.set_data([], [])
            line.set_3d_properties([])

        return self.lines,

    def draw(self, skeleton):
        #izip to save memory
        from itertools import izip
        glob_transf = skeleton.global_transforms

        #all joints except root (it has id 0 so we need range [1:])
        for line, joint in izip(self.lines, skeleton.joints[1:]):
            joint_beg_id = joint.current_id
            joint_end_id = joint.parent_id

            #center skeleton
            joint_beg = glob_transf[joint_beg_id].translation
            joint_end = glob_transf[joint_end_id].translation

            data = zip(joint_beg, joint_end)
            #flip 1 and 2 to change y and z axis as in our data y is vertical one
            line.set_data(data[0], data[1])
            line.set_3d_properties(data[2])
            if self.show_joint_names:
                self.ax.text(joint_beg[0], joint_beg[1], joint_beg[2], joint.name, size=10, zorder=1, color='k')

        return self.lines


class MarkersDrawer(object):

    def __init__(self, axis, color="g", markersize=7):
        markers_plot, = axis.plot([], [], [], 'o', c=color, markersize=markersize)
        self.markers_plot = markers_plot

    def reinit(self):
        self.markers_plot.set_data([], [])
        self.markers_plot.set_3d_properties([])
        return self.markers_plot

    def draw(self, markers):
        xx, yy, zz = markers
        self.markers_plot.set_data(xx, yy)
        self.markers_plot.set_3d_properties(zz)
        return self.markers_plot

def convert_to_list(obj):
    if hasattr(obj, "__len__"):
        return obj
    else:
        return [obj]

def scale_scene(ax, scene_length):
    ax.set_xlim3d(-scene_length, scene_length)
    ax.set_ylim3d(-scene_length, scene_length)
    ax.set_zlim3d(-scene_length, scene_length)

def draw_scene(*skeleton_animations, **options):
    from itertools import izip_longest, cycle

    global frame_id
    frame_id      = options.get("initial_frame", 1)
    scene_length  = options.get("scene_length", G17_SCENE_LENGTH)
    markers_anim  = options.get("markers_anim", [])
    FPS           = options.get("FPS", 30)

    fig = plt.figure()
    ax = fig.gca(projection='3d')

    palette = cycle(['r', 'c', 'm', 'y', 'k', 'b', 'g'])
    color = next(palette)
    drawers = [MarkersDrawer(ax, color=color)]
    #ensure that single skeleton is converted into list with one element
    skeleton_animations = map(convert_to_list, skeleton_animations)

    for skeleton_anim in skeleton_animations:
        first_pose = skeleton_anim[0]
        color = next(palette)
        skeletonDrawer = SkeletonDrawer(ax, first_pose, color=color)
        drawers.append(skeletonDrawer)

    scale_scene(ax, scene_length)
    interval = 1000 / FPS # 1 second = 1000 milliseconds
    anim_data = izip_longest(markers_anim, *skeleton_animations)

    def init_func():
        graph_objects = tuple()
        for drawer in drawers:
            graph_objects += (drawer.reinit(), )
        return graph_objects

    def animate(scene_data):
        global frame_id
        fig.suptitle("frame number %r" % frame_id)
        frame_id += 1

        graph_objects = tuple()
        for drawer, scene_object in zip(drawers, scene_data):
            if scene_object is not None:
                graph_objects += (drawer.draw(scene_object), )
        return graph_objects


    #blit=False is necessary for Mac OS X (exception otherwise)
    #We need to keep these reference as well, otherwise it would be picked up by GB
    anim = animation.FuncAnimation(fig, animate, frames=anim_data, interval=interval, init_func=init_func, blit=False, repeat=False)

    plt.xlabel('x')
    plt.ylabel('y')
    plt.show()


def draw_skeleton(ax, skeleton, show_joint_names):
    glob_trans = skeleton.global_transforms
    #all joints except root (it has id 0 so we need range [1:])
    for joint in skeleton.joints[1:]:

        joint_beg_id = joint.current_id
        joint_end_id = joint.parent_id

        joint_beg = glob_trans[joint_beg_id].translation
        joint_end = glob_trans[joint_end_id].translation

        x, y, z = joint_beg
        line = zip(joint_beg, joint_end)

        #here inverse because y and z axis are inversed
        ax.plot(line[0], line[2], line[1], color="b")
        ax.scatter(x, z, y, color="r", marker=".")
        if show_joint_names:
            ax.text(x, z, y, joint.name, size=10, zorder=1, color='k')

def show_skeleton_structure(skeleton):
    fig = plt.figure()
    ax = fig.gca(projection='3d')

    scale_scene(ax, G17_SCENE_LENGTH)
    skeleton_drawer = SkeletonDrawer(ax, skeleton, show_joint_names=True)
    skeleton_drawer.draw(skeleton)

    plt.xlabel('x')
    plt.ylabel('z')
    plt.show()

