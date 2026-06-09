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

Added timing, result labels, and retry attempts

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

Retry behavior:
- healthy stops retryign early
- unhealthy/failed retry until max_retries is used

Important distinction:
- response_time = how long the website took to respond
- timeout_seconds = max time the tool will wait before giving up
- check_website() handles one check
- main() handles retries and adds attempts

Day 4 result:
- logs now show website health, response speed, tool now performs basic retries

# Day 5 Notes

Added alert logic and a final run summary.

New fields:
- alert = true/false decision after retries
- alert_reason = reason for alert, or null

Alert behavior:
- healthy = no alert
- unhealthy/failed = alert after retries
- terminal shows ALERT when alert is true

Run summary:
- total_checked = number of URLs checked
- total_alert = number of alerting results
- total_healthy = number of healthy results

Important distinction:
- print_summary() prints one URL result
- main() tracks totals across the full run
- counters must start before the URL loop so they do not reset

Day 5 result:
- each URL gets alert fields in the log
- terminal shows per-URL status plus final totals

# Python Monitoring Tool Notes

## Project Goal

Build a Linux-friendly Python monitoring tool that checks website health, retries non-healthy results, writes structured JSON logs, and prints readable terminal summaries.

## Current Features

- Loads settings from `config.json`
- Checks multiple target URLs
- Uses `timeout_seconds` to avoid hanging requests
- Tracks `healthy`, `unhealthy`, and `failed` results
- Measures `response_time_ms`
- Retries unhealthy/failed checks with `max_retries`
- Adds `attempts`, `alert`, and `alert_reason` to the final log entry
- Writes JSON lines to `logs/monitor.log`
- Auto-creates the `logs/` folder if missing
- Prints one summary per URL plus a final run summary

## Core Flow

`main()`:
- Loads config
- Validates required settings
- Gets `timeout_seconds` and `max_retries`
- Loops through `target_urls`
- Retries each URL until healthy or retries run out
- Adds `attempts`, `alert`, and `alert_reason`
- Writes the final log entry
- Prints per-URL and final summaries

`check_website(url, timeout)`:
- Performs one HTTP check
- Returns one structured log entry
- Does not handle retry counting

`write_log(entry)`:
- Makes sure `logs/` exists
- Appends one JSON log line to `logs/monitor.log`

`print_summary(entry)`:
- Prints one short readable result for a single URL

## Result Types

- `healthy` = website responded with HTTP 200
- `unhealthy` = website responded, but not with HTTP 200
- `failed` = request broke before getting a valid response

## Important Log Fields

- `target` = website being checked
- `status_code` = HTTP status code, or `null` if failed
- `response_time_ms` = how long the website took to respond
- `timeout_seconds` = max time the tool was willing to wait
- `result` = `healthy`, `unhealthy`, or `failed`
- `attempts` = how many tries were used
- `alert` = true if final result needs attention
- `alert_reason` = why alert triggered, or `null`
- `error` = request failure message, or `null`

## Retry Logic

- `max_retries` means extra tries after the first attempt
- Total possible attempts = `max_retries + 1`
- Healthy results stop retrying early
- Unhealthy/failed results retry until `max_retries` is used
- `attempts` is added in `main()` because `main()` owns the retry loop

## Alert Logic

- Healthy = `alert: false`
- Unhealthy = `alert: true`
- Failed = `alert: true`
- Alert is decided after retries finish
- `alert_reason` is `non_healthy_after_retries` for unhealthy/failed results

## Config Validation

`validate_config()` checks that required settings exist before the monitor runs.

Required config keys:
- `target_urls`
- `timeout_seconds`
- `max_retries`

This prevents unclear errors later in the program.

## Linux-First Notes

- `os.makedirs("logs", exist_ok=True)` makes the tool safer on a fresh Linux machine
- `tail -f logs/monitor.log` watches logs live
- `grep '"alert": true' logs/monitor.log` filters alerting checks
- `grep '"result": "failed"' logs/monitor.log` filters failed checks

## Final Project Value

This project demonstrates:
- Python scripting
- Config-driven automation
- HTTP health checks
- Structured JSON logging
- Retry logic
- Alert decision logic
- Basic config validation
- Linux-style log inspection
- Clean operational thinking