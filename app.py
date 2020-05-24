from flask import Flask, request
from flask_json import FlaskJSON, as_json, JsonError
from create_data_model import create_data_model
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
from pairs import pairs
from all_points_to_str import all_points_to_str
from get_geojson_coordinates import get_geojson_coordinates
from get_points_to_visit import get_points_to_visit
import traceback


app = Flask(__name__)
FlaskJSON(app)

@app.route('/get_optimal_route', methods=['POST'])
@as_json
def optimise_route():

    try:
        config = request.get_json(force=True)

        data = create_data_model(config= config)

        # Create the routing index manager.
        manager = pywrapcp.RoutingIndexManager(len(data['time_matrix']),
                                               data['num_vehicles'], data['depot'])

        # Create Routing Model.
        routing = pywrapcp.RoutingModel(manager)

        # Add Capacity constraint.
        def demand_callback(from_index):
            """Returns the demand of the node."""
            # Convert from routing variable Index to demands NodeIndex.
            from_node = manager.IndexToNode(from_index)
            return data['demands'][from_node]

        demand_callback_index = routing.RegisterUnaryTransitCallback(
            demand_callback)
        routing.AddDimensionWithVehicleCapacity(
            demand_callback_index,
            0,  # null capacity slack
            data['vehicle_capacities'],  # vehicle maximum capacities
            True,  # start cumul to zero
            'Capacity')


        # Create and register a transit callback.
        def time_callback(from_index, to_index):
            """Returns the travel time between the two nodes."""
            # Convert from routing variable Index to time matrix NodeIndex.
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return data['time_matrix'][from_node][to_node]


        transit_callback_index = routing.RegisterTransitCallback(time_callback)

        # Define cost of each arc.
        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)


        # Add Time Windows constraint.
        time = 'Time'
        routing.AddDimension(
            transit_callback_index,
            30,  # allow waiting time
            int(data['time_matrix'].sum()),
            # SET THIS TO WORST CASE SCENARIO #300000,  # maximum time per vehicle
            False,  # Don't force start cumul to zero.
            time)
        time_dimension = routing.GetDimensionOrDie(time)
        # Add time window constraints for each location except depot.
        for location_idx, time_window in enumerate(data['time_windows']):
            if location_idx == 0:
                continue
            index = manager.NodeToIndex(location_idx)
            time_dimension.CumulVar(index).SetRange(time_window[0], time_window[1])
        # Add time window constraints for each vehicle start node.
        for vehicle_id in range(data['num_vehicles']):
            index = routing.Start(vehicle_id)
            time_dimension.CumulVar(index).SetRange(data['time_windows'][0][0],
                                                    data['time_windows'][0][1])

        # Instantiate route start and end times to produce feasible times.
        for i in range(data['num_vehicles']):
            routing.AddVariableMinimizedByFinalizer(
                time_dimension.CumulVar(routing.Start(i)))
            routing.AddVariableMinimizedByFinalizer(
                time_dimension.CumulVar(routing.End(i)))

        # Setting first solution heuristic.
        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = (
            routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

        # Solve the problem.
        solution = routing.SolveWithParameters(search_parameters)

        if not solution:
            raise ValueError("No Optimization found")

        times = []
        time_dimension = routing.GetDimensionOrDie('Time')
        features = []
        for vehicle_id in range(data['num_vehicles']):
            index_orders = []
            index = routing.Start(vehicle_id)
            while not routing.IsEnd(index):
                time_var = time_dimension.CumulVar(index)
                times.append(solution.Max(time_var))
                index_orders.append(manager.IndexToNode(index))
                index = solution.Value(routing.NextVar(index))

            ##Get the GEJSONs from OSMP pairwise
            all_points_str = all_points_to_str(config, to_str=False)

            geojsons = []
            for ind, i in enumerate(pairs(index_orders)):

                ###Re-check that n+1 index is actually depot
                try:
                    first_point = all_points_str[ i[0] ]
                ##Improve this
                except IndexError:
                    first_point = all_points_str[ 0 ]

                try:
                    second_point = all_points_str[i[1]]
                ##Improve this
                except IndexError:
                    second_point = all_points_str[ 0 ]
                osmp_return = get_geojson_coordinates(first_point, second_point)

                geojson = {}
                geojson["geometry"] = osmp_return["geometry"]
                geojson["properties"] = {}
                geojson["properties"]["accumulated_duration"] = times[ind]
                geojson["properties"]["vehicle_id"] = vehicle_id
                geojson["type"] = "Feature"

                geojsons.append(geojson)

            ##Append coordinates in coordinates tag
            features.extend(geojsons)
            points_to_visit = get_points_to_visit(config, vehicle_id, index_orders)

            features.extend(points_to_visit)

    except Exception as e:
        traceback.print_exc()
        raise JsonError(description=e.args[0])


    return {"type": "FeatureCollection", "features": features}

if __name__ == "__main__":
    app.run(port=5000, host='0.0.0.0')
    #app.run(port=5000)
