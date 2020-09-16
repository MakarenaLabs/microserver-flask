from flask import Flask, request, jsonify
import json
import time
from modbusmaster_module import modbus_master_relay as modbus_relay
from FPGABitstream import FPGABitstream
import sys
import logging

app = Flask(__name__)

handler = logging.StreamHandler(sys.stdout)  # Create the file logger
app.logger.addHandler(handler)             # Add it to the built-in logger
app.logger.setLevel(logging.DEBUG)         # Set the log level to debug

data = {}

with open('config.json', 'r') as conf:
	config = json.load(conf)

if 'microzed' in config['bitstream']:
	from xnucleo_pl_module.main import getSensorsOneShot as gsos
	app.logger.debug("microzed config")
else:
	from xnucleo_module.main import getSensorsOneShot as gsos
	app.logger.debug("ultra96 config")

fpga = FPGABitstream(config['bitstream'])

modbus_relay.init_all(uart_address=int(config['addresses']['uart'], 16), gpio_address=int(config['addresses']['gpio'], 16))

@app.route('/devices', methods = ['GET', 'POST'])
def manage_devices():
	global data
	if request.method == 'GET':

		if 'microzed' in config['bitstream']:
			print("ready")
			ss = gsos(fpga.i2c)
			print(ss)
			data = json.loads(ss)
		else:
			data = json.loads(gsos(3))
			
		with open('./data.json', 'r') as json_file:
			jsone = json.load(json_file)
			data["relay1"] = jsone["relays"]["relay1"]
			data["relay2"] = jsone["relays"]["relay2"]
			data["relay3"] = jsone["relays"]["relay3"]
			data["relay4"] = jsone["relays"]["relay4"]
			data["frequency"] = jsone["config"]["frequency"]
			data["updated"] = jsone["config"]["updated"]
		response = app.response_class(
			response=json.dumps(data),
			status=200,
			mimetype='application/json'
		)
		return response


	if request.method == 'POST':
		temp_data = request.get_json(force=True)
		print("TEMP_DATA")
		print(temp_data)
		if 'updated' in temp_data.keys():
			data['updated'] = temp_data['updated']
		if 'frequency' in temp_data.keys():
			data['frequency'] = temp_data['frequency']
		if 'hum' in temp_data.keys():
			data['hum'] = temp_data['hum']
		if 'temp1' in temp_data.keys():
			data['temp1'] = temp_data['temp1']
		if 'pressure' in temp_data.keys():
			data['pressure'] = temp_data['pressure']
		if 'temp2' in temp_data.keys():
			data['temp2'] = temp_data['temp2']
		if 'accel1' in temp_data.keys():
			data['accel1'] = temp_data['accel1']
		if 'Gaxis' in temp_data.keys():
			data['Gaxis'] = temp_data['Gaxis']
		if 'accel2' in temp_data.keys():
			data['accel2'] = temp_data['accel2']
		if 'magneto' in temp_data.keys():
			data['magneto'] = temp_data['magneto']
		if 'relay1' in temp_data.keys():
			data['relay1'] = temp_data['relay1']
			modbus_relay.set_relay_function(0, 1 if data['relay1'] else 0)
			time.sleep(0.05)
		if 'relay2' in temp_data.keys():
			data['relay2'] = temp_data['relay2']
			modbus_relay.set_relay_function(1, 1 if data['relay2'] else 0)
			time.sleep(0.05)
		if 'relay3' in temp_data.keys():
			data['relay3'] = temp_data['relay3']
			modbus_relay.set_relay_function(2, 1 if data['relay3'] else 0)
			time.sleep(0.05)
		if 'relay4' in temp_data.keys():
			data['relay4'] = temp_data['relay4']
			modbus_relay.set_relay_function(3, 1 if data['relay4'] else 0)
			time.sleep(0.05)

		print(data)

		data_json = {}

		data_json["config"] = {}
		data_json["sensors"] = {}
		data_json["relays"] = {}

		data_json["config"]["frequency"] = data["frequency"]
		data_json["config"]["updated"] = data["updated"]
		data_json["sensors"]['hum'] = data['hum']
		data_json["sensors"]['temp1'] = data['temp1']
		data_json["sensors"]['pressure'] = data['pressure']
		data_json["sensors"]['temp2'] = data['temp2']
		data_json["sensors"]['accel1'] = data['accel1']
		data_json["sensors"]['Gaxis'] = data['Gaxis']
		data_json["sensors"]['accel2'] = data['accel2']
		data_json["sensors"]['magneto'] = data['magneto']
		data_json["relays"]['relay1'] = data['relay1']
		data_json["relays"]['relay2'] = data['relay2']
		data_json["relays"]['relay3'] = data['relay3']
		data_json["relays"]['relay4'] = data['relay4']

		with open('./data.json', 'w') as json_file:
			json.dump(data_json, json_file)
		return ""


#app.run(host="0.0.0.0")
