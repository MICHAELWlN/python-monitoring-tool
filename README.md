# Python Monitoring and Troubleshooting Tool

This is an in-progress Python tool for checking basic website/service health.

## Day 1 Goal

Create the repository and make the first working HTTP check.

## Day 2 Goal

Add structured JSON logging so each website check is saved to a log file.

Current features:
- Loads target settings from config.json
- Checks a URL using HTTP
- Reports status code
- Handles request errors with try/except
- Writes each check result as JSON to logs/monitor.log
- Logs timestamp, target URL, status code, health result, and errors

Planned features:
- Repeated failure detection
- Alert cooldown logic
- Multiple targets
- Troubleshooting output

## Day 3 Goal

Support multiple target URLs from config.json

The tool currently checks one URL per run. Day 3 should upgrade the config so it can store a list of target URLs, then use a 'for' loop in 'main()' to check each target, write each result to 'logs/monitor.log', and print a short summary for each check.


## Run

```zsh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python monitor.py
```

## Logs

Each run appends one JSON object to:

```text
logs/monitor.log
```
