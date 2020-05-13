from numpy import Inf

def get_time_constrains(config):

    ret = []
    ret.append((0,99999999999999))
    for i in config["directions"]:
        ##lower is arrive_after
        if "arrive_after" in i.keys():
            lower_bound = max(0,i.get("arrive_after") - config["starting_time"])
        else:
            lower_bound = 0

        if "arrive_before" in i.keys():
            upper_bound = i.get("arrive_before") - config["starting_time"]
        else:
            ##Set a value large enough for it to not get constrained
            upper_bound = 3600000000000

        ret.append((lower_bound, upper_bound))

    ##Quick way to check if all are (0,inf)
    # if len(set(ret)) == 0 and list(set(ret))[0] == (0,float('inf')):
    #     return None

    return ret
