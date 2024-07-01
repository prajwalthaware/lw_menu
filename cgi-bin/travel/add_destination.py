#!/usr/bin/env python3

import cgi
import cgitb
from utils import load_data, save_data

cgitb.enable()

print("Content-type: text/html\n")

form = cgi.FieldStorage()
destination = form.getvalue("destination")

data = load_data()
data['destinations'].append(destination)
save_data(data)

print("<html><body>")
print("<h2>Destination Added!</h2>")
print("<a href='/html/travel/index.html'>Back to Home</a>")
print("</body></html>")

