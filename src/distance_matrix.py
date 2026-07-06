# Import sys
import sys
from pathlib import Path
sys.path.append(str(Path.cwd()))

# from scr.data_loader import all
from src.data_loader import *


# Extract Latitude and Longitude
locations = df[['Latitude', 'Longitude']].to_numpy()

# Extract 'Esti_Demand_Per_Day_kg' for all channels
demands = df['Esti_Demand_Per_Day_kg'].tolist()

# Depot coordinates to the 'locations' array.
locations = np.vstack([[28.7909, 77.0655], locations])

# Depot node don't have own demand
demands = [0] + demands

# Shape of the DataFrame
print('Dataset Shape: ', df.shape)


# Calculate the distance between two Geo-Coordinates
def haversine(coord1, coord2):
    # Earth Radius
    R = 6371

    # Convert latitude and longitude from degrees to radians.
    lat1, lon1 = map(radians, coord1)
    lat2, lon2 = map(radians, coord2)

    # Calculate the difference
    d_lat, d_lon = lat2 - lat1, lon2 - lon1

    # Apply the Haversine formula
    a = sin(d_lat/2)**2 + cos(lat1)*cos(lat2)*sin(d_lon/2)**2
    return R * 2 * atan2(sqrt(a), sqrt(1 - a))

# Empty distance matrix to store distances btw all pairs of locations
distance_matrix = np.zeros((len(locations), len(locations)))


# Iterate through all combinations of locations (i, j)
for i in range(len(locations)):
    for j in range(len(locations)):
        # Calculate the distance and Convert it from Kilometers to Meters.
        distance_matrix[i][j] = haversine(locations[i], locations[j]) * 1000
 