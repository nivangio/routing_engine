from get_time_constrains import get_time_constrains
from get_time_matrix import get_time_matrix
from ortools.constraint_solver import pywrapcp, routing_enums_pb2

def optimize_route(config):

    elem = {}
    elem['time_matrix'] = get_time_matrix(config)
    elem['time_windows'] = get_time_constrains(config)
    elem['num_vehicles'] = config["vehicles"]
    elem['depot'] = 0

    manager = pywrapcp.RoutingIndexManager(len(elem['time_matrix']),
                                           elem['num_vehicles'], elem['depot'])

    routing = pywrapcp.RoutingModel(manager)

    def time_callback(from_index, to_index):
        """Returns the travel time between the two nodes."""
        # Convert from routing variable Index to time matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return elem['time_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(time_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    time = 'Time'
    routing.AddDimension(
        transit_callback_index,
        30,  # allow waiting time
        int(elem['time_matrix'].sum()), # SET THIS TO WORST CASE SCENARIO 300000,  # maximum time per vehicle
        False,  # Don't force start cumul to zero.
        time)
    time_dimension = routing.GetDimensionOrDie(time)
    # Add time window constraints for each location except depot.
    for location_idx, time_window in enumerate(elem['time_windows']):
        if location_idx == 0:
            continue
        index = manager.NodeToIndex(location_idx)
        time_dimension.CumulVar(index).SetRange(time_window[0], time_window[1])
    # Add time window constraints for each vehicle start node.
    for vehicle_id in range(elem['num_vehicles']):
        index = routing.Start(vehicle_id)
        time_dimension.CumulVar(index).SetRange(elem['time_windows'][0][0],
                                                elem['time_windows'][0][1])
    for i in range(elem['num_vehicles']):
        routing.AddVariableMinimizedByFinalizer(
            time_dimension.CumulVar(routing.Start(i)))
        routing.AddVariableMinimizedByFinalizer(
            time_dimension.CumulVar(routing.End(i)))

    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    # Solve the problem.
    #BUG IN THISLINE, IT DOESN'T SOLVE SHIT! RETURNS None
    solution = routing.SolveWithParameters(search_parameters)
    ret = []

    index = routing.Start(0)
    elem_order = []
    while not routing.IsEnd(index):
        elem_id = manager.IndexToNode(index)
        previous_index = index
        index = solution.Value(routing.NextVar(index))
        route_distance = routing.GetArcCostForVehicle(previous_index, index, 0)
        elem_order.append((elem_id, route_distance))
    print(elem_order) # Warning maybe this should be the output!
    return solution


from json import load as jsonload

with open("json_sample.json") as f:
    sample = jsonload(f)

optimize_route(sample)
