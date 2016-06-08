import numpy as np
from vicon_anim_parser.src.character import Joint, JointHinge, \
JointBall, JointFree, JointUniversal, Transform

def create_joint(xml_el, current_id, parent_id):
    joint, joint_el = _create_specific_joint(xml_el, current_id, parent_id)
    _build_common_all(joint, joint_el)
    return joint


def _create_specific_joint(xml_el, current_id, parent_id):
    joint_tags = {
        "JointFree": (JointFree, None),
        "JointBall": (JointBall, None),
        "JointHinge": (JointHinge, "AXIS"),
        "JointHardySpicer": (JointUniversal, "AXIS-PAIR"),
        "JointDummy": (Joint, None)
    }

    def is_found(joint_element):
        return joint_element is not None

    def parse_joint(tag_name, joint_element):
        joint_constructor, attr_name = joint_tags[tag_name]
        joint = joint_constructor(current_id, parent_id)

        if attr_name is not None:
            params = joint_element.get(attr_name).strip().split()
            joint.store_params(*map(float, params))

        return  joint

    joint_element = None
    joint = None

    for tag_name in joint_tags:
        joint_element = xml_el.find(tag_name)
        if is_found(joint_element):
            joint = parse_joint(tag_name, joint_element)
            break

    if joint is None:
        raise Exception("joint {0} of segment {1} has unknown type".format(current_id, xml_el.get("NAME")))

    return joint, joint_element

def _build_common_all(joint, joint_el):
    transform = Transform()
    translation = joint_el.get("PRE-POSITION").strip().split()
    translation = np.array(map(float, translation))
    transform.translation = translation

    angles = joint_el.get("PRE-ORIENTATION").strip().split()
    x, y, z = np.array(map(float, angles))
    transform.rotation = Transform.from_euler_rad(x, y, z)

    joint.transform = transform
    joint.name = joint_el.get("NAME")