import pandas as pd

import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from get_info import get_week_of_the_year, get_day_of_the_week, get_hour
from data import get_data

def convert_data(datetime, road):
    X = pd.DataFrame(dict(
        day_of_the_week=[float(get_day_of_the_week(datetime))],
        hour=[float(get_hour(datetime))],
        road=[str(road)]))
    return X

def scaling(x):
    return 2.5195**x - 1.5195

def dispatch_roads(dictionary,dataframe,day,hour):
    """
    From a trip dictionary with roads as keys and distances as values,
    dispatches the roads into 3 lists according to the scenario
    """
    list_road_day_hour = []
    list_no_road = []
    list_no_day_hour = []

    for key,value in dictionary.items():

        if key.upper() not in dataframe['routes'].unique():
            list_no_road.append(key.upper())

        elif len(dataframe[(dataframe['routes'] == key.upper()) \
                           & (dataframe['day_of_the_week'] == day) \
                           & (dataframe['hour'] == hour)]) == 0:
            list_no_day_hour.append(key.upper())

        else:
            list_road_day_hour.append(key.upper())

    return list_road_day_hour, list_no_road, list_no_day_hour

def road_day_hour(dataframe,list_roads,day,hour):
    """
    For tuples of (roads,day,hour) we have data on,
    returns a dictionnary with roads as keys
    and collision severity estimates as values
    """
    dict_predict = {}

    for road in list_roads:
        inter = dataframe[(dataframe['routes'] == road) \
                                    & (dataframe['day_of_the_week'] == day) \
                                    & (dataframe['hour'] == hour)]
        result = inter['collision_severity'].mean()
        dict_predict[road] = result

    return dict_predict

def road_not_in_roads(dataframe,list_roads,day,hour):
    """
    For roads don't have,
    returns a dictionnary with roads as keys
    and collision severity estimates as values
    """
    dict_predict = {}

    inter = dataframe[(dataframe['day_of_the_week'] == day) \
                      & (dataframe['hour'] == hour)]
    result = inter['collision_severity'].mean()

    for road in list_roads:
        dict_predict[road] = result

    return dict_predict

def no_day_hour(dataframe,list_roads,day,hour):
    """
    For roads we have, for which we don't have data on that date/hour,
    returns a dictionnary with roads as keys
    and collision severity estimates as values
    """
    inter = dataframe[dataframe['routes'].isin(list_roads)].copy()

    X = inter.drop(columns = ['collision_severity'])
    y = inter[['collision_severity']]

    preprocessor = ColumnTransformer([('road_transformer', OneHotEncoder(sparse = False), ['routes'])])

    final_pipe = Pipeline([
        ('preprocessing', preprocessor),
        ('linear_regression', LinearRegression())])

    final_pipe_trained = final_pipe.fit(X,y)

    dict_predict = {}

    for road in list_roads:
        X_pred = pd.DataFrame([[hour,day,'DUNNET AVENUE']], columns=['hour','day_of_the_week','routes'])
        result = final_pipe_trained.predict(X_pred.iloc[0:2])
        dict_predict[road] = result[0][0]

    return dict_predict

def concat_3_dict(d1,d2,d3):
    """
    Concatenates 3 dictionaries
    """
    d4 = d1.copy()
    d4.update(d2)
    d4.update(d3)
    return d4

def ponderated_mean(d1,d2):
    """
    Takes two dictionaries in argument :
    the first one has roads in keys and distance in values,
    the second one has roads in keys and collision_severity in values.
    Computes the mean of collision_severities ponderated with distances
    """
    mean_danger = 0
    sum_dist = 0

    for key,value in d1.items():
        mean_danger += d2[key.upper()] * value
        sum_dist += value

    mean_danger = mean_danger/sum_dist

    return mean_danger
