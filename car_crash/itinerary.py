#takes two addresses, returns route
import requests
from geopy.geocoders import Nominatim
def itinerary(address, destination):
    geolocator = Nominatim(user_agent="car_crash")
    start = geolocator.geocode(address + " Los Angeles")
    end = geolocator.geocode(destination + " Los Angeles")
    longitude_start = start.longitude
    latitude_start = start.latitude
    longitude_end = end.longitude
    latitude_end = end.latitude
    pos = longitude_start, latitude_start, longitude_end, latitude_end
    url = f'http://router.project-osrm.org/route/v1/driving/{pos[0]},{pos[1]};{pos[2]},{pos[3]}?overview=false&steps=true'
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
