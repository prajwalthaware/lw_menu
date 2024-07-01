#!/usr/bin/env python3

import cgi
import subprocess
import cgitb
import json

# Enable detailed error messages for CGI scripts
cgitb.enable()

# Function to speak the provided text using espeak-ng
def speak_text(text):
    try:
        # Execute the espeak-ng command to speak the text
        result = subprocess.check_output(["/usr/local/bin/espeak-ng", text], stderr=subprocess.STDOUT, text=True)
        return {"status": "success", "message": "Text spoken successfully."}
    except subprocess.CalledProcessError as e:
        # Return the error message if the command fails
        return {"status": "error", "message": str(e)}

# Parse form data sent via POST request
form = cgi.FieldStorage()

# Extract the value of the "text" field from the form data
text = form.getvalue("text")

# Initialize the output variable
output = {}

# Check if text is provided
if text:
    # Call the speak_text function with the provided text
    output = speak_text(text)
else:
    output = {"status": "error", "message": "No text provided."}

# Print the HTTP header with the content type
print("Content-Type: application/json\n")

# Output the JSON response
print(json.dumps(output))

