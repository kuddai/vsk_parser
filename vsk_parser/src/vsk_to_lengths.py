import sys
import xml.etree.ElementTree as ET

from vsk_parser.src.character import Joint, JointHinge, Transform, Skeleton
from vsk_parser.src.skeleton_drawer import render_skeleton
from vsk_parser.src.jointVSKFactory import create_joint

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
        joint = create_joint(el, current_id, parent_id)
        joints.append(joint)
        name2joint_id[joint.name] = current_id

        stack.extend((child, current_id) for child in el.findall("Segment"))

    return joints, name2joint_id


def main(xml_name):
    tree = ET.parse(xml_name)
    root = tree.getroot()
    skeleton_el = root.find("Skeleton")
    skeleton_root_el = skeleton_el.find("Segment")
    joints, name2joint_id = parse_skeleton(skeleton_root_el)

    leg = joints[name2joint_id["LeftUpLeg_LeftLeg"]]
    leg.move(45)

    hand = joints[name2joint_id["RightArm_RightForeArm"]]
    hand.move(90, 90)

    skeleton = Skeleton(joints)
    render_skeleton(skeleton, display_names=True)



    # for name, joint_id in name2joint_id.items():
    #   print name
    #   print joints[joint_id].transform, "\n"
    #print_skeleton_lengths(skeleton_root_el)

if __name__ == "__main__":
    main(sys.argv[1])