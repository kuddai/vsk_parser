import sys

from vicon_anim_parser.src.skeleton_drawer import show_markers_anim
from vicon_anim_parser.src.csv_anim_parser import parse_markers

def main():
    csv_file_name = sys.argv[1]
    print csv_file_name

    def animation_gen():
        #skeletons = []
        for frame_id, markers in enumerate(parse_markers(csv_file_name)):
            if frame_id + 1 < 500:
                continue
            print "finished frame", frame_id + 1
            yield markers

    show_markers_anim(animation_gen())


if __name__ == "__main__":
    # python vicon_anim_parser/src/csv_markers_shower.py "Ruslan Cal 03.csv"
    main()