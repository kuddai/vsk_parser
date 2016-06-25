from Learning.data_cleaning import get_segment_anim_data
from vicon_anim_parser.scene_drawer import get_segments_anim
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
segment_id2parent_id, header, anim_data = get_segment_anim_data("Ruslan.vsk", "./SwordMovements/sword_movements_01.csv")
anim = get_segments_anim(anim_data, segment_id2parent_id, scene_length=1100)
plt.show()
