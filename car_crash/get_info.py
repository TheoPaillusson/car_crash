import pandas as pd
import datetime
from datetime import datetime

# informations récupérées via l'appli front


def get_day_of_the_week(x):
    return pd.to_datetime(x).weekday()

def get_hour(x):
    return pd.to_datetime(x).hour

