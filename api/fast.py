from fastapi import FastAPI

from car_crash.itinerary import get_coordinates, itinerary
from car_crash.predict import *

import os
from os.path import join, dirname
from dotenv import load_dotenv
from car_crash.data import get_data

api = FastAPI()

# importing the dataframe for predictions
df = get_data()
days_of_the_week = {'Monday':0, 'Tuesday':1, 'Wednesday':2, 'Thursday':3, 'Friday':4, 'Saturday':5, 'Sunday':6}

@api.get("/")
def root():
    return {"message": "Hello World"}

# testing the api response

@api.get("/danger")
def danger(itinerary, day, hour):
    return itinerary


# a debug
@api.get("/dange")
def return_danger(itinerary, day, hour):
    list_road_day_hour, list_no_road, list_no_day_hour = dispatch_roads(dictionary=itinerary, dataframe=df, day=days_of_the_week[day], hour=hour)
    dict_road_day_hour = road_day_hour(dataframe=df, list_roads=list_road_day_hour, day=day, hour=hour)
    dict_no_road = road_not_in_roads(dataframe=df, list_roads=list_no_road, day=day, hour=hour)
    dict_no_day_hour = no_day_hour(dataframe=df, list_roads=list_no_day_hour, day=day, hour=hour)
    df_concat = concat_3_dict(dict_road_day_hour, dict_no_road, dict_no_day_hour)
    danger = ponderated_mean(itinerary, df_concat)
    return danger






