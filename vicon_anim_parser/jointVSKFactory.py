import numpy as np
from vicon_anim_parser.character import Joint, JointHinge, \
JointBall, JointFree, JointUniversal, Transform

def create_joint(xml_el, current_id, parent_id):
    joint, joint_el = _create_specific_joint(xml_el, current_id, parent_id)
    _build_common_all(joint, joint_el)
    _build_segment_name(joint, xml_el)
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
    """
    from here:
    https://github.com/jslee02/vsk/tree/master/docs

    The orientation is specified as a helical vector. The
    direction of this vector gives the direction of the axis.
    The magnitude of this vector gives the amount of
    rotation around that axis in radians.
    """

    transform = Transform()
    translation = joint_el.get("PRE-POSITION").strip().split()
    translation = np.array(map(float, translation))
    transform.translation = translation

    #epxonential mapping -> axis-angle pair
    angles = joint_el.get("PRE-ORIENTATION").strip().split()

    axis = np.array(map(float, angles))
    magnitude = np.linalg.norm(axis)
    if abs(magnitude) < 0.0001:
        #magnitude = angle is too small -> rotation is just identity matrix
        transform.rotation = np.eye(3)
    else:
        axis = axis / magnitude
        transform.rotation = Transform.rotate_around_rad(axis, magnitude)

    joint.transform = transform
    joint.name = joint_el.get("NAME")

def _build_segment_name(joint, xml_el):
    joint.segment_name = xml_el.get("NAME").strip()