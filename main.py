import openrouteservice
from geopy.geocoders import Nominatim
import os
from dotenv import load_dotenv

import numpy as np
from python_tsp.distances import great_circle_distance_matrix
from python_tsp.heuristics import solve_tsp_simulated_annealing
from python_tsp.exact import solve_tsp_dynamic_programming



load_dotenv()

geolocator = Nominatim(user_agent="tsp_for_maps") # App name specification


# If you looking for a specific place, you can add its name here, but if you want to use coordinates, you have to use the: geolocator.reverse() function.
location1 = geolocator.geocode("Győr, Baross Gábor út 1.")
if location1 is None:
    raise ValueError("Address not found: Győr, Baross Gábor út 1.")

location2 = geolocator.geocode("Győr, Szent István út 10.")
if location2 is None:
    raise ValueError("Address not found: Győr, Szent István út 10.")

location3 = geolocator.geocode("Győr, Széchenyi tér 7.")
if location3 is None:
    raise ValueError("Address not found: Győr, Széchenyi tér 7.")
location4 = geolocator.geocode("Győr,Széchenyi út 4.")

# You can print the coordinates of the address.
location1_latitude = location1.latitude
location1_longitude = location1.longitude

location2_latitude = location2.latitude
location2_longitude = location2.longitude

location3_latitude = location3.latitude
location3_longitude = location3.longitude

location4_latitude = location4.latitude
location4_longitude = location4.longitude

coords = ((location1.longitude, location1.latitude), (location2.longitude, location2.latitude), (location3.longitude, location3.latitude), (location4.longitude, location4.latitude))  # (longitude, latitude) order
api_key = os.environ.get('OPEN_ROUTE_SERVICE_API_KEY')
if not api_key:
    raise ValueError("Please set the OPEN_ROUTE_SERVICE_API_KEY environment variable.")
client = openrouteservice.Client(key=api_key) # Specify your personal API key
# You can choose between different travel modes:
# 'driving-car', 'cycling-regular', 'foot-walking'
mode = 'foot-walking'

routes = client.directions(
    coords,
    profile=mode,
    format='geojson' # specify the format of the output data, you can choose between 'geojson', 'gpx', 'kml', 'osrm', 'string', 'svg' or 'text'
    )

sources = np.array([
    [location1_latitude, location1_longitude],
    [location2_latitude, location2_longitude],
    [location3_latitude, location3_longitude],
    [location4_latitude, location4_longitude]
])
distance_matrix = great_circle_distance_matrix(sources)
# Use  the heuristic TSP solver function
permutation_heuristic, distance_heuristic = solve_tsp_simulated_annealing(distance_matrix)
# Use the exact TSP solver function (dynamic programming as imported)
permutation_exact, distance_exact = solve_tsp_dynamic_programming(distance_matrix)

if distance_heuristic == distance_exact:
    print("The heuristic and exact solutions match." + str(distance_exact) + " meters" + " Route: " + str(permutation_exact))
elif distance_heuristic < distance_exact:
    print("The heuristic solution is better than the exact solution, which is unexpected. " + str(distance_heuristic) + " meters" + " Route: " + str(permutation_heuristic))
else:
    print("The exact solution is better than the heuristic solution." + str(distance_exact) + " meters" + " Route: " + str(permutation_exact))

