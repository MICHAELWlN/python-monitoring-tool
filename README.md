# Python Monitoring and Troubleshooting Tool

This is an in-progress Python tool for checking basic website/service health.

## Day 1 Goal

Create the repository and make the first working HTTP check.

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

## Run

```zsh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python monitor.py
```
