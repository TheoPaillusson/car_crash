import pandas as pd
from car_crash.get_info import get_week_of_the_year, get_day_of_the_week, get_hour
from data import get_data

def convert_data(datetime, road):
    X = pd.DataFrame(dict(
        week_of_the_year=[float(get_week_of_the_year(datetime))],
        day_of_the_week=[float(get_day_of_the_week(datetime))],
        hour=[float(get_hour(datetime))],
        road=[str(road)]))
    return X


def groupby(road,week,day,hour):
    df = get_data()
    inter = df[(df['primary_road'] == road) & (df['week_of_the_year'] == week) \
                        & (df['day_of_the_week'] == day) \
                        & (df['hour'] == hour)]
    result = round(inter['collision_severity'].mean(),2)
    return result


def mean_danger(dictionnary,week,day,hour):
    mean_danger = 0
    sum_dist = 0
    for key,value in dictionnary.items():
        mean_danger += groupby(key,week,day,hour) * value
        sum_dist += value
    mean_danger = mean_danger/sum_dist

    return mean_danger

def test_predict():
    return 