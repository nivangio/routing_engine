
def get_points_to_visit(config, route_points):

    ret = []
    ###Since 0 = depot, start at 1
    for i in route_points[1:]:
        ##It's i-1 because the index order includes the depor as 0
        ret.append(config["directions"][(i-1)])

    return ret

