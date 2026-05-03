# Python Monitoring and Troubleshooting Tool

This is an in-progress Python tool for checking basic website/service health.

Current features:
- Loads target settings from config.json
- Checks a URL using HTTP
- Reports status code
- Handles request errors with try/except

Planned features:
- Structured JSON logging
- Repeated failure detection
- Alert cooldown logic
- Multiple targets
- Troubleshooting output

# Day 1 Understanding

This tool checks one website using settings from config.json.

config.json stores:
- target_url
- timeout_seconds

import json:
- lets Python read JSON data

import requests:
- lets Python send HTTP requests to websites

load_config():
- opens config.json
- converts the JSON data into a Python dictionary
- returns that dictionary

main():
- controls the program flow
- loads the config
- passes the URL and timeout into check_website()

check_website(url, timeout):
- sends a GET request to the URL
- waits up to timeout seconds
- prints the URL and status code
- prints healthy if status code is 200
- prints unhealthy if status code is not 200
- prints failed if the request breaks

Important distinction:
- healthy = website responded with 200
- unhealthy = website responded, but not with 200
- failed = the request itself failed

try/except:
- try runs code that might fail
- except catches request errors so the program does not crash

# Day 2 Notes

Structured logging means saving results in a consistent format instead of only printing text.

Each check creates a dictionary with:
- timestamp
- target URL
- status code
- healthy true/false
- error message or null

json.dumps() converts a Python dictionary into JSON text.

Opening a file with "a" means append mode.
Append mode adds a new line without deleting the old logs.

JSON lines means each log entry is one JSON object on its own line.

