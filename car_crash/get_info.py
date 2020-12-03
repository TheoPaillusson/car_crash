import pandas as pd
import datetime
from datetime import datetime



def get_week_of_the_year(x):
    return pd.to_datetime(x).isocalendar()[1]

def get_day_of_the_week(x):
    return pd.to_datetime(x).weekday()

def get_hour(x):
    return pd.to_datetime(x).hour

