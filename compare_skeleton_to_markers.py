import sys

import numpy as np
from math import radians, degrees
from vicon_anim_parser.scene_drawer import draw_scene
from vicon_anim_parser.csv_anim_parser import parse_skeleton_animations, parse_markers
from vicon_anim_parser.vsk_parser import parse_skeleton_structure

def gen_skeleton_anims(vsk_file_name, csv_file_name, beg_frame, end_frame):
    from copy import deepcopy
    print "vsk parsed"
    skeleton_original = parse_skeleton_structure(vsk_file_name)

    np.set_printoptions(suppress=True, precision=4)

    for i, raw_animation in enumerate(parse_skeleton_animations(csv_file_name)):
        frame_id = i + 1

        if frame_id < beg_frame:
            continue
        if frame_id > end_frame:
            break

        skeleton = deepcopy(skeleton_original)
        for joint_name in skeleton.get_joints_names():
            joint = skeleton.get_joint_by_name(joint_name)
            params = raw_animation[joint_name]
            joint.move(*params)

        skeleton.update_global_transforms()

        # print frame_id
        # print skeleton.get_global_m4x4_by_name("Hips_Spine")
        yield skeleton


#data -> tuples of skeleton and markers for each frame
def draw_skeleton_and_markers(data, beg_frame=1, FPS=30):
    from vicon_anim_parser.scene_drawer import SkeletonDrawer
    import matplotlib.pyplot as plt
    #this import is necessary for plt.figure().gca(projection='3d') line
    #without it there will be exception here:
    from mpl_toolkits.mplot3d import Axes3D
    import matplotlib.animation as animation

    fig = plt.figure()
    ax = fig.gca(projection='3d')

    rest_pose_skeleton = data[0][0]
    skeletonDrawer = SkeletonDrawer(ax, rest_pose_skeleton)
    markersDrawer  = MarkersDrawer(ax)

    def init():
        skeleton_lines = skeletonDrawer.reinit()
        markers_plot = markersDrawer.reinit()
        return skeleton_lines, markers_plot

    def animate(i):
        frame_id = beg_frame + i
        #due to first element being 0
        skeleton, markers = data[i]
        skeleton_lines = skeletonDrawer.draw(skeleton)
        markers_plot   = markersDrawer.draw(markers)
        fig.suptitle("frame_id %r" % frame_id)

        return skeleton_lines, markers_plot

    scale_axes_equally(ax, 2000)

    interval = 1000/FPS
    #blit=False is necessary for Mac OS X (exception otherwise)
    #We need to keep these reference as well, otherwise it would be picked up by GB
    anim = animation.FuncAnimation(fig, animate, frames=len(data), interval=interval, init_func=init, blit=False, repeat=False)

    plt.xlabel('x')
    plt.ylabel('y')
    plt.show()

def main():
    vsk_file_name = sys.argv[1]
    csv_file_name = sys.argv[2]

    print vsk_file_name, csv_file_name

    beg_frame = 1
    end_frame = 650

    skeletons = list(gen_skeleton_anims(vsk_file_name, csv_file_name, beg_frame, end_frame))
    #print "skeletons parsed", len(skeletons)
    markers_anim = list(parse_markers(csv_file_name))[beg_frame - 1:end_frame]
    print "markers parsed", len(markers_anim)

    draw_scene(skeletons, markers_anim=markers_anim, initial_frame=beg_frame, FPS=30)


if __name__ == "__main__":
    #python compare_skeleton_to_markers.py Dan_first_mocap.vsk "WalkingUpSteps01.csv"
    main()
