#!/usr/bin/env python3

import cgi
import cgitb
from utils import load_data, save_data

cgitb.enable()

print("Content-type: text/html\n")

form = cgi.FieldStorage()
activity = form.getvalue("activity")

data = load_data()
data['activities'].append(activity)
save_data(data)

print("<html><body>")
print("<h2>Activity Added!</h2>")
print("<a href='/html/travel/index.html'>Back to Home</a>")
print("</body></html>")

