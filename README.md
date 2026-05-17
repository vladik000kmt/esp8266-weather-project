[README.txt](https://github.com/user-attachments/files/27874763/README.txt)
Project Description:
Weather Station with VK Bot Visualization
A system for collecting, storing, and displaying meteorological data (temperature, humidity, pressure, CO₂) using an ESP8266, a Flask server, and a VK bot.

Technologies:
ESP8266 (Arduino framework): C++, libraries: WiFiClientSecure, ArduinoJson, Adafruit AHTX0/BMP280, MQ135.
Flask server: Python 3, Flask, file system operations.
VK Bot: Python, vk_api library, Bot Long Poll, inline keyboards.

Launch Instructions:
Upload the code to the ESP8266, specify your Wi-Fi credentials and the server URL (you can use ngrok/tunnel).
Run the Flask server.
Run a tunneling service (xtunnel/ngrok).
Create a VK group, obtain a token with message permissions.
Run the VK bot, providing the token and group ID.

Note: The project was created for educational purposes to monitor indoor microclimate.
