import pandas as pd
from predict import scaling

def get_data():
    '''returns a DataFrame'''
    dataframe = pd.read_csv('../raw_data/clean.csv').drop(columns = ['primary_road','weather_1','latitude','longitude','week_of_the_year','case_id'])
    dataframe['routes'] = dataframe['routes'].apply(lambda x : x.upper())
    dataframe['collision_severity'] = dataframe['collision_severity'].apply(scaling)
    dataframe['collision_severity'] = dataframe['collision_severity'].apply(int)
    return dataframe
