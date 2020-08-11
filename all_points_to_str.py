
def all_points_to_str(config, to_str= True):
    ##Build points and make request
    all_points = []

    all_points.append(str(config["starting_location"]["long"]) + "," + str(config["starting_location"]["lat"]))

    for i in config["directions"]:
        all_points.append(str(i["long"]) + "," + str(i["lat"]))

    if to_str:
        points_str = ";".join(all_points)
        return points_str
    else:
        return all_points