import matplotlib.pyplot as plt
#this import is necessary for plt.figure().gca(projection='3d') line
#without it there will be exception here:
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
import numpy as np

#3.5 meters in one direction (7 overall)
G17_SCENE_LENGTH = 3500

class SkeletonDrawer(object):

    def __init__(self, axis, rest_pose_skeleton, color="r", linewidth=4.0, show_names=False):
        #minus root joint
        self.ax = axis
        self.show_names = show_names
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
            if self.show_names:
                self.ax.text(joint_beg[0], joint_beg[1], joint_beg[2], joint.segment_name, size=10, zorder=1, color='k')

        return self.lines

class SegmentsDrawer(object):
    def __init__(self, axis, segment_id2parent_id, color="r", linewidth=4.0):
        def mk_plot(parent_id):
            if parent_id == -1:
                return axis.plot([], [], [], 'o', c=color, linewidth=linewidth)
            else:
                return axis.plot([], [], [], '-', c=color, linewidth=linewidth)

        self.ax = axis
        self.segment_id2parent_id = segment_id2parent_id

        lines = sum([mk_plot(parent_id) for parent_id in segment_id2parent_id], [])
        self.lines = lines

    def reinit(self):
        for line in self.lines:
            line.set_data([], [])
            line.set_3d_properties([])

        return self.lines,

    def draw(self, pose):
        xx, yy, zz = pose
        segment_id2parent_id = self.segment_id2parent_id

        for segment_id, parent_id in enumerate(segment_id2parent_id):
            line = self.lines[segment_id]
            if parent_id == -1:
                #sword and root (display elements without root as large dots)
                line.set_data(xx[segment_id], yy[segment_id])
                line.set_3d_properties(zz[segment_id])
            else:
                line.set_data([xx[segment_id], xx[parent_id]], [yy[segment_id], yy[parent_id]])
                line.set_3d_properties([zz[segment_id], zz[parent_id]])
        return self.lines

    @staticmethod
    def show_pose(pose, segment_id2parent_id, **options):
        scene_length = options.get("scene_length", G17_SCENE_LENGTH)
        view_angle_horiz = options.get("view_angle_horiz", 145)
        view_angle_vertc = options.get("view_angle_vertc", 35)
        hide_axes = options.get("hide_axes", False)

        fig = plt.figure()
        ax = fig.gca(projection='3d')
        ax.view_init(view_angle_vertc, view_angle_horiz)
        scale_scene(ax, scene_length)
        if hide_axes:
            ax.set_axis_off()

        drawer = SegmentsDrawer(ax, segment_id2parent_id)
        drawer.draw(pose)

        plt.show()


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

class MouseDrawer(object):

    def __init__(self, axis, scene_length):
        self.scene_length = scene_length
        mouse_drawer, = axis.plot([], [], [], 'o', c="b", markersize=12)
        mouse_tail, = axis.plot([], [], [], '-', c="b", linewidth=2)

        self.mouse_last_point = mouse_drawer
        self.mouse_tail = mouse_tail
        self.mouse_points = []

    def reinit(self):
        self.mouse_last_point.set_data([], [])
        self.mouse_last_point.set_3d_properties([])
        self.mouse_tail.set_data([], [])
        self.mouse_tail.set_3d_properties([])
        return self.mouse_last_point, self.mouse_tail

    def draw(self, mouse_data):
        if mouse_data is None:
            return self.mouse_last_point, self.mouse_tail

        scene_length = self.scene_length
        mouse_t, mouse_ft = mouse_data
        new_mouse_point = (0, mouse_t*scene_length, mouse_ft*scene_length)
        self.mouse_points.append(new_mouse_point)

        mouse_track_x, mouse_track_y, mouse_track_z = zip(*self.mouse_points)
        self.mouse_tail.set_data(mouse_track_x, mouse_track_y)
        self.mouse_tail.set_3d_properties(mouse_track_z)

        self.mouse_last_point.set_data(new_mouse_point[0], new_mouse_point[1])
        self.mouse_last_point.set_3d_properties(new_mouse_point[2])

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

def get_segments_anim(anim_data, segment_id2parent_id, **options):
    """
    if initial frame is -1 then frames won't be displayed
    """

    global frame_id
    frame_id         = options.get("initial_frame", 1)
    scene_length     = options.get("scene_length", G17_SCENE_LENGTH)
    FPS              = options.get("FPS", 30)
    view_angle_horiz = options.get("view_angle_horiz", 145)
    view_angle_vertc = options.get("view_angle_vertc", 35)
    mouse_curve      = options.get("mouse_curve", [None] * len(anim_data))
    hide_axes        = options.get("hide_axes", False)

    assert len(mouse_curve) == len(anim_data)

    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.view_init(view_angle_vertc, view_angle_horiz)
    scale_scene(ax, scene_length)
    if hide_axes:
        ax.set_axis_off()

    body_drawer = SegmentsDrawer(ax, segment_id2parent_id)
    mouse_drawer = MouseDrawer(ax, scene_length)

    interval = 1000 / FPS # 1 second = 1000 milliseconds

    def show_current_frame():
        global frame_id
        if frame_id <= 0:
            return
        fig.suptitle("frame number %r" % frame_id)
        frame_id += 1
        if frame_id % 500 == 0:
            print "frame number", frame_id

    def init_func():
        return body_drawer.reinit(), mouse_drawer.reinit()

    def animate(data_point):
        show_current_frame()
        body_pose, mouse_data = data_point
        return body_drawer.draw(body_pose), mouse_drawer.draw(mouse_data)

    #blit=False is necessary for Mac OS X (exception otherwise)
    #We need to keep these reference as well, otherwise it would be picked up by GB
    anim = animation.FuncAnimation(fig, animate, frames=zip(anim_data, mouse_curve), interval=interval, init_func=init_func, blit=False, repeat=False)
    plt.xlabel('x')
    plt.ylabel('y')
    return anim

def show_skeleton_structure(skeleton):
    fig = plt.figure()
    ax = fig.gca(projection='3d')

    scale_scene(ax, G17_SCENE_LENGTH)
    skeleton_drawer = SkeletonDrawer(ax, skeleton, show_names=True)
    skeleton_drawer.draw(skeleton)

    plt.xlabel('x')
    plt.ylabel('z')
    plt.show()

