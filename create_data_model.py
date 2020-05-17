from get_time_constrains import get_time_constrains
from get_time_matrix import get_time_matrix

def create_data_model(config):
    data = {}
    data['time_matrix'] = get_time_matrix(config)
    #data['time_matrix'] = get_fake_time_matrix(config)
    data['time_windows'] = get_time_constrains(config)
    data['num_vehicles'] = len(config['vehicles'])

    ##Las demands estan en cada item y las paso a array
    data['demands'] = list(map(lambda x: x['demands'], config["directions"]))
    ##Add an insert to demands. This is to specify that it starts in an empty state.
    ##Could be dynamic in a future occation
    data['demands'].insert(0,0)

    data['vehicle_capacities'] = list(map(lambda x: x['vehicle_capacity'], config["vehicles"]))
    data['depot'] = 0
    return data