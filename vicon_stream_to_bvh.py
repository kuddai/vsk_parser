import sys

from vicon_anim_parser.scene_drawer import show_skeleton_structure
from vicon_anim_parser.csv_anim_parser import parse_skeleton_animations
from vicon_anim_parser.vsk_parser import parse_skeleton_structure
from transforms3d.euler import mat2euler
from vicon_anim_parser.vicon_anim_convertor import write_bvh
from vicon_anim_parser.vicon_stream_parser import parse_vicon_stream
from vicon_anim_parser.character import Transform
import numpy as np

def main():
    vsk_file_name = sys.argv[1]
    stream_file_name = sys.argv[2]

    print vsk_file_name, stream_file_name
    skeleton_original = parse_skeleton_structure(vsk_file_name)


    raw_anim, frame_rate_HZ = parse_vicon_stream(stream_file_name)
    frame_ids = sorted(list(raw_anim.keys()))
    skeletons = []

    for frame_id in frame_ids:
        pose = raw_anim[frame_id]
        skeleton = skeleton_original.clone()
        for segment in pose:
            name, dofs = segment
            joint = skeleton.get_joint_by_segment_name(name)
            rx, ry, rz = dofs[:3]
            loc_rot = Transform.from_euler_rad(rx, ry, rz)
            joint.transform.rotation = loc_rot

            loc_trans = dofs[3:]
            joint.transform.translation = np.array(loc_trans)# / 1000.0
            # if joint.is_root():
            #     print "root translation", joint.transform.translation

        #no need for global update as we won't draw animation here
        #skeleton.update_global_transforms()
        skeleton.rescale_joints(1/10.0)
        skeleton.swap_Y_Z_axes()
        skeletons.append(skeleton)

        if len(skeletons) % 500 == 0:
            print len(skeletons), "poses finished"

    skeleton_original.rescale_joints(1/10.0)
    skeleton_original.swap_Y_Z_axes()

    with open("Dan_first_mocap_4.bvh", "w") as f:
        write_bvh(skeleton_original, skeletons, f)


if __name__ == "__main__":
    # command
    # python vicon_anim_parser/vicon_stream_to_bvh.py Dan_first_mocap.vsk WalkingUpSteps01_ViconStream.txt
    main()