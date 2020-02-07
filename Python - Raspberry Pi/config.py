import json

with open('config.json') as file:
    config = json.load(file)

name = config["name"]
iot_endpoint = config["iot_endpoint"]
MAC = config["MAC"]

if "<" in name or "<" in iot_endpoint or "<" in MAC:
    raise Exception("Configure all fields in config.json")
