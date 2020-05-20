from copy import deepcopy

def get_points_to_visit(config, vehicle_id, route_points):

    ret = []
    ###Since 0 = depot, start at 1
    for i in route_points[1:]:
        elem = deepcopy(config["directions"][(i-1)])

        ##It's i-1 because the index order includes the depor as 0
        to_append = {"type": "Feature", "geometry":{"type":"Point", "coordinates":[float(elem.pop("long")), float(elem.pop("lat"))]}}
        to_append["properties"] = elem
        to_append["properties"]["vehicle_id"] = vehicle_id
        ret.append(to_append)

    return ret

