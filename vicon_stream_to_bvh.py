import sys

from vicon_anim_parser.scene_drawer import show_skeleton_structure
from vicon_anim_parser.csv_anim_parser import parse_skeleton_animations
from vicon_anim_parser.vsk_parser import parse_skeleton_structure
from transforms3d.euler import mat2euler
from vicon_anim_parser.vicon_anim_convertor import write_bvh
from vicon_anim_parser.vicon_stream_parser import parse_vicon_stream
from vicon_anim_parser.character import Transform, Skeleton
import numpy as np

def main():
    OUTPUT_MSG_FREQ = 500
    from copy import deepcopy
    vsk_file_name = sys.argv[1]
    stream_file_name = sys.argv[2]
    bvh_file_name = sys.argv[3]

    print vsk_file_name, stream_file_name
    skeleton_original = parse_skeleton_structure(vsk_file_name)
    skeleton_TPose = deepcopy(skeleton_original)#skeleton_original.clone()
    skeleton_TPose.embed_rotations()

    raw_anim, frame_rate_HZ = parse_vicon_stream(stream_file_name)
    frame_ids = sorted(list(raw_anim.keys()))
    skeletons = []

    for frame_id in frame_ids:
        pose = raw_anim[frame_id]
        skeleton = skeleton_TPose.clone()

        if frame_id % OUTPUT_MSG_FREQ == 0:
            print frame_id, "frames are done"

        for segment in pose:
            name, dofs = segment
            joint = skeleton.get_joint_by_segment_name(name)
            rx, ry, rz = dofs[:3]
            loc_rot = Transform.from_euler_rad(rx, ry, rz)
            if joint.is_root():
                loc_trans = dofs[3:]
                joint.transform.translation = np.array(loc_trans)

            orig_rot = skeleton_original.get_joint_by_segment_name(name).transform.rotation
            if joint.is_root():
                prev_rot = np.eye(3)
            else:
                prev_rot = skeleton_original.global_transforms[joint.parent_id].rotation
            comp_rot = np.dot(prev_rot, orig_rot).T
            joint.transform.rotation = np.dot(prev_rot, np.dot(loc_rot, comp_rot))

        #no need for global update as we won't draw animation here
        skeleton.rescale_joints(1/10.0)
        skeleton.swap_Y_Z_axes()
        skeletons.append(skeleton)

        if len(skeletons) % 500 == 0:
            print len(skeletons), "poses finished"

    skeleton_TPose.rescale_joints(1/10.0)
    skeleton_TPose.swap_Y_Z_axes()

    with open(bvh_file_name, "w") as f:
        write_bvh(skeleton_TPose, skeletons, f)


if __name__ == "__main__":
    # command
    # python vicon_stream_to_bvh.py Dan_first_mocap.vsk WalkingUpSteps02_raw.txt Dan_walking_up_02.bvh
    main()