from get_time_constrains import get_time_constrains
from get_time_matrix import get_time_matrix

def create_data_model(config):
    data = {}
    data['time_matrix'] = get_time_matrix(config)
    data['time_windows'] = get_time_constrains(config)
    data['num_vehicles'] = config['vehicles']
    data['depot'] = 0
    return data