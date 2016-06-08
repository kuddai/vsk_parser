import sys

from vicon_anim_parser.src.skeleton_drawer import show_skeleton_structure, show_skeleton_anim
from vicon_anim_parser.src.vsk_parser import parse_skeleton_structure
from vicon_anim_parser.src.csv_anim_parser import parse_animations




def main():
    vsk_file_name = sys.argv[1]
    csv_file_name = sys.argv[2]

    print vsk_file_name, csv_file_name

    from copy import deepcopy
    skeleton_original = parse_skeleton_structure(vsk_file_name)

    # raw_animation = parse_animations(csv_file_name)
    # skeleton = deepcopy(skeleton_original)
    #
    #
    # for joint_name in skeleton.get_joints_names():
    #     joint = skeleton.get_joint_by_name(joint_name)
    #     params = raw_animation[joint_name]
    #     joint.move(*params)
    #
    # skeleton.move_to_origin()
    # skeleton.update_global_transform()
    #
    # render_skeleton(skeleton, display_names=True)

    def animation_gen():
        skeletons = []
        for raw_animation in parse_animations(csv_file_name, max_anims=1000):
            skeleton = deepcopy(skeleton_original)
            for joint_name in skeleton.get_joints_names():
                joint = skeleton.get_joint_by_name(joint_name)
                params = raw_animation[joint_name]
                joint.move(*params)

            #skeleton.move_to_origin()
            skeleton.update_global_transform()
            # yield skeleton
            skeletons.append(skeleton)

        print "animations are loaded"

        for skeleton_id in xrange(500, len(skeletons)):# len(skeletons)):
            skeleton = skeletons[skeleton_id]
            yield skeleton

    show_skeleton_anim(animation_gen())

if __name__ == "__main__":
    main()