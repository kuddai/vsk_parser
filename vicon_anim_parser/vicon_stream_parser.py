import sys

def parse_vicon_stream(file_name):
    from collections import defaultdict
    raw_anim = defaultdict(list)

    with open(file_name) as f:
        num_anims = int(f.readline())
        frame_rate_hz = float(f.readline())
        print "number of frames in the file", num_anims

        for line in f.xreadlines():
            line = line.strip()
            terms = line.split(",")
            frame_id = int(terms[0])
            segment_name = terms[1].strip()
            dofs = map(float,terms[2:])
            raw_joint = (segment_name, dofs)
            raw_anim[frame_id].append(raw_joint)

        return raw_anim, frame_rate_hz


if __name__ == "__main__":
    file_name = sys.argv[1]
    raw_anim = parse_vicon_stream(file_name)
    print "animation length", len(raw_anim)