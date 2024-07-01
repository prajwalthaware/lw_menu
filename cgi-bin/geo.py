#!/usr/bin/env python3

import cgi
import cgitb
import json
from geopy.geocoders import Nominatim

# Enable CGI traceback for debugging
cgitb.enable()

# Print necessary headers
print("Content-Type: application/json\n")

# Parse the query parameters
form = cgi.FieldStorage()
location_name = form.getvalue("location")
my_location_name = form.getvalue("my_location")

# Function to get coordinates
def get_coordinates(location_name):
    geolocator = Nominatim(user_agent="my_geocoder")
    location = geolocator.geocode(location_name)
    if location:
        return {"latitude": location.latitude, "longitude": location.longitude}
    else:
        return {"error": "Location not found"}

# Get coordinates for the provided locations
location_coords = get_coordinates(location_name)
my_location_coords = get_coordinates(my_location_name)

# Generate Google Maps route URL
if "error" not in location_coords and "error" not in my_location_coords:
    google_maps_url = (
        f"https://www.google.com/maps/dir/?api=1"
        f"&origin={my_location_coords['latitude']},{my_location_coords['longitude']}"
        f"&destination={location_coords['latitude']},{location_coords['longitude']}"
    )
    result = {
        "location_coordinates": location_coords,
        "my_location_coordinates": my_location_coords,
        "google_maps_url": google_maps_url
    }
else:
    result = {
        "location_coordinates": location_coords,
        "my_location_coordinates": my_location_coords
    }

# Output the result as JSON
print(json.dumps(result))

