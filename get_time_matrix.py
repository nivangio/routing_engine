base_url = "http://router.project-osrm.org/table/v1/driving/{}"
from requests import get
from json import loads as jsonloadstring
from numpy import array, round as npround
from all_points_to_str import all_points_to_str

def get_time_matrix(config):

    points_str = all_points_to_str(config)

    request_url = base_url.format(points_str)

    response = get(request_url)

    response_dict = jsonloadstring(response.text)
    ret = array(response_dict["durations"]).astype(int)

    return ret