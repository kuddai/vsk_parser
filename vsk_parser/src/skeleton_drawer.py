import matplotlib.pyplot as plt
#this import is necessary for plt.figure().gca(projection='3d') line
#without it there will be exception
from mpl_toolkits.mplot3d import Axes3D

def render_skeleton(skeleton, display_names = False):
    def get_max_length():
        trans = skeleton.global_transforms
        max_length = max(abs(el) for trn in trans for el in trn.translation)
        return max_length

    def scale_equally(ax):
        max_length = get_max_length()
        ax.set_xlim3d(-max_length, max_length)
        ax.set_ylim3d(-max_length, max_length)
        ax.set_zlim3d(-max_length, max_length)

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
        for joint_beg, joint_end, name in traverse_bones():
            x, y, z = joint_beg
            line = zip(joint_beg, joint_end)

            #here inverse because y and z axis are inversed
            ax.plot(line[0], line[2], line[1], color="b")
            ax.scatter(x, z, y, color="r", marker=".")
            if display_names:
                ax.text(x, z, y, name, size=10, zorder=1, color='k')

    fig = plt.figure()
    ax = fig.gca(projection='3d')

    scale_equally(ax)
    draw_skeleton(ax)

    plt.xlabel('x')
    plt.ylabel('z')
    plt.show()
