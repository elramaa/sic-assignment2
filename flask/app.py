from flask import Flask, request, render_template
from dotenv import load_dotenv
import pymongo
import os
from utils import get_time_now, send_ubidots

load_dotenv()
AUTH_TOKEN = "novasmansa321"

app = Flask(__name__)
client = pymongo.MongoClient(os.getenv("MONGO_URL"))
db = client["db"]


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/temp", methods=["GET", "POST"])
def temp_api():
    collections = db["temperature"]
    if request.method == "POST":
        if request.headers.get("X-Auth-Token") != AUTH_TOKEN:
            return "Unauthorized", 401
        temp = request.json["temp"]
        print(temp)
        collections.insert_one({"temp": temp, "time": get_time_now()})
        send_ubidots({"temp": temp})
        return f"Data sent: {temp}"
    if request.method == "GET":
        result = collections.find().sort({"time": -1}).limit(50)
        return [{"temp": i["temp"], "time": i["time"]} for i in result]


@app.route("/api/distance", methods=["GET", "POST"])
def distance_api():
    collections = db["distance"]
    if request.method == "POST":
        if request.headers.get("X-Auth-Token") != AUTH_TOKEN:
            return "Unauthorized", 401
        distance = request.json["distance"]
        collections.insert_one({"distance": distance, "time": get_time_now()})
        send_ubidots({"distance": distance})
        return f"Data sent: {distance}"
    if request.method == "GET":
        result = collections.find().sort({"time": -1}).limit(50)
        return [{"distance": i["distance"], "time": i["time"]} for i in result]


@app.route("/api/humidity", methods=["GET", "POST"])
def humidity_api():
    collections = db["humidity"]
    if request.method == "POST":
        if request.headers.get("X-Auth-Token") != AUTH_TOKEN:
            return "Unauthorized", 401
        humidity = request.json["humidity"]
        collections.insert_one({"humidity": humidity, "time": get_time_now()})
        send_ubidots({"humidity": humidity})
        return f"Data sent: {humidity}"
    if request.method == "GET":
        result = collections.find().sort({"time": -1}).limit(50)
        return [{"humidity": i["humidity"], "time": i["time"]} for i in result]


@app.route("/api/iot", methods=["POST"])
def iot_api():
    humidity_collections = db["humidity"]
    temp_collections = db["temperature"]
    distance_collections = db["distance"]
    if request.method == "POST":
        if request.headers.get("X-Auth-Token") != AUTH_TOKEN:
            return "Unauthorized", 401
        humidity = request.json["humidity"]
        distance = request.json["distance"]
        temp = request.json["temp"]
        humidity_collections.insert_one({"humidity": humidity, "time": get_time_now()})
        distance_collections.insert_one({"distance": distance, "time": get_time_now()})
        temp_collections.insert_one({"temp": temp, "time": get_time_now()})
        data = {"humidity": humidity, "distance": distance, "temp": temp}
        send_ubidots(data)
        return data


if __name__ == "__main__":
    app.run()
