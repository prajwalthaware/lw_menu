#!/usr/bin/env python3

import cgi
import cgitb
import json
import pywhatkit as kit
import sys

cgitb.enable()

def send_instant(phone_number, message):
    try:
        kit.sendwhatmsg_instantly(phone_number, message)
        return json.dumps({'status': 'Message sent instantly'})
    except Exception as e:
        return json.dumps({'error': str(e)})

def send_scheduled(phone_number, message, hour, minute):
    try:
        kit.sendwhatmsg(phone_number, message, hour, minute)
        return json.dumps({'status': 'Message scheduled'})
    except Exception as e:
        return json.dumps({'error': str(e)})

def main():
    print("Content-Type: application/json")
    print()

    form = cgi.FieldStorage()
    action = form.getvalue('action')
    phone_number = form.getvalue('phone_number')
    message = form.getvalue('message')

    if action == 'instant':
        if not phone_number or not message:
            print(json.dumps({'error': 'Phone number and message are required'}))
            return
        print(send_instant(phone_number, message))

    elif action == 'scheduled':
        hour = form.getvalue('hour')
        minute = form.getvalue('minute')
        if not phone_number or not message or hour is None or minute is None:
            print(json.dumps({'error': 'Phone number, message, hour, and minute are required'}))
            return
        print(send_scheduled(phone_number, message, int(hour), int(minute)))

if __name__ == '__main__':
    main()

