#takes two addresses, returns route
import requests

api = GOOGLE_MAP_API

def get_coordinates(departure, arrival, api=api):
    url_start = f'https://maps.googleapis.com/maps/api/geocode/json?address={departure}&key={api}'
    url_destination =f'https://maps.googleapis.com/maps/api/geocode/json?address={arrival}&key={api}'
    response1 = requests.get(url_start).json()
    response2 =requests.get(url_destination).json()
    lon_start = response['results'][0]['geometry']['location']['lng']
    lat_start = response['results'][0]['geometry']['location']['lat']
    lon_end = response2['results'][0]['geometry']['location']['lng']
    lat_end = response2['results'][0]['geometry']['location']['lat']
    return lon_start, lat_start, lon_end, lat_end

coordinates = get_coordinates(departure, arrival, api=api)

def itinerary(coordinates):
    url = f'http://router.project-osrm.org/route/v1/driving/{coordinates[0]},{coordinates[1]};{coordinates[2]},{coordinates[3]}?overview=false&steps=true'
    response = requests.get(url).json()
    step = response['routes'][0]['legs'][0]['steps']
    names = []
    for i in range(len(step)):
        names.append(response['routes'][0]['legs'][0]['steps'][i]['name'])
    del names[-1]
    distances = []
    for i in range(len(step)):
        distances.append(response['routes'][0]['legs'][0]['steps'][i]['distance'])
    del distances[-1]
    route = dict(zip(names,distances))
    return route

# get map
def get_geojson(coordinates):
    url = f'http://router.project-osrm.org/route/v1/driving/{coordinates[0]},{coordinates[1]};{coordinates[2]},{coordinates[3]}?steps=true&geometries=geojson'
    response = requests.get(url).json()
    geojson = response['routes'][0]['geometry']['coordinates']
    return geojson
