### Visualizing the Routes Using Folium

# Imports Dependencies
import folium
import requests
import numpy as np
import time
import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


# Selenium html_to_png
def html_to_png(html_file, output_file):
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1400,900")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    driver.get("file://" + os.path.abspath(html_file))

    # wait for map tiles to load
    time.sleep(5)

    driver.save_screenshot(output_file)
    driver.quit()


# OSRM Route: This will provide appox. real png route images
def get_osrm_route(coords):
    if len(coords) < 2:
        return None

    coord_str = ";".join([f"{lon},{lat}" for lat, lon in coords])

    url = f"http://router.project-osrm.org/route/v1/driving/{coord_str}?overview=full&geometries=geojson"

    try:
        res = requests.get(url, timeout=10).json()

        if "routes" in res and len(res["routes"]) > 0:
            return res["routes"][0]["geometry"]
        else:
            return None
    except:
        return None
    

# Random Color
def get_random_color():
    return '#%06X' % np.random.randint(0, 0xFFFFFF)


# Main Function 
def generate_vehicle_images(solution, manager, routing,
                            locations, demands,
                            vehicle_count, solution_name):

    print(f"\nGenerating maps for {solution_name}...")
    depot_lat, depot_lon = locations[0]

    output_dir = "outputs"
    os.makedirs(output_dir, exist_ok=True)

    generated_images = []

    for vehicle_id in range(vehicle_count):

        index = routing.Start(vehicle_id)
        route_coords = []
        stop_order = 0

        # skip unused vehicles
        if solution.Value(routing.NextVar(index)) == routing.End(vehicle_id):
            continue

        # Create map
        m = folium.Map(location=[depot_lat, depot_lon],
                       zoom_start=10,
                       tiles='OpenStreetMap')

        # Depot
        folium.Marker(
            [depot_lat, depot_lon],
            popup="Depot",
            icon=folium.Icon(color="red")
        ).add_to(m)

        route_color = get_random_color()

        # Build route
        while not routing.IsEnd(index):
            node = manager.IndexToNode(index)
            lat, lon = locations[node]
            route_coords.append([lat, lon])

            if node != 0:
                stop_order += 1
                folium.Marker(
                    [lat, lon],
                    popup=f"Stop {stop_order} | Demand {demands[node]}",
                    icon=folium.Icon(color="blue")
                ).add_to(m)

            index = solution.Value(routing.NextVar(index))

        # return to depot
        node = manager.IndexToNode(index)
        lat, lon = locations[node]
        route_coords.append([lat, lon])

        # Get real road route (OSRM)
        geojson = None
        if len(route_coords) <= 100:
            geojson = get_osrm_route(route_coords)

        # Draw route
        if geojson:
            folium.GeoJson(
                geojson,
                style_function=lambda x: {
                    "color": route_color,
                    "weight": 4
                }
            ).add_to(m)

            coords_geo = geojson["coordinates"]
            latlon = [[lat, lon] for lon, lat in coords_geo]
            m.fit_bounds(latlon)

        else:
            folium.PolyLine(route_coords,
                            color=route_color,
                            weight=4).add_to(m)
            m.fit_bounds(route_coords)

        # Title
        title = f"<h3 align='center'>{solution_name} - Vehicle {vehicle_id}</h3>"
        m.get_root().html.add_child(folium.Element(title))

        # Save files
        html_file = os.path.join(output_dir, f"temp_vehicle_{vehicle_id}.html")
        png_file = os.path.join(output_dir, f"vehicle_{vehicle_id}.png")

        # Save temporary HTML
        m.save(html_file)

        try:
            html_to_png(html_file, png_file)
            print(f"✅ Vehicle {vehicle_id} PNG saved")
            generated_images.append(png_file)
        except Exception as e:
            print(f"❌ Vehicle {vehicle_id} failed: {e}")

        # 🔥 Delete HTML after screenshot
        if os.path.exists(html_file):
            os.remove(html_file)

        time.sleep(1)

    return generated_images