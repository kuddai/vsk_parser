import sys

import numpy as np
from vicon_anim_parser.scene_drawer import draw_scene, show_skeleton_structure
from vicon_anim_parser.vsk_parser import parse_skeleton_structure
from vicon_anim_parser.vicon_stream_parser import parse_vicon_stream
from vicon_anim_parser.character import Transform, Skeleton


def main():
    vsk_file_name = sys.argv[1]
    vicon_stream_name = sys.argv[2]

    print vsk_file_name, vicon_stream_name

    skeleton_original = parse_skeleton_structure(vsk_file_name)
    skeletons = []
    raw_anim, frame_rate_hz = parse_vicon_stream(vicon_stream_name)
    frame_ids = sorted(list(raw_anim.keys()))
    counter = 0

    for frame_id in frame_ids:
        pose = raw_anim[frame_id]
        skeleton = skeleton_original.clone()
        for segment in pose:
            name, dofs = segment
            joint = skeleton.get_joint_by_segment_name(name)
            rx, ry, rz = dofs[:3]
            loc_rot = Transform.from_euler_rad(rx, ry, rz)
            joint.transform.rotation = loc_rot

            if joint.is_root():
                loc_trans = dofs[3:]
                joint.transform.translation = np.array(loc_trans)

        skeleton.update_global_transforms()
        skeletons.append(skeleton)

        if counter % 500 == 0:
            print counter, "poses finished"

        counter += 1

    print "hi"

    draw_scene(skeletons, FPS=60)
    #show_skeleton_structure(skeletons[1])

if __name__ == "__main__":
    #python show_vicon_stream.py Dan_first_mocap.vsk LocalRotations.txt
    main()
