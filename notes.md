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

# Day 3 Notes

Upgraded the tool from checking one website to checking multiple websites.

config.json now stores:
- target_urls = list of websites
- timeout_seconds = max wait time for each check

Python list:
- stores multiple values together
- target_urls is a list of website strings

for loop:
- repeats the same code for each URL
- for url in config["target_urls"] gives one URL at a time

main():
- loads config
- gets timeout_seconds
- loops through target_urls
- checks one url
- writes each entry to logs/monitor.log
- prints a summary for each URL

Important distinction:
- config["target_urls"] = the whole list
- url = one website during the current loop

Day 3 result:
- one run checks multiple websiteds
- each website creates one JSON log line
- terminal shows one summary per website

# Day 4 Notes

Added response time tracking to each website check.

response.elapsed:
- comes from the requests response object
- shows how long the HTTP request took

response.elapsed.total_seconds():
- runs the total_seconds method
- converts the elapsed time into seconds as a number

response_time:
- stores response time in milliseconds
- calculated with response.elapsed.total_seconds() * 1000
- added to each log entry

Successful/unhealthy checks:
- have a real status_code
- have a real response_time
- error is null

Failed checks:
- status_code is null
- response_time is null
- error stores the failure message

Important distinction:
- response_time = how long the website took to respond
- timeout_seconds = max time the tool will wait before giving up

Day 4 result:
- logs now show website health and response speed
