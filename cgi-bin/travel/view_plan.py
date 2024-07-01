#!/usr/bin/env python3

import cgi
import cgitb
from utils import load_data

cgitb.enable()

print("Content-type: text/html\n")

data = load_data()

print("<html><body>")
print("<h2>Travel Itinerary</h2>")
print("<h3>Destinations</h3>")
print("<ul>")
for destination in data['destinations']:
    print(f"<li>{destination}</li>")
print("</ul>")
print("<h3>Activities</h3>")
print("<ul>")
for activity in data['activities']:
    print(f"<li>{activity}</li>")
print("</ul>")
print("<h3>Accommodations</h3>")
print("<ul>")
for accommodation in data['accommodations']:
    print(f"<li>{accommodation}</li>")
print("</ul>")
print("<a href='/html/travel/index.html'>Back to Home</a>")
print("</body></html>")

