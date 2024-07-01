#!/usr/bin/env python3

import cgi
import base64
import os

# Ensure proper headers are sent to the browser
print("Content-Type: text/html\n")

# Retrieve the photo data
form = cgi.FieldStorage()
photo_data = form.getvalue('photoData')

if photo_data:
    # Decode the base64 image data
    photo_data = photo_data.split(",")[1]
    photo_data = base64.b64decode(photo_data)

    # Define the path to save the photo
    save_path = "/var/www/cgi-bin/photo.png"

    # Save the image
    with open(save_path, "wb") as f:
        f.write(photo_data)

    print("<html><body><h1>Photo Saved!</h1></body></html>")
else:
    print("<html><body><h1>Error: No photo data received!</h1></body></html>")

