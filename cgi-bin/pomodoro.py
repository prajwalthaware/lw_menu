#!/usr/bin/env python3

import cgi
import cgitb
import json
import os

cgitb.enable()

DATA_FILE = "/tmp/pomodoro_data.json"

def read_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    return {"state": "stopped", "minutes": 25, "seconds": 0}

def write_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file)

def start_timer():
    data = read_data()
    if data["state"] == "stopped":
        data["state"] = "running"
        data["minutes"] = 25
        data["seconds"] = 0
        write_data(data)
    return data

def stop_timer():
    data = read_data()
    if data["state"] == "running":
        data["state"] = "stopped"
        write_data(data)
    return data

def reset_timer():
    data = {"state": "stopped", "minutes": 25, "seconds": 0}
    write_data(data)
    return data

def get_timer():
    return read_data()

form = cgi.FieldStorage()
action = form.getvalue("action")

if action == "start":
    data = start_timer()
elif action == "stop":
    data = stop_timer()
elif action == "reset":
    data = reset_timer()
else:
    data = get_timer()

print("Content-Type: application/json")
print()
print(json.dumps(data))

