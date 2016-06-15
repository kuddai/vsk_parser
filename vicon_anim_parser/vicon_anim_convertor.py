import sys

from vicon_anim_parser.scene_drawer import show_skeleton_structure
from vicon_anim_parser.csv_anim_parser import parse_skeleton_animations
from vicon_anim_parser.vsk_parser import parse_skeleton_structure
from transforms3d.euler import mat2euler

def write_bvh(skeleton_original, skeleton_animation, f):
    rest = skeleton_original
    successors = rest.get_joint_id2children()
    joints = rest.joints

    joints_visit_order = []

    #recursion because we have to put closing bracket }
    #for each joint -> it is easier to do with recursion.
    #overwise has to add visited array

    def record_joint_bvh(jid, shift):
        joint = joints[jid]
        is_root = jid == 0
        has_children = len(successors[jid]) > 0
        is_end_site = not has_children

        tab =  "\t" * shift
        tab2 = "\t" * (shift + 1)

        if not is_end_site:
            joints_visit_order.append(jid)

        if is_root:
            header = "%sROOT %s\n" % (tab, joint.name)
        elif has_children:
            header = "%sJOINT %s\n" % (tab, joint.name)
        else:
            header = "%sEnd Site\n" % tab

        if is_root:
            offset = [0.0, 0.0, 0.0]
        else:
            offset = joint.transform.translation

        if is_root:
            channels = "CHANNELS 6 Xposition Yposition Zposition Zrotation Xrotation Yrotation"
        elif has_children:
            channels = "CHANNELS 3 Zrotation Xrotation Yrotation"
        else:
            channels = None

        f.write(header)
        f.write("%s{\n" % tab)

        f.write("%sOFFSET\t %s\n" % (tab2, "\t ".join(map(str, offset))))

        if channels is not None:
            f.write("%s%s\n" % (tab2, channels))

        for cid in successors[jid]:
            record_joint_bvh(cid, shift + 1)

        f.write("%s}\n" % tab)

    #starting from root
    root_id = 0
    shift = 0

    f.write("HIERARCHY\n")
    record_joint_bvh(root_id, shift)
    f.write("MOTION\n")
    f.write("Frames:   %d\n" % len(skeleton_animation))
    f.write("Frame Time: 0.033333\n")

    from math import degrees

    for skeleton in skeleton_animation:
        joints = skeleton.joints
        for jid in joints_visit_order:
            joint = joints[jid]
            angles_rad = mat2euler(joint.transform.rotation, axes='rzxy')
            angles = map(degrees, angles_rad)

            if joint.is_root():
                print "\t ".join(map(str, joint.transform.translation))
                f.write("\t ".join(map(str, joint.transform.translation)))
                f.write("\t ")
            f.write("\t ".join(map(str, angles)))
            f.write("\t ")
        f.write("\n")


def gen_skeleton_anims(skeleton_original, csv_file_name, beg_frame, end_frame):
    from copy import deepcopy

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
        yield skeleton


def main():
    vsk_file_name = sys.argv[1]
    csv_file_name = sys.argv[2]

    print vsk_file_name, csv_file_name

    from copy import deepcopy
    skeleton_original = parse_skeleton_structure(vsk_file_name)

    skeleton_anim = list(gen_skeleton_anims(skeleton_original, csv_file_name, 600, 1200))


    with open("hierarchy_bvh_test.bvh", "w") as f:
        write_bvh(skeleton_original, skeleton_anim, f)





if __name__ == "__main__":
    # command
    # python vicon_anim_parser/vicon_anim_convertor.py Ruslan.vsk "Ruslan Cal 03.csv"
    main()