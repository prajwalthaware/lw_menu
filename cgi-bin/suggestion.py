#!/usr/bin/env python3

import cgi
import json

def main():
    # Get the query parameter from the URL
    form = cgi.FieldStorage()
    query = form.getvalue('q', '')

    # Sample suggestions (you can replace it with your MongoDB query)
    suggestions = ["ls", "ls -l", "cd", "mkdir", "touch", "rm", "mv", "cp", "pwd",
                   "grep", "find", "cat", "echo", "chmod", "chown", "wget", "tar", "zip", "unzip"]

    # Filter suggestions based on the query (case-insensitive)
    filtered_suggestions = [s for s in suggestions if query.lower() in s.lower()]

    # Output JSON response
    print("Content-Type: application/json")
    print()
    print(json.dumps(filtered_suggestions))

if __name__ == "__main__":
    main()

