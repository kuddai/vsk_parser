import sys

import numpy as np
from math import radians, degrees
from transforms3d import euler
from vicon_anim_parser.src.character import Transform, JointFree
from vicon_anim_parser.src.csv_anim_parser import parse_animations, parse_markers


def gen_sword_anims(csv_file_name):
    num_empty_frames = 0
    for i, raw_anim in enumerate(parse_animations(csv_file_name)):
        frame_id = i + 1
        try:
            coords = map(float, raw_anim["World_SwordSegment"])
            if frame_id == 1:
                first_coords = coords
            joint = JointFree(0, -1)
            joint.move(*coords)
            yield joint

        except ValueError:
            num_empty_frames += 1
            print "frame", frame_id, "is empty", raw_anim["World_SwordSegment"]
            #yiled None to preserve frame order
            yield None

    print "number of empty frames", num_empty_frames

def draw_sword(sword_joints, markers_anim, beg_frame=1, end_frame=None, FPS=30):
    import matplotlib.pyplot as plt
    #this import is necessary for plt.figure().gca(projection='3d') line
    #without it there will be exception here:
    from mpl_toolkits.mplot3d import Axes3D
    import matplotlib.animation as animation

    if end_frame is None:
        end_frame = len(sword_joints)

    fig = plt.figure()
    ax = fig.gca(projection='3d')

    num_frames = end_frame - beg_frame + 1
    #marker points points
    sword_pts,   = ax.plot([], [], [], '-o', c="r", markersize=9)
    markers_pts,  = ax.plot([], [], [], '.', c="b", markersize=7)


    #text_box = ax.text(0.02, 0.95, '', transform=ax.transAxes)


    def init():
        sword_pts.set_data([], [])
        sword_pts.set_3d_properties([])

        markers_pts.set_data([], [])
        markers_pts.set_3d_properties([])

        #text_box.set_text("")

        return sword_pts, markers_pts #, text_box

    SWORD_LENGTH = 300

    def animate(i):
        frame_id = beg_frame + i
        #due to first element being 0
        el_id = frame_id - 1
        sword_joint, markers = sword_joints[el_id], markers_anim[el_id]
        if sword_joint is not None:
            x0, y0, z0 = sword_joint.transform.translation

            sword_pts.set_data(x0, y0)
            sword_pts.set_3d_properties(z0)

        xx, yy, zz = markers
        markers_pts.set_data(xx, yy)
        markers_pts.set_3d_properties(zz)

        #text_box.set_text(frame_id)
        fig.suptitle("frame_id %r" % frame_id)

        return sword_pts, markers_pts#, text_box

    ax.set_xlim3d(-2000, 2000)
    ax.set_ylim3d(-2000, 2000)
    ax.set_zlim3d(-2000, 2000)

    interval = 1000/FPS
    #blit=False is necessary for Mac OS X (exception otherwise)
    #We need to keep these reference as well, otherwise it would be picked up by GB
    anim = animation.FuncAnimation(fig, animate, frames=num_frames, interval=interval, init_func=init, blit=False, repeat=False)

    plt.xlabel('x')
    plt.ylabel('y')
    plt.show()

def main():
    vsk_file_name = sys.argv[1]
    csv_file_name = sys.argv[2]

    print vsk_file_name, csv_file_name
    #skeleton_original = parse_skeleton_structure(vsk_file_name)

    beg_frame = 600
    end_frame = 900

    sword_joints = list(gen_sword_anims(csv_file_name))
    markers_anim = list(parse_markers(csv_file_name))
    print len(sword_joints)
    print sword_joints[0].transform
    draw_sword(sword_joints, markers_anim, beg_frame, end_frame)


if __name__ == "__main__":
    #python vicon_anim_parser/compare_sword_to_markers.py Ruslan.vsk "Ruslan Cal 03.csv"
    main()
