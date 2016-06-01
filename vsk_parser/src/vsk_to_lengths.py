import sys
import xml.etree.ElementTree as ET

from vsk_parser.src.character import Joint, Transform, Skeleton
from vsk_parser.src.skeleton_drawer import render_skeleton


def extract_joint(element, current_id, parent_id):
    import numpy as np
    joint = Joint(current_id, parent_id)
    transform = Transform()
    joint_el = element[0]

    translation = joint_el.get("PRE-POSITION").strip().split()
    translation = np.array(map(float, translation))
    transform.translation = translation

    angles = joint_el.get("PRE-ORIENTATION").strip().split()
    x, y, z = np.array(map(float, angles))
    transform.rotation = Transform.from_euler_rad(x, y, z)

    joint.transform = transform
    joint.name = joint_el.get("NAME")

    return joint


def parse_skeleton(skeleton_root_el):
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

        joint = extract_joint(el, current_id, parent_id)
        joints.append(joint)
        name2joint_id[joint.name] = current_id

        stack.extend((child, current_id) for child in el.findall("Segment"))

    return joints, name2joint_id


def print_skeleton_lengths(skeleton_root_el):
    count = 0
    for segment in skeleton_root_el.iter("Segment"):
        joint = segment[0]
        count += 1
        print count, joint.get("NAME"), joint.get("PRE-POSITION")

def display_all_joint(joints, name2joint_id):
    for joint_id in xrange(len(joints)):
        joint = joints[joint_id]
        path = [joint.name]
        while not joint.is_root():
            joint = joints[joint.parent_id]
            path.append(joint.name)

        print " -> ".join(path)

def main(xml_name):
    tree = ET.parse(xml_name)
    root = tree.getroot()
    skeleton_el = root.find("Skeleton")
    skeleton_root_el = skeleton_el.find("Segment")
    joints, name2joint_id = parse_skeleton(skeleton_root_el)

    skeleton = Skeleton(joints)
    render_skeleton(skeleton)

    # for name, joint_id in name2joint_id.items():
    #   print name
    #   print joints[joint_id].transform, "\n"
    #print_skeleton_lengths(skeleton_root_el)

if __name__ == "__main__":
    main(sys.argv[1])