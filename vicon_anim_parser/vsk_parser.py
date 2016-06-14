import sys
import xml.etree.ElementTree as ET
import numpy as np

from vicon_anim_parser.character import Skeleton
from vicon_anim_parser.skeleton_drawer import show_skeleton_structure
from vicon_anim_parser.jointVSKFactory import create_joint

def _parse_skeleton_from_root(skeleton_root_el):
    joints = []

    def available_id():
        return len(joints)

    name2joint_id = {}
    #root has no parents in other words
    parent_id = -1
    stack = [(skeleton_root_el,parent_id)]

    while len(stack) > 0:
        current_id = available_id()
        el, parent_id = stack.pop()
        joint = create_joint(el, current_id, parent_id)
        joints.append(joint)
        name2joint_id[joint.name] = current_id

        stack.extend((child, current_id) for child in el.findall("Segment"))

    return joints, name2joint_id


def parse_skeleton_structure(vsk_file_name):
    tree = ET.parse(vsk_file_name)
    root = tree.getroot()
    skeleton_el = root.find("Skeleton")
    skeleton_root_el = skeleton_el.find("Segment")
    joints, name2joint_id = _parse_skeleton_from_root(skeleton_root_el)
    return Skeleton(joints, name2joint_id)


def main():
    vsk_file_name = sys.argv[1]
    skeleton = parse_skeleton_structure(vsk_file_name)
    skeleton.move_to_origin()

    #moving hand
    # left_arm = skeleton.get_joint_by_name("LeftArm_LeftForeArm")
    # left_arm.move(45, 45)


    # #moving leg
    # left_leg = skeleton.get_joint_by_name("Hips_LeftUpLeg")
    # left_leg.move(0, 0, 90)

    # #hips root
    # root = skeleton.get_joint_by_name("World_Hips")
    # root.move(-91.56, -0.59, 173.5, 0, 0, 0) #-91.5623,-0.594814,173.508

    #problem shoulder on frame 2453
    # left_shoulder = skeleton.get_joint_by_name("LeftShoulder_LeftArm")
    # left_shoulder.move(146.154,	51.1199, 118.597)

    skeleton.update_global_m4x4()
    #just checking whether skeleton was parsed correctly or not

    show_skeleton_structure(skeleton, show_joint_names=False)

if __name__ == "__main__":
    # python vicon_anim_parser/src/vsk_parser.py Ruslan.vsk
    main()