base_url = "http://router.project-osrm.org/table/v1/driving/{}"
from requests import get
from json import loads as jsonloadstring
from numpy import array, round as npround
from all_points_to_str import all_points_to_str
import numpy as np

def get_time_matrix(config):

    points_str = all_points_to_str(config)

    request_url = base_url.format(points_str)

    response = get(request_url)

    response_dict = jsonloadstring(response.text)
    ret = array(response_dict["durations"]).astype(int)

    return ret

def get_fake_time_matrix(config):

    ret = np.array( [
np.array([0, 1232, 1599, 964, 1488, 1441, 1291, 1323, 978, 1228, 1493, 1617, 1570, 765, 1272, 1359]),
np.array([1333, 0, 653, 922, 542, 495, 864, 297, 917, 622, 783, 671, 624, 1059, 985, 904]),
np.array([1669, 643, 0, 1291, 447, 161, 1021, 461, 1258, 862, 715, 419, 198, 1395, 855, 904]),
np.array([1062, 862, 1262, 0, 946, 1104, 360, 926, 61, 482, 995, 1237, 1190, 589, 761, 839]),
np.array([1626, 600, 475, 1008, 0, 317, 688, 505, 976, 630, 446, 475, 428, 1271, 587, 648]),
np.array([1537, 511, 166, 1158, 314, 0, 889, 402, 1125, 730, 697, 430, 313, 1262, 837, 770]),
np.array([1388, 891, 1022, 374, 668, 863, 0, 731, 341, 259, 731, 1110, 1091, 869, 496, 570]),
np.array([1407, 303, 489, 934, 492, 410, 725, 0, 901, 482, 692, 580, 587, 1132, 845, 814]),
np.array([1060, 914, 1215, 55, 899, 1057, 314, 880, 0, 435, 949, 1190, 1144, 528, 714, 792]),
np.array([1314, 651, 855, 475, 605, 696, 260, 491, 443, 0, 700, 830, 783, 970, 489, 596]),
np.array([1530, 801, 697, 990, 427, 625, 709, 721, 957, 663, 0, 542, 634, 1084, 338, 387]),
np.array([1704, 678, 370, 1355, 508, 430, 1074, 598, 1322, 866, 564, 0, 297, 1405, 703, 752]),
np.array([1612, 586, 215, 1201, 416, 359, 1070, 506, 1169, 773, 639, 313, 0, 1312, 778, 827]),
np.array([861, 1074, 1441, 610, 1337, 1282, 869, 1164, 555, 990, 1157, 1433, 1386, 0, 936, 1022]),
np.array([1375, 1045, 899, 795, 629, 825, 588, 901, 762, 549, 408, 744, 836, 929, 0, 107]),
np.array([1428, 947, 957, 885, 692, 750, 599, 867, 852, 637, 362, 803, 894, 982, 111, 0]) ])

    return ret
