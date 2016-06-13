import sys

import numpy as np
from math import radians, degrees
from transforms3d import euler
from vicon_anim_parser.src.character import Transform, JointFree
from vicon_anim_parser.src.skeleton_drawer import show_skeleton_structure, show_skeleton_anim, scale_equally_markers
from vicon_anim_parser.src.csv_anim_parser import parse_animations, parse_markers
from vicon_anim_parser.src.vsk_parser import parse_skeleton_structure

def gen_skeleton_anims(vsk_file_name, csv_file_name, beg_frame, end_frame):
    from copy import deepcopy
    print "vsk parsed"
    skeleton_original = parse_skeleton_structure(vsk_file_name)

    for i, raw_animation in enumerate(parse_animations(csv_file_name)):
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



        skeleton.update_global_transform()
        yield skeleton


#data -> tuples of skeleton and markers for each frame
def draw_skeleton_and_markers(data, beg_frame=1, FPS=1):
    from vicon_anim_parser.src.skeleton_drawer import SkeletonDrawer
    import matplotlib.pyplot as plt
    #this import is necessary for plt.figure().gca(projection='3d') line
    #without it there will be exception here:
    from mpl_toolkits.mplot3d import Axes3D
    import matplotlib.animation as animation

    fig = plt.figure()
    ax = fig.gca(projection='3d')

    num_lines  = data[0][0].get_num_joints() - 1
    #marker points points

    skeleton_lines = sum([ax.plot([], [], [], '-', c="r", linewidth=4.0)  for i in xrange(num_lines)], [])
    markers_pts,   = ax.plot([], [], [], 'o', c="g", markersize=7)

    skeletonDrawer = SkeletonDrawer(ax, skeleton_lines)

    def init():
        for line in skeleton_lines:
            line.set_data([], [])
            line.set_3d_properties([])

        markers_pts.set_data([], [])
        markers_pts.set_3d_properties([])

        return skeleton_lines, markers_pts

    def animate(i):
        frame_id = beg_frame + i
        #due to first element being 0
        skeleton, markers = data[i]

        result = skeletonDrawer.animate(skeleton)

        xx, yy, zz = markers
        markers_pts.set_data(xx, yy)
        markers_pts.set_3d_properties(zz)

        #text_box.set_text(frame_id)
        fig.suptitle("frame_id %r" % frame_id)

        result += (markers_pts,)
        return result

    ax.set_xlim3d(-2000, 2000)
    ax.set_ylim3d(-2000, 2000)
    ax.set_zlim3d(-2000, 2000)

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

    beg_frame = 885
    end_frame = 1003

    skeletons = list(gen_skeleton_anims(vsk_file_name, csv_file_name, beg_frame, end_frame))
    print "skeletons parsed", len(skeletons)
    markers_anim = list(parse_markers(csv_file_name))[beg_frame - 1:end_frame]
    print "markers parsed", len(markers_anim)


    draw_skeleton_and_markers(zip(skeletons, markers_anim), beg_frame)


if __name__ == "__main__":
    #python vicon_anim_parser/compare_skeleton_to_markers.py Ruslan.vsk "Ruslan Cal 03.csv"
    main()
