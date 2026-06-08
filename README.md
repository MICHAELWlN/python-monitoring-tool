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

## Day 4 Goal

Add response_time_ms to every log entry
Polish response time tracking
Polish log fields and simplify result handling
Add basic retry tracking

The tool already calculates response time for successful and unhealthy checks. Day 4 should clean this up by making the log field name clear, testing all result types, retry unhealthy or failed checks before writing the final log entry, and keeping the terminal output simple

Required work:
- Rename 'response_time' to 'response_time_ms'
- Keep successful/unhealthy checks logging a real response time
- Keep failed checks logging 'response_time_ms: null'
- Test healthy, unhealthy, and failed URLs
- Confirm logs/monitor.log gets one JSON line per website
- Add a 'result' field with one of three values: 'healthy', 'unhealthy', or 'failed'
- Retry unhealthy or failed checks up to 'max_retries'
- Stop retrying early if a check becomes 'healthy'
- Add 'attempts' to the final log entry
- Update notes.md with a short Day 4 section

Done when:
- Each log entry clearly shows website health, response speed, result, and timeout setting
- Terminal output stays short: 'Checked <url> - <result>'
- Unhealthy or failed checks log the total attempts used
- Changes are committed and pushed to GitHub

## Day 5 Goal

Add basic alert logic after retries

The tool already retries unhealthy or failed checks. Day 5 should add a simple alert decision after all attempts are finished, so the final log entry clearly shows whether the result should trigger attention

Required work:
- Add an 'alert' field to the final log entry
- Set 'alert' to 'false' when result is 'healthy'
- Set 'alert' to 'true' when result is 'unhealthy' or 'failed' after retries are used
- Add an 'alert_reason' field with a short reason such as 'non_healthy_after_retries'
- Keep terminal output short, but include alert status when needed
- Test healthy, unhealthy, and failed URLs
- Update notes.md with a short Day 5 section

Done when:
- Healthy checks log 'alert: false'
- Unhealthy or failed checks log 'alert: true'
- logs/monitor.log shows 'result', 'attempts', 'alert' and 'alert_reason'
- Terminal output stays readable
- Changes are committed and pushed to GitHub

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
