import openrouteservice
from geopy.geocoders import Nominatim
import os
from dotenv import load_dotenv

load_dotenv()

geolocator = Nominatim(user_agent="tsp_for_maps") # App name specification


# If you looking for a specific place, you can add its name here, but if you want to use coordinates, you have to use the: geolocator.reverse() function.
location1 = geolocator.geocode("Győr, Baross Gábor út 1.")
location2 = geolocator.geocode("Győr, Szent István út 10.")  # Changed to a different address


# You can print the coordinates of the address.
location1_latitude = location1.latitude
location1_longitude = location1.longitude

location2_latitude = location2.latitude
location2_longitude = location2.longitude


coords = ((location1.longitude, location1.latitude), (location2.longitude, location2.latitude))  # (longitude, latitude) order
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


distance_m = routes["features"][0]["properties"]["segments"][0]["distance"]

if distance_m >= 1000:
    print(f"The distance between the two locations is {distance_m/1000} kilometers.")
else:
    print(f"The distance between the two locations is {distance_m} meters.")


