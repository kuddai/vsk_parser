import sys
import xml.etree.ElementTree as ET
import numpy as np
from vicon_anim_parser.scene_drawer import show_skeleton_structure
from vicon_anim_parser.jointVSKFactory import create_joint
from vicon_anim_parser.character import Skeleton

def parse_skeleton_structure(vsk_file_name):
    tree = ET.parse(vsk_file_name)
    root = tree.getroot()
    skeleton_el = root.find("Skeleton")
    skeleton_root_el = skeleton_el.find("Segment")
    joints, name2joint_id = _parse_skeleton_from_root(skeleton_root_el)
    return Skeleton(joints, name2joint_id)

def parse_child2parent(vsk_file_name):
    """
    child to parent names.
    If child name is not present then return None
    """
    from collections import defaultdict
    child2parent = defaultdict(lambda: None)

    tree = ET.parse(vsk_file_name)
    root = tree.getroot()
    skeleton_el = root.find("Skeleton")
    skeleton_root_el = skeleton_el.find("Segment")
    root_name = skeleton_root_el.get("NAME").strip()
    child2parent[root_name] = None
    stack = [(skeleton_root_el, root_name)]

    while len(stack) > 0:
        parent, parent_name = stack.pop()
        for child in parent.findall("Segment"):
            child_name = child.get("NAME").strip()
            child2parent[child_name] = parent_name
            stack.append((child, child_name))

    return child2parent

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

def main():
    vsk_file_name = sys.argv[1]
    skeleton = parse_skeleton_structure(vsk_file_name)
    skeleton.move_to_origin()
    skeleton.embed_rotations()
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

    skeleton.update_global_transforms()
    #just checking whether skeleton was parsed correctly or not
    show_skeleton_structure(skeleton)

if __name__ == "__main__":
    # python vicon_anim_parser/vsk_parser.py Ruslan.vsk
    main()