# Removed incorrect import of reverse from networkx
import openrouteservice
from geopy.geocoders import Nominatim
import os
from dotenv import load_dotenv

import numpy as np
from python_tsp.distances import great_circle_distance_matrix
from python_tsp.heuristics import solve_tsp_simulated_annealing
from python_tsp.exact import solve_tsp_dynamic_programming
import time
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable



load_dotenv()

geolocator = Nominatim(user_agent="tsp_for_maps", timeout=10) # App name specification


def geocode_with_retries(address, attempts=4, base_delay=1, timeout=10):
    for attempt in range(attempts):
        try:
            return geolocator.geocode(address, timeout=timeout)
        except (GeocoderTimedOut, GeocoderUnavailable):
            if attempt == attempts - 1:
                raise
            time.sleep(base_delay * (2 ** attempt))
    return None

# If you looking for a specific place, you can add its name here, but if you want to use coordinates, you have to use the: geolocator.reverse() function.
location1 = geocode_with_retries("Győr, Baross Gábor út 1.")
if location1 is None:
    raise ValueError("Address not found: Győr, Baross Gábor út 1.")

location2 = geocode_with_retries("Győr, Szent István út 10.")
if location2 is None:
    raise ValueError("Address not found: Győr, Szent István út 10.")

location3 = geocode_with_retries("Győr, Széchenyi tér 7.")
if location3 is None:
    raise ValueError("Address not found: Győr, Széchenyi tér 7.")
location4 = geocode_with_retries("Győr, Széchenyi út 4.")
if location4 is None:
    raise ValueError("Address not found: Győr, Széchenyi út 4.")

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
    [location1_longitude, location1_latitude],
    [location2_longitude, location2_latitude],
    [location3_longitude, location3_latitude],
    [location4_longitude, location4_latitude]
])
distance_matrix = great_circle_distance_matrix(sources)
# Use  the heuristic TSP solver function
permutation_heuristic, distance_heuristic = solve_tsp_simulated_annealing(distance_matrix)
# Use the exact TSP solver function (dynamic programming as imported)
permutation_exact, distance_exact = solve_tsp_dynamic_programming(distance_matrix)

if distance_heuristic >= distance_exact:
    print("The heuristic and exact solutions match." + str(distance_exact) + " meters" )
    for idx in permutation_exact:
        location = geolocator.reverse((coords[idx][1], coords[idx][0]))
        if location:
            print(f"{coords[idx]} -> {location.address}")
        else:
            print(f"Error: {coords[idx]} not found.")
            print(f"Hiba: {coords[idx]} nem található.")
else:
    print("The exact solution is better than the heuristic solution." + str(distance_exact) + " meters" + " Route: " + str(permutation_exact))
    for idx in permutation_heuristic:
        location = geolocator.reverse((coords[idx][1], coords[idx][0]))
        if location:
            print(f"{coords[idx]} -> {location.address}")
        else:
            print(f"Error: {coords[idx]} not found.")
            print(f"Hiba: {coords[idx]} nem található.")
        