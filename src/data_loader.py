# Import library
import pandas as pd
import numpy as np
import time, os

# Library for OR-Tools
from ortools.constraint_solver import pywrapcp, routing_enums_pb2

# Import Math to Calculate Haversine formula
from math import radians, cos, sin, sqrt, atan2

# Library for URL encoding
from urllib.parse import quote

# Load the dataset containing retailer coordinates and demands.
df = pd.read_excel("C:\\Users\\ratha\\OneDrive\\Placement\\end-to-end-projects\\jcci-route-optimizer\\data\\jcci_location_data_latti_longi.xlsx")