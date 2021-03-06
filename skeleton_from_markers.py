import sys

import numpy as np
from math import radians, degrees
from vicon_anim_parser.scene_drawer import draw_scene, show_skeleton_structure
from vicon_anim_parser.csv_anim_parser import parse_skeleton_animations, parse_markers, parse_segments_fully
from vicon_anim_parser.vsk_parser import parse_skeleton_structure
from vicon_anim_parser.character import Transform, Joint

def gen_skeleton_anims(vsk_file_name, csv_file_name, beg_frame, end_frame):
    from copy import deepcopy

    skeleton_original = parse_skeleton_structure(vsk_file_name)

    np.set_printoptions(suppress=True, precision=4)

    for i, raw_animation in enumerate(parse_segments_fully(csv_file_name)):
        frame_id = i + 1

        if frame_id < beg_frame:
            continue
        if frame_id > end_frame:
            break

        skeleton = deepcopy(skeleton_original)
        for joint_name in skeleton.get_joints_names():
            joint = skeleton.get_joint_by_name(joint_name)
            parent_name, name = joint_name.split('_', 1)

            current_anlges = raw_animation[name][:3]
            #transform global -> current
            Rgc = Transform.from_euler(*current_anlges)

            if parent_name == "World":
                #print Rgc
                rxryrz_xyz = raw_animation[name]
                #joint.move(*rxryrz_xyz)
                continue

            parent_angles = raw_animation[parent_name][:3]
            #transform global -> parent
            Rgp = Transform.from_euler(*parent_angles)

            R = np.dot(Rgc, Rgp.T)

            # if name == "Spine":
            #     print R

            joint.transform.rotation = np.dot(joint.transform.rotation, R)

        skeleton.update_global_transforms()

        # rsh = skeleton.get_joint_by_name("LeftShoulder_LeftArm")
        #print "frame id", frame_id
        # print raw_animation["LeftShoulder_LeftArm"]
        # print rsh.transform.m4x4
        #
        # print skeleton.global_transforms[rsh.current_id]

        # print frame_id
        # print skeleton.get_global_m4x4_by_name("Hips_Spine")
        yield skeleton

    print "vsk parsed"

def main():
    vsk_file_name = sys.argv[1]
    csv_file_name = sys.argv[2]

    print vsk_file_name, csv_file_name

    beg_frame = 1
    end_frame = 500

    skeletons = list(gen_skeleton_anims(vsk_file_name, csv_file_name, beg_frame, end_frame))
    #print "skeletons parsed", len(skeletons)
    #markers_anim = list(parse_markers(csv_file_name))[beg_frame - 1:end_frame]
    #print "markers parsed", len(markers_anim)


    draw_scene(skeletons, initial_frame=beg_frame, FPS=30)
    #show_skeleton_structure(skeletons[1])

if __name__ == "__main__":
    #python compare_skeleton_to_markers.py Dan_first_mocap.vsk "WalkingUpSteps01.csv"
    main()
