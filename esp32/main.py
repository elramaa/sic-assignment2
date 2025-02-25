from machine import Pin, SoftI2C
import ujson
import network
import utime as time
import dht
import urequests as requests
from hcsr04 import HCSR04
import ssd1306
from time import sleep



DEVICE_ID = "nova-dashboard"
WIFI_SSID = "internet gratis"
WIFI_PASSWORD = "admin1234"
DHT_PIN = Pin(13)
sensor = HCSR04(trigger_pin=15, echo_pin=17, echo_timeout_us=10000)
i2c = SoftI2C(scl=Pin(22), sda=Pin(21))

oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

def send_data(temperature, humidity, distance):
    url = "https://nova-sic-api.vercel.app/api/iot"
    headers = {"Content-Type": "application/json", "X-Auth-Token": "novasmansa321"}
    data = {
        "temp": temperature,
        "humidity": humidity,
        "distance": distance
    }

    try:
        response = requests.post(url=url, data=ujson.dumps(data), headers=headers)
        print("Sent Data:", data)  # Debugging
        print("Response Code:", response.status_code)
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
        oled.fill(0)
        #oled.show()
        dht_sensor.measure()
        temperature = dht_sensor.temperature()
        humidity = dht_sensor.humidity()
        distance = sensor.distance_cm()
        oled.text(f"Suhu: {temperature}C", 0, 0)
        oled.text(f"Kelembaban: {humidity}%", 0, 10)
        oled.text("Ketinggian air:", 0, 20)
        oled.text(f"{distance:.2f} cm", 0, 30)
        oled.show()
        print(f"\nSuhu: {temperature}°C, Kelembaban: {humidity}%, Distance: {distance:.2f} cm")
        send_data(temperature, humidity, distance)
    except Exception as e:
        print("Error membaca sensor DHT11:", e)

    time.sleep(5)
