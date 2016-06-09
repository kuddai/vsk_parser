import sys

from vicon_anim_parser.src.skeleton_drawer import show_skeleton_structure, show_skeleton_anim
from vicon_anim_parser.src.vsk_parser import parse_skeleton_structure
from vicon_anim_parser.src.csv_anim_parser import parse_animations


def show_joint_negative_values(joint_name, csv_file_name):
    for frame_id, raw_animation in enumerate(parse_animations(csv_file_name)):
        params = raw_animation[joint_name]

        if params[0] < 0:
            output = "frame_id {:6}, param1 {:04}, param2 {:04}".format(frame_id + 1, int(params[0]), int(params[1]))
            print output

def main():
    vsk_file_name = sys.argv[1]
    csv_file_name = sys.argv[2]

    print vsk_file_name, csv_file_name

    from copy import deepcopy
    skeleton_original = parse_skeleton_structure(vsk_file_name)

    def animation_gen():
        #skeletons = []
        for frame_id, raw_animation in enumerate(parse_animations(csv_file_name)):
            if frame_id + 1 < 500:
                continue

            skeleton = deepcopy(skeleton_original)
            for joint_name in skeleton.get_joints_names():
                joint = skeleton.get_joint_by_name(joint_name)
                params = raw_animation[joint_name]
                joint.move(*params)

            #skeleton.move_to_origin()
            skeleton.update_global_transform()
            print "finished frame", frame_id + 1
            yield skeleton
            #skeletons.append(skeleton)

        # print "animations are loaded"
        #
        # for skeleton_id in xrange(500, len(skeletons)):# len(skeletons)):
        #     skeleton = skeletons[skeleton_id]
        #     yield skeleton

    show_skeleton_anim(animation_gen())
    #show_joint_negative_values("LeftArm_LeftForeArm", csv_file_name)


if __name__ == "__main__":
    #python vicon_anim_parser/src/vsk_to_lengths.py Ruslan.vsk "Ruslan Cal 03.csv"
    main()