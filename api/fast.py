from fastapi import FastAPI
from car_crash.itinerary import get_coordinates, itinerary
from car_crash.predict import *
import os
from os.path import join, dirname
from dotenv import load_dotenv
from car_crash.data import get_data
from pydantic import BaseModel
import json
import numpy as np

# importing the dataframe for predictions
df = get_data()
days_of_the_week = {'Monday':0, 'Tuesday':1, 'Wednesday':2, 'Thursday':3, 'Friday':4, 'Saturday':5, 'Sunday':6}

# classes to receive road dictionnary
class Trip(BaseModel):
    steps : dict
    day : str
    hour : str
# class Day(BaseModel):
#     day : str

# class Hour(BaseModel):
#     hour : int

api = FastAPI()

@api.get("/")
def root():
    return {"message": "Hello World"}

@api.post("/danger")
# steps = trip dictionnary
def create_trip(trip:Trip):
# computation of dangerousness

    day = days_of_the_week[trip.day]
    hour = int(trip.hour)
    itinerary = trip.steps
    
    itinerary = np.array(itinerary['data'])
    dataframe_trajet = pd.DataFrame(columns=['names', 'distances'])
    dataframe_trajet.names = itinerary[:,0]
    dataframe_trajet.distances = itinerary[:,1]
    dataframe_trajet.distances.apply(lambda x: float(x))
    print(dataframe_trajet)


    list_road_day_hour, list_no_road, list_no_day_hour = dispatch_roads(dataframe_trajet=dataframe_trajet, dataframe=df, day=day, hour=hour)

    dict_road_day_hour = road_day_hour(dataframe=df, list_roads=list_road_day_hour, day=day, hour=hour)
    
    dict_no_road = road_not_in_roads(dataframe=df, list_roads=list_no_road, day=day, hour=hour)
    
    dict_no_day_hour = no_day_hour(dataframe=df, list_roads=list_no_day_hour, day=day, hour=hour)
    
    df_concat = concat_3_df(dict_road_day_hour, dict_no_road, dict_no_day_hour)
    
    mean_danger = ponderated_mean(dataframe_trajet=dataframe_trajet, dataframe_severity=df_concat)
        
    return mean_danger