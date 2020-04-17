base_url = "http://router.project-osrm.org/table/v1/driving/{}"
from requests import get
from json import loads as jsonloadstring
from numpy import array, round as npround

def get_time_matrix(config):

    ##Build points and make request
    all_points = []

    all_points.append(config["starting_location"]["long"] + "," + config["starting_location"]["lat"])

    for i in config["directions"]:
        all_points.append(i["long"] + "," + config["starting_location"]["lat"])

    points_str = ";".join(all_points)

    request_url = base_url.format(points_str)

    response = get(request_url)

    response_dict = jsonloadstring(response.text)
    ret = array(response_dict["durations"]).astype(int)

    return ret