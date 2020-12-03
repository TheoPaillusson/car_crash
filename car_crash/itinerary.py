# take gps coordinates and return name and distance
import requests
def itinerary(start_lon,start_lat,dest_lon,dest_lat):
    url = f'http://router.project-osrm.org/route/v1/driving/{start_lon},{start_lat};{dest_lon},{dest_lat}?overview=false&steps=true'
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
