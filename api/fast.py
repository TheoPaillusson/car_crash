from fastapi import FastAPI
from car_crash.test_api import model_predict, user_data

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello World"}


# variables de l'url
departure, arrival = user_data()
danger = model_predict(departure=departure, arrival=arrival)

# testing the api response
@app.get("/danger/{d_long}/{d_lat}/{a_long}/{a_lat}")
def return_danger(d_long: float, d_lat: float, a_long: float, a_lat: float ):
    return {"mean_danger": danger}