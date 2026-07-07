# Import Library
import requests

def get_osrm_route(coords):
    if len(coords) < 2:
        return None, 0, 0

    coord_str = ";".join([f"{lon},{lat}" for lat, lon in coords])

    url = f"http://router.project-osrm.org/route/v1/driving/{coord_str}?overview=full&geometries=geojson"

    try:
        res = requests.get(url, timeout=10).json()
        if "routes" in res and len(res["routes"]) > 0:
            route = res["routes"][0]
            return route["geometry"], route["distance"], route["duration"]
        else:
            return None, 0, 0
    except Exception as e:
        print(f"Error fetching OSRM route: {e}")
        return None, 0, 0 
    

# To get the summary result table...
import pandas as pd

def generate_route_summary_table(solution, manager, routing, locations, demands, vehicle_count):
    route_summaries = []

    print("Collecting route data for table...")

    for vehicle_id in range(vehicle_count):
        index = routing.Start(vehicle_id)
        route_nodes_indices = []
        route_demands = 0
        num_stops = 0
        current_route_coords = []

        # Skip unused vehicles
        if solution.Value(routing.NextVar(index)) == routing.End(vehicle_id):
            continue

        # Add depot to route coordinates
        depot_node = manager.IndexToNode(routing.Start(vehicle_id))
        current_route_coords.append(locations[depot_node])

        while not routing.IsEnd(index):
            node = manager.IndexToNode(index)
            current_route_coords.append(locations[node])

            if node != 0:  # Exclude depot from stops count and demand
                num_stops += 1
                route_demands += demands[node]

            index = solution.Value(routing.NextVar(index))

        # Add final depot to route coordinates
        final_depot_node = manager.IndexToNode(routing.End(vehicle_id))
        current_route_coords.append(locations[final_depot_node])

        # Get OSRM estimated distance and duration
        # Ensure get_osrm_route returns 3 values: geojson, distance, duration
        geojson, osrm_distance, osrm_duration = get_osrm_route(current_route_coords)

        # Convert OSRM duration from seconds to minutes
        osrm_duration_min = osrm_duration / 60

        route_summaries.append({
            "Vehicle ID": vehicle_id,
            "No. of Stops": num_stops,
            "Total Daily Demand (kg)": route_demands,
            "Est. Distance (km)": round(osrm_distance / 1000, 2),
            "Est. Time (min)": round(osrm_duration_min, 2)
        })

    df_summary = pd.DataFrame(route_summaries)
    return df_summary
