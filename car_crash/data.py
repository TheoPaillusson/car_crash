import pandas as pd

clean_path = 'raw_data/clean.csv'

def scaling(x):
    return 2.5195**x - 1.5195


def get_data():
    '''returns a DataFrame'''
    dataframe = pd.read_csv(clean_path).drop(columns = ['primary_road','weather_1','latitude','longitude','week_of_the_year','case_id'])
    dataframe['routes'] = dataframe['routes'].apply(lambda x : x.upper())
    dataframe['collision_severity'] = dataframe['collision_severity'].apply(scaling)
    dataframe['collision_severity'] = dataframe['collision_severity'].apply(int)
    return dataframe

