from machine import Pin
import ujson
import network
import utime as time
import dht
import urequests as requests
from hcsr04 import HCSR04
from time import sleep



DEVICE_ID = "nova-dashboard"
WIFI_SSID = "DESKTOP 5543"
WIFI_PASSWORD = "ahmadganteng321"
TOKEN = "BBUS-GzPYLI0hqdHE4WkQVlo4p3cptliG7R"
DHT_PIN = Pin(13)
sensor = HCSR04(trigger_pin=21, echo_pin=22, echo_timeout_us=10000)

def send_data(temperature, humidity, distance):
    url = "http://192.168.137.95:5000/api/iot"
    headers = {"Content-Type": "application/json"}
    data = {
        "temp": temperature,
        "humidity": humidity,
        "distance": distance
    }

    try:
        response = requests.post(url=url, data=ujson.dumps(data), headers=headers)
        print("Sent Data:", data)  # Debugging
        #print("Response Code:", response.status_code)
        print("Response:", response.text)
        del response  # Hapus response untuk menghemat memori
    except Exception as e:
        print("Gagal mengirim data:", e)

wifi_client = network.WLAN(network.STA_IF)
wifi_client.active(True)
print("Connecting device to WiFi")
wifi_client.connect(WIFI_SSID, WIFI_PASSWORD)

while not wifi_client.isconnected():
    print("Connecting")
    time.sleep(1)
print("WiFi Connected!")
print(wifi_client.ifconfig())

dht_sensor = dht.DHT11(DHT_PIN)

while True:
    try:
        dht_sensor.measure()
        temperature = dht_sensor.temperature()
        humidity = dht_sensor.humidity()
        distance = sensor.distance_cm()
        print(f"\nSuhu: {temperature}°C, Kelembaban: {humidity}%, Distance: {distance:.2f} cm")
        send_data(temperature, humidity, distance)
    except Exception as e:
        print("Error membaca sensor DHT11:", e)

    time.sleep(5)