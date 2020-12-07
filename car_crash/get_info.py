import pandas as pd
import datetime
from datetime import datetime
import requests

# informations récupérées via l'appli front

def get_day_of_the_week(x):
    return pd.to_datetime(x).weekday()

def get_hour(x):
    return pd.to_datetime(x).hour

def get_la_weather(api):
    url = f'http://api.openweathermap.org/data/2.5/weather?q=los%20angeles&appid={api}'
    response = requests.get(url).json()
    weather = response['weather'][0]['main']
    if weather == 'Drizzle':
        return 'raining'
    if weather == 'Rain':
        return 'raining'
    if weather == 'Thunderstorm':
        return 'raining'
    if weather == 'Snow':
        return 'snowing'
    if weather == 'Fog':
        return 'fog'
    if weather == 'Clear':
        return 'clear'
    if weather == 'Clouds':
        return 'cloudy'
    if weather == 'mist':
        return 'fog'
    else:
        return 'unknown'
