import openrouteservice

coords = ((-0.1257, 51.5085), (-0.1425, 51.5074))  # London coordinates
client = openrouteservice.Client(key='OPEN_ROUTE_SRVICE_API_KEY')
routes = client.directions(coords)
print(routes)