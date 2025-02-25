# Perkenalan
Halo, kami dari tim NOVA dari SMAN 1 Malang. Disini proyek yang kami buat adalah suatu iot untuk monitoring water.

# Diagram
![Diagram](/diagram/diagram.jpeg "Diagram")

# Hardware Yang Digunakan
Disini kami menggunakan beberapa hardware, antara lain:
- ESP32
- Sensor ultrasonic
- Sensor suhu
- LCD

# Software yang digunakan
Software yang kami gunakan, yakni:
- Flask as backend
- MongoDB as flask
- Ubidots as dashboard

# API Services
Kami membuat API Services menggunakan flask, yang dapat diakses secara umum melalui link https://nova-sic-api.vercel.app
Untuk route yang tersedia, yakni:
- `/` untuk melihat dashboard yang terintegrasi dengan Ubidots
- `/api/iot` untuk mengupload 3 jenis data, temperature, humidity, dan distance
- `/api/temp` untuk mengupload data temperature
- `/api/humidity` untuk mengupload data humidity
- `/api/distance` untuk mengupload data distance