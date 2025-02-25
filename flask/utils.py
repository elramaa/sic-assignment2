import datetime
from dotenv import load_dotenv
import os
import json
import requests as req
from zoneinfo import ZoneInfo

load_dotenv()


def get_time_now():
    return datetime.datetime.now(tz=ZoneInfo("Asia/Jakarta"))


def send_ubidots(data):
    UBIDOTS_DEVICE_ID = os.getenv("UBIDOTS_DEVICE_ID")
    UBIDOTS_TOKEN = os.getenv("UBIDOTS_TOKEN")
    url = "http://industrial.api.ubidots.com/api/v1.6/devices/" + UBIDOTS_DEVICE_ID
    headers = {"Content-Type": "application/json", "X-Auth-Token": UBIDOTS_TOKEN}
    try:
        response = req.post(url=url, data=json.dumps(data), headers=headers)
        print("Ubidots Response:", response.text)
        del response  # Hapus response untuk menghemat memori
    except Exception as e:
        print("Gagal mengirim data:", e)
