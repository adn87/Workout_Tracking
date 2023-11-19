import os

import requests
from datetime import datetime
from os import environ

Gender = "male"
WEIGHT_KG = 94
HEIGHT_CM = 188
AGE = 28

APP_ID = environ["APP_ID"]
API_KEY = environ["API_KEY"]

exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
sheet_endpoint = environ["sheet_endpoint"]

exercise_text = input("Tell me what you exercised today: ")

headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY
}

parameters = {
    "query": exercise_text,
    "gender": Gender,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}
response = requests.post(url=exercise_endpoint, json=parameters, headers=headers)
response.raise_for_status()
result = response.json()

today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%X")

for exercise in result["exercises"]:
    sheet_input = {
        'workout': {
            "date": today_date,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }
    bearer_header = {
        "Authorization": f"Bearer {environ["TOKEN"]}"
    }
    sheet_response = requests.post(url=sheet_endpoint, json=sheet_input, headers=bearer_header)
    print(sheet_response.text)

