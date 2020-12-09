import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn import preprocessing
from data import get_data

def dispatch_roads(dataframe_trajet,dataframe,day,hour):
    """
    From a trip DataFrame with roads and distances,
    dispatches the roads into 3 lists according to the scenario
    """
    list_road_day_hour = []
    list_no_road = []
    list_no_day_hour = []

    for road in dataframe_trajet['names']:

        if str(road).upper() not in dataframe['routes'].unique():
            list_no_road.append(str(road).upper())

        elif len(dataframe[(dataframe['routes'] == str(road).upper()) \
                           & (dataframe['day_of_the_week'] == day) & (dataframe['hour'] == hour)]) == 0:
            list_no_day_hour.append(str(road).upper())

        else:
            list_road_day_hour.append(str(road).upper())

    return list_road_day_hour, list_no_road, list_no_day_hour

def road_day_hour(dataframe,list_roads,day,hour):
    """
    For tuples of (roads,day,hour) we have data on,
    returns a dataframe with roads and collision
    severity estimates
    """
    list_pred = []

    for road in list_roads:
        inter = dataframe[(dataframe['routes'] == road) \
                                    & (dataframe['day_of_the_week'] == day) \
                                    & (dataframe['hour'] == hour)]
        result = inter['collision_severity'].mean()
        list_pred.append(result)
    dict_pred = {'names':list_roads,'collision_severity':list_pred}
    df_pred = pd.DataFrame(dict_pred)

    return df_pred

def road_not_in_roads(dataframe,list_roads,day,hour):
    """
    For roads don't have,
    returns a dictionnary with roads as keys
    and collision severity estimates as values
    """
    list_pred = []

    inter = dataframe[(dataframe['day_of_the_week'] == day) \
                      & (dataframe['hour'] == hour)]
    result = inter['collision_severity'].mean()

    for road in list_roads:
        list_pred.append(result)

    dict_pred = {'names':list_roads,'collision_severity':list_pred}
    df_pred = pd.DataFrame(dict_pred)

    return df_pred

def no_day_hour(dataframe,list_roads,day,hour):
    """
    For roads we have, for which we don't have data on that date/hour,
    returns a dictionnary with roads as keys
    and collision severity estimates as values
    """
    inter = df[df['routes'].isin(list_roads)].copy()

    X = inter.drop(columns = ['collision_severity'])
    y = inter['collision_severity']

    preprocessor = ColumnTransformer([('road_transformer', OneHotEncoder(sparse = False), ['routes'])])

    forest = RandomForestRegressor(n_estimators=100, n_jobs = -1)

    final_pipe = Pipeline([
        ('preprocessing', preprocessor),
        ('linear_regression', forest)])

    final_pipe_trained = final_pipe.fit(X,y)

    list_pred = []

    for road in list_roads:
        X_pred = pd.DataFrame([[hour,day,road]], columns=['hour','day_of_the_week','routes'])
        result = final_pipe_trained.predict(X_pred)
        list_pred.append(result[0])

    dict_pred = {'names':list_roads,'collision_severity':list_pred}
    df_pred = pd.DataFrame(dict_pred)

    return df_pred

def concat_3_df(df1,df2,df3):
    """
    Concatenates 3 DataFrames
    """
    return pd.concat([df_1, df_2,df_3]).reset_index(drop=True)

def ponderated_mean(dataframe_trajet,dataframe_severity):
    """
    Takes two dictionaries in argument :
    the first one has roads in keys and distance in values,
    the second one has roads in keys and collision_severity in values.
    Computes the mean of collision_severities ponderated with distances
    """
    mean_danger = 0
    sum_dist = 0

    for i in range(len(dataframe_trajet)):
        inter = df_concat[df_concat['names'] == str(dataframe_trajet['names'][i]).upper()].reset_index(drop=True)
        mean_danger += inter['collision_severity'].loc[0] * dataframe_trajet['distances'][i]
        sum_dist += dataframe_trajet['distances'][i]

    mean_danger = mean_danger/sum_dist

    return mean_danger
