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
    max_length = get_max_length(skeleton)
    ax.set_xlim3d(-max_length, max_length)
    ax.set_ylim3d(-max_length, max_length)
    ax.set_zlim3d(-max_length, max_length)

def render_skeleton(skeleton, display_names = False):
    def traverse_bones():
        glob_trans = skeleton.global_transforms
        for joint in skeleton.joints:
            if joint.is_root():
                continue

            joint_beg_id = joint.current_id
            joint_end_id = joint.parent_id

            joint_beg = glob_trans[joint_beg_id].translation
            joint_end = glob_trans[joint_end_id].translation

            yield joint_beg, joint_end, joint.name

    def draw_skeleton(ax):
        print "draw begin"
        for joint_beg, joint_end, name in traverse_bones():
            x, y, z = joint_beg
            line = zip(joint_beg, joint_end)

            #here inverse because y and z axis are inversed
            ax.plot(line[0], line[2], line[1], color="b")
            ax.scatter(x, z, y, color="r", marker=".")
            if display_names:
                ax.text(x, z, y, name, size=10, zorder=1, color='k')
        print "draw end"

    fig = plt.figure()
    ax = fig.gca(projection='3d')

    scale_equally(ax, skeleton)
    draw_skeleton(ax)

    plt.xlabel('x')
    plt.ylabel('z')
    plt.show()


def render_skeleton_anim(animations, original_skeleton, display_names = False):
    fig = plt.figure()
    ax = fig.gca(projection='3d')


    def get_max_length(skeleton):
        trans = skeleton.global_transforms
        max_length = max(abs(el) for trn in trans for el in trn.translation)
        return max_length

    def scale_equally(skeleton):
        max_length = get_max_length(skeleton)
        ax.set_xlim3d(-max_length, max_length)
        ax.set_ylim3d(-max_length, max_length)
        ax.set_zlim3d(-max_length, max_length)

    def traverse_bones(skeleton):
        glob_trans = skeleton.global_transforms
        for joint in skeleton.joints:
            if joint.is_root():
                continue

            joint_beg_id = joint.current_id
            joint_end_id = joint.parent_id

            joint_beg = glob_trans[joint_beg_id].translation
            joint_end = glob_trans[joint_end_id].translation

            yield joint_beg, joint_end, joint.name



    def draw_skeleton(skeleton):

        # if draw_skeleton.drawn :
        #     print "already drawn something"
        #     return

        print "skeleton beee", skeleton
        #plt.clf()
        #fig.clear()
        for joint_beg, joint_end, name in traverse_bones(skeleton):
            x, y, z = joint_beg
            line = zip(joint_beg, joint_end)

            #here inverse because y and z axis are inversed
            ax.plot(line[0], line[2], line[1], color="b")
            ax.scatter(x, z, y, color="r", marker=".")
            if display_names:
                ax.text(x, z, y, name, size=10, zorder=1, color='k')
        #ax.figure.canvas.draw()
        fig.canvas.draw()
        #plt.draw()
        draw_skeleton.drawn  = True
        print "skeleton end"

    draw_skeleton.drawn = False


    print "hi"
    scale_equally(original_skeleton)
    #anim = animation.FuncAnimation(fig, draw_skeleton, animations, repeat=False, interval=100, blit=False)
    anim = animation.FuncAnimation(fig, draw_skeleton, animations, repeat=False)

    plt.xlabel('x')
    plt.ylabel('z')
    plt.show()


def render_skeleton_anim2(animations, original_skeleton, display_names = False):
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    #all joints except root
    num_lines =  original_skeleton.get_num_joints() - 1
    #bones lines
    lines = sum([ax.plot([], [], [], c="b")  for i in xrange(num_lines)], [])
    #joint points
    pts   = sum([ax.plot([], [], [], 'o', c="r")  for i in xrange(num_lines)], [])

    def init():
        for line, pt, note in zip(lines, pts):
            line.set_data([], [])
            line.set_3d_properties([])

            pt.set_data([], [])
            pt.set_3d_properties([])
            note.set_text("")

        return lines, pts

    def animate(skeleton):
        #skeleton = next(animations)
        glob_trans = skeleton.global_transforms

        for line, pt, note, joint in zip(lines, pts, skeleton.joints[1:]):
            joint_beg_id = joint.current_id
            joint_end_id = joint.parent_id

            joint_beg = glob_trans[joint_beg_id].translation
            joint_end = glob_trans[joint_end_id].translation

            data = zip(joint_beg, joint_end)
            line.set_data(data[0], data[2])
            line.set_3d_properties(data[1])

            pt.set_data(data[0], data[2])
            pt.set_3d_properties(data[1])

        return lines, pts

    scale_equally(ax, original_skeleton)
    #anim = animation.FuncAnimation(fig, draw_skeleton, animations, repeat=False, interval=100, blit=False)
    anim = animation.FuncAnimation(fig, animate, animations, init_func=init, blit=False, repeat=False)

    plt.xlabel('x')
    plt.ylabel('z')
    plt.show()