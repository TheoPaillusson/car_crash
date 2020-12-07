from fastapi import FastAPI
from car_crash.itinerary import get_coordinates, itinerary
import os
from os.path import join, dirname
from dotenv import load_dotenv

api = FastAPI()

# for api key
dotenv_path = join(dirname(dirname(__file__)), '.env')
load_dotenv(dotenv_path)
google_map_api = os.environ.get('GOOGLE_MAP_API')




@api.get("/")
def root():
    return {"message": "Hello World"}

# testing the api response
@api.get("/danger")
def return_danger(departure, arrival):
    coordinates = get_coordinates(departure=departure, arrival=arrival, api=google_map_api)
    return itinerary(coordinates)
