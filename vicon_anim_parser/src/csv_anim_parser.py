import sys

#Trajectories 14930

def skip_lines(f, num_lines):
    for _ in xrange(num_lines):
        a = next(f)

def read_till_joints_keyword(f):
    line = None
    while line != "Joints":
        line = next(f).strip()


def str2int(word):
    """
    preserves empty strings
    """
    return "" if len(word) == 0 else float(word)

def is_new_joint_name(old_name, new_name):
    return len(new_name) > 0 and old_name != new_name


def remove_prefix(name):
    parts = name.split(":")
    return parts[-1]

def parse_anim(joint_names, csv_line_terms):
    raw_skeleton = {}
    params = []
    current_joint_name = ""
    for i, term in enumerate(csv_line_terms):
        new_name = remove_prefix(joint_names[i])
        if is_new_joint_name(current_joint_name, new_name):
            raw_skeleton[current_joint_name] = map(str2int, params)
            params = []
            current_joint_name = new_name

        params.append(term)
    #store last one
    raw_skeleton[current_joint_name] = params
    #delete empty data (it must be frame and subframe information)
    del raw_skeleton[""]
    return raw_skeleton

def parse_animations(csv_file_name, max_anims = float("inf")):
    with open(csv_file_name) as csv:
        #skip first two lines: Joints and unknown number
        read_till_joints_keyword(csv)

        skip_lines(csv, 1)

        joint_names = next(csv).split(",")
        #skip transform types and  deg and mm description lines
        #this line must not be skipped if there are over formats then deg and mm
        skip_lines(csv, 2)

        #first line of actual dats
        line = next(csv)
        terms = line.split(",")

        #yield raw skeleton
        #return parse_anim(joint_names, terms)
        n = 0
        while line != "" and line != "Trajectories" and n < max_anims:
            terms = line.split(",")

            #yield raw skeleton
            yield parse_anim(joint_names, terms)
            line = next(csv)
            n += 1


if __name__ == "__main__":
    result = next(parse_animations(sys.argv[1]))
    print result



