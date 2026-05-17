from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

@app.route('/api/temperature', methods=['POST'])
def receive_data():
    try:
        data = request.get_json()

        if not data:
            return "No data", 400

        temperature = data.get('temperature')
        temperature = round(temperature, 1)
        humidity = data.get('humidity')
        humidity = round(humidity, 1)
        pressure = data.get('pressure')
        pressure = round(pressure, 1)
        co2 = data.get('co2')
        co2 = round(co2, 1)
        device_id = data.get('device_id', 'unknown')

        now_time = datetime.now().strftime('%H:%M:%S')

        try:
            with open(f'{device_id}.txt', 'r', encoding='utf-8') as f:
                quantity = f.readline().strip()
                right_time = f.readline().strip()
                temperature_list = list(map(float, f.readline().split()))
                humidity_list = list(map(float, f.readline().split()))
                pressure_list = list(map(float, f.readline().split()))
                carbon_dioxide_list = list(map(float, f.readline().split()))
        except:
            quantity = "0"
            right_time = "0"
            temperature_list = []
            humidity_list = []
            pressure_list = []
            carbon_dioxide_list = []

        try:
            quantity_num = int(quantity) if quantity else 0
            if quantity_num < 10:
                quantity_num += 1
                quantity = str(quantity_num)
            elif quantity_num >= 10:
                quantity = "10"
        except ValueError:
            quantity = "1"

        temperature_list.append(temperature)
        humidity_list.append(humidity)
        pressure_list.append(pressure)
        carbon_dioxide_list.append(co2)

        if len(temperature_list) > 10:
            temperature_list = temperature_list[-10:]
        if len(humidity_list) > 10:
            humidity_list = humidity_list[-10:]
        if len(pressure_list) > 10:
            pressure_list = pressure_list[-10:]
        if len(carbon_dioxide_list) > 10:
            carbon_dioxide_list = carbon_dioxide_list[-10:]

        with open(f'{device_id}.txt', 'w', encoding='utf-8') as f:
            f.write(quantity + '\n')
            f.write(now_time + '\n')
            f.write(' '.join(map(str, temperature_list)) + '\n')
            f.write(' '.join(map(str, humidity_list)) + '\n')
            f.write(' '.join(map(str, pressure_list)) + '\n')
            f.write(' '.join(map(str, carbon_dioxide_list)) + '\n')

        return jsonify({"status": "ok", "message": "Data received"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)