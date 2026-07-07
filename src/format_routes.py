# Define print_route_details
def print_route_details(solution, manager, routing, vehicle_count, demands,
                        solution_name="Solution"):

    print(f"\n--- {solution_name} ---")
    print(f"Objective: {solution.ObjectiveValue()} meters")
    total_distance = 0
    total_load = 0
    used_vehicles = 0

    for vehicle_id in range(vehicle_count):
        index = routing.Start(vehicle_id)
        route_nodes = []
        route_distance = 0
        route_load = 0

        # Check if the vehicle actually has a route.
        # A vehicle is used if its next stop from the start is not its end depot
        if solution.Value(routing.NextVar(index)) != routing.End(vehicle_id):
            used_vehicles += 1
            print(f"Route for vehicle {vehicle_id}:")
            while not routing.IsEnd(index):
                node_index = manager.IndexToNode(index)
                route_load += demands[node_index]
                route_nodes.append(node_index)
                previous_index = index
                index = solution.Value(routing.NextVar(index))
                route_distance += routing.GetArcCostForVehicle(previous_index, index, vehicle_id)

            # Add the last node (which should be the depot) to complete the route visualization
            node_index = manager.IndexToNode(index)
            route_nodes.append(node_index)

            print(" " + " -> ".join(map(str, route_nodes)))
            print(f"Distance of the route: {route_distance}m")
            print(f"Load of the route: {route_load}\n")
            total_distance += route_distance
            total_load += route_load
        else:
            print(f"Route for vehicle {vehicle_id}: (unused)\n") # Explicitly indicate unused vehicles

    print(f"Total distance of all routes: {total_distance}m")
    print(f"Total load of all routes: {total_load}")
    print(f"Number of vehicles used: {used_vehicles}/{vehicle_count}")