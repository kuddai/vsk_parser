import matplotlib.pyplot as plt
#this import is necessary for plt.figure().gca(projection='3d') line
#without it there will be exception here:
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation


def get_max_length(skeleton):
    trans = skeleton.global_transforms
    max_length = max(abs(el) for trn in trans for el in trn.translation)
    return max_length

def scale_equally(ax, skeleton):
    max_length = get_max_length(skeleton)*2
    ax.set_xlim3d(-max_length, max_length)
    ax.set_ylim3d(-max_length, max_length)
    ax.set_zlim3d(-max_length, max_length)

def draw_skeleton(ax, skeleton):
    glob_trans = skeleton.global_transforms
    #all joints except root (it has id 0 so we need range [1:])
    for joint in skeleton.joints[1:]:

        joint_beg_id = joint.current_id
        joint_end_id = joint.parent_id

        joint_beg = glob_trans[joint_beg_id].translation
        joint_end = glob_trans[joint_end_id].translation

        x, y, z = joint_beg
        line = zip(joint_beg, joint_end)

        #here inverse because y and z axis are inversed
        ax.plot(line[0], line[2], line[1], color="b")
        ax.scatter(x, z, y, color="r", marker=".")
        ax.text(x, z, y, joint.name, size=10, zorder=1, color='k')

def show_skeleton_structure(skeleton):
    fig = plt.figure()
    ax = fig.gca(projection='3d')

    scale_equally(ax, skeleton)
    draw_skeleton(ax, skeleton)

    plt.xlabel('x')
    plt.ylabel('z')
    plt.show()

def show_skeleton_anim(animations, FPS=30):
    first_frame_skeleton = next(animations)
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    #all joints except root
    num_lines =  first_frame_skeleton.get_num_joints() - 1
    #bones lines
    lines = sum([ax.plot([], [], [], c="b")  for i in xrange(num_lines)], [])
    #joint points
    pts   = sum([ax.plot([], [], [], 'o', c="r")  for i in xrange(num_lines)], [])

    start_point = first_frame_skeleton.get_root().transform.translation

    def init():
        for line, pt in zip(lines, pts):
            line.set_data([], [])
            line.set_3d_properties([])

            pt.set_data([], [])
            pt.set_3d_properties([])

        return lines, pts

    def animate(skeleton):
        #skeleton = next(animations)
        glob_trans = skeleton.global_transforms

        for line, pt, joint in zip(lines, pts, skeleton.joints[1:]):
            joint_beg_id = joint.current_id
            joint_end_id = joint.parent_id

            #center skeleton
            joint_beg = glob_trans[joint_beg_id].translation - start_point
            joint_end = glob_trans[joint_end_id].translation - start_point

            data = zip(joint_beg, joint_end)
            #flip 1 and 2 to change y and z axis as in our data y is vertical one
            line.set_data(data[0], data[2])
            line.set_3d_properties(data[1])

            pt.set_data(data[0], data[2])
            pt.set_3d_properties(data[1])

        return lines, pts

    scale_equally(ax, first_frame_skeleton)
    interval = 1000/FPS
    #blit=False is necessary for Mac OS X (exception otherwise)
    #We need to keep these reference as well, otherwise it would be picked up by GB
    anim = animation.FuncAnimation(fig, animate, animations, interval=interval, init_func=init, blit=False, repeat=False)

    plt.xlabel('x')
    plt.ylabel('z')
    plt.show()