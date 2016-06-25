import sys
import matplotlib.pyplot as plt
import numpy as np

"""
mouse data record:
position_horizontal, position_vertical, velocity_horizontal, velocity_vertical, timestamp
"""

MPX = 0 #MOUSE POSITION X
MPY = 1 #MOUSE POSITION Y
MVX = 2 #MOUSE VELOCITY X
MVY = 3 #MOUSE VELOCITY Y
MTS = 4 #TimeStamp in seconds

def plot_horizontal_data(mouse_data, line_color="r", marker_color="g", linewidth=4.0, title=""):
    xx = [r[MPX] for r in mouse_data]
    vx = [r[MVX] for r in mouse_data]

    fig = plt.figure()
    fig.suptitle(title)
    ax = fig.add_subplot(111)

    ax.grid(True, which='both')
    ax.axhline(y=0, color='k')
    ax.axvline(x=0, color='k')

    ax.plot(xx, vx, "-", c=line_color, linewidth=linewidth)
    ax.plot(xx, vx, "o", c=marker_color)

    ax.set_xlabel("Position X")
    ax.set_ylabel("Velocity X")

    plt.show()

def compare_mouse_curves(curve1_data, curve2_data, curve1_name="curve 1", curve2_name="curve 2"):
    color1 = "r"
    color2 = "b"
    linewidth = 2.0
    markersize = 4

    xx1 = [r[MPX] for r in curve1_data]
    vx1 = [r[MVX] for r in curve1_data]

    xx2 = [r[MPX] for r in curve2_data]
    vx2 = [r[MVX] for r in curve2_data]

    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.grid(True, which='both')
    ax.axhline(y=0, color='k')
    ax.axvline(x=0, color='k')

    curve1, = ax.plot(xx1, vx1, "-o", c=color1, linewidth=linewidth, markersize=markersize, label=curve1_name)
    curve2, = ax.plot(xx2, vx2, "-*", c=color2, linewidth=linewidth, markersize=markersize, label=curve2_name)

    ax.set_xlabel("Position X")
    ax.set_ylabel("Velocity X")

    plt.legend(handles=[curve1, curve2])
    plt.show()


def parse_mouse_data(mouseDataFileName):
    mouseData = []
    with open(mouseDataFileName) as f:
        # skip header
        f.readline()
        for line in f:
            try:
                mouseData.append(map(float, line.split(",")))
            except:
                print line
                raise ValueError("problem on " + line)
    return mouseData

def get_segment_anim_data(vsk_file_name, csv_file_name):
    from vicon_anim_parser.vsk_parser import parse_child2parent
    from vicon_anim_parser.csv_anim_parser import parse_segments_names, remove_subjects_names, parse_segments

    header = parse_segments_names(csv_file_name)
    header = remove_subjects_names(header)
    # remove sword segment
    # header = header[:-1]

    child2parent = parse_child2parent(vsk_file_name)

    segment_name2segment_id = {segment_name: segment_id for segment_id, segment_name in enumerate(header)}

    segment_id2parent_id = [None] * len(header)
    for segment_id in xrange(len(header)):
        segment_name = header[segment_id]
        parent_name = child2parent[segment_name]
        parent_id = -1 if parent_name is None else segment_name2segment_id[parent_name]
        segment_id2parent_id[segment_id] = parent_id

    anim_data = list(parse_segments(csv_file_name))

    return segment_id2parent_id, header, anim_data

def convert_anim_for_learning(anim):
    converted = []
    for pose in anim:
        xx, yy, zz = pose
        pose_vector = xx + yy + zz
        converted.append(pose_vector)
    converted = np.array(converted)
    converted = converted.astype('float32')
    return converted

def convert_pose_row_to_markers(pose_vector):
    length = len(pose_vector)
    assert length % 3 == 0, "pose row is wrong, can divide equally one 3 parts. length %s" % length

    coord_length = length / 3
    xx = pose_vector[0 :   coord_length]
    yy = pose_vector[coord_length : 2 * coord_length]
    zz = pose_vector[2 * coord_length : 3 * coord_length]

    return xx, yy, zz

def convert_anim_data_to_interp_knots(anim_data):
    length = len(anim_data)
    return [float(i) / length for i in xrange(length)]

def interp_mouse_data(interp_knots, mouse_curve):
    import numpy as np
    time_beg = mouse_curve[0][MTS]
    time_end = mouse_curve[-1][MTS]
    time_interval = time_end - time_beg

    tt = map(lambda r: (r[MTS] - time_beg) / time_interval, mouse_curve)
    xx = map(lambda r: r[MPX], mouse_curve)
    yy = map(lambda r: r[MPY], mouse_curve)
    vx = map(lambda r: r[MVX], mouse_curve)
    vy = map(lambda r: r[MVY], mouse_curve)

    xx_new = np.interp(interp_knots, tt, xx)
    yy_new = np.interp(interp_knots, tt, yy)
    vx_new = np.interp(interp_knots, tt, vx)
    vy_new = np.interp(interp_knots, tt, vy)

    return xx_new, yy_new, vx_new, vy_new

def couple_data(anim_data, mouse_curve):
    interp_knots = convert_anim_data_to_interp_knots(anim_data)
    return interp_mouse_data(interp_knots, mouse_curve)

def plot_styled(xx, fxx, label_x="argumnet", label_fx="function", title=""):
    line_color = "r"
    marker_color = "g"
    linewidth = 4.0

    fig = plt.figure()
    fig.suptitle(title)
    ax = fig.add_subplot(111)

    ax.grid(True, which='both')
    ax.axhline(y=0, color='k')
    ax.axvline(x=0, color='k')

    ax.plot(xx, fxx, "-", c=line_color, linewidth=linewidth)
    ax.plot(xx, fxx, "o", c=marker_color)

    ax.set_xlabel(label_x)
    ax.set_ylabel(label_fx)

    plt.show()

def save_coupled_horizontal_data(name, mouse_curve, anim_data):
    xx, yy, vx, vy = couple_data(anim_data, mouse_curve)
    mouse_input = np.array(zip(xx, vx)).astype('float32')
    anim_output = convert_anim_for_learning(anim_data)

    print name, "input  shape", mouse_input.shape
    print name, "output shape", anim_output.shape

    np.savez(".\\Learning\\data_horizontal\\" + name, mouse_input, anim_output)
    return mouse_input, anim_output

def show_coupled_horizontal_data(anim_data, segment_id2parent_id, mouse_curve):
    from vicon_anim_parser.scene_drawer import get_segments_anim
    xx, yy, vx, vy = couple_data(anim_data, mouse_curve)
    return get_segments_anim(anim_data,
                             segment_id2parent_id,
                             scene_length=800,
                             initial_frame=-1,
                             mouse_curve=zip(xx, vx),
                             view_angle_horiz = 180,
                             hide_axes=True)




