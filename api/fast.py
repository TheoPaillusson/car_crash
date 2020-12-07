from fastapi import FastAPI
from car_crash.test_api import model_predict, user_data

import os
from os.path import join, dirname
from dotenv import load_dotenv
# for api key
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
GOOGLE_MAP_API = os.environ.get('GOOGLE_MAP_API')

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello World"}


# variables de l'url

#danger = model_predict()


# testing the api response
@app.get("/danger")
def return_danger(d_long, d_lat, a_long, a_lat):
    print(d_long, d_lat, a_long, a_lat)
    return {"mean_danger": 'danger', 'test':'departure'}
