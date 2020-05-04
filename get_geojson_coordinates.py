from requests import get
from json import  loads as jsonloadstring
base_url = 'http://router.project-osrm.org/route/v1/driving/{};{}?overview=full&geometries=geojson'

def get_geojson_coordinates(point_1,point_2):

    request_url = base_url.format(point_1, point_2)
    response = get(request_url)

    response_dict = jsonloadstring(response.text)
    ret = response_dict["routes"][0]

    return ret