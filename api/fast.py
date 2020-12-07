from fastapi import FastAPI
from car_crash.test_api import model_predict, user_data
from app.app import return_inputs
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

departure, arrival = return_inputs()
danger = model_predict()


# testing the api response
@app.get("/danger/")
def return_danger():
    return {"mean_danger": danger, 'test':departure}