# Python Monitoring and Troubleshooting Tool

A Linux-friendly Python monitoring tool that checks website health, retries non-healthy results, writes structured JSON logs, and prints readable terminal summaries.

## Features

- Loads monitor settings from `config.json`
- Validates required config settings before running
- Checks multiple target URLs
- Uses `timeout_seconds` to prevent hanging requests
- Measures response time in milliseconds
- Classifies results as `healthy`, `unhealthy`, or `failed`
- Retries unhealthy/failed checks with `max_retries`
- Adds `attempts`, `alert`, and `alert_reason` to final log entries
- Writes JSON lines to `logs/monitor.log`
- Auto-creates the `logs/` folder if missing
- Prints one summary per URL plus a final run summary

## Project Structure

```text
python-monitoring-tool/
├── config.json
├── monitor.py
├── notes.md
├── requirements.txt
├── README.md
└── logs/
    └── .gitkeep
```

Runtime log files are ignored by Git.

## Example Config

```json
{
  "target_urls": [
    "https://example.com",
    "https://httpbin.org/status/500",
    "https://fake-website-that-does-not-exist12345.com"
  ],
  "timeout_seconds": 10,
  "max_retries": 2
}
```

## Run

Create and activate a virtual environment:

```zsh
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```zsh
pip install -r requirements.txt
```

Run the monitor:

```zsh
python3 monitor.py
```

## Example Terminal Output

```text
Checked https://example.com - healthy
Checked https://httpbin.org/status/500 - unhealthy ALERT
Checked https://fake-website-that-does-not-exist12345.com - failed ALERT
Summary: 3 checked | 2 alerts | 1 healthy
```

## Log Output

Each run appends one JSON object per website to:

```text
logs/monitor.log
```

Example log entry:

```json
{
  "timestamp": "2026-06-09T06:30:00.000000+00:00",
  "target": "https://example.com",
  "status_code": 200,
  "response_time_ms": 123.45,
  "result": "healthy",
  "timeout_seconds": 10,
  "error": null,
  "attempts": 1,
  "alert": false,
  "alert_reason": null
}
```

## Result Types

- `healthy` = website responded with HTTP 200
- `unhealthy` = website responded, but not with HTTP 200
- `failed` = request broke before getting a valid response

## Alert Behavior

- Healthy checks do not alert
- Unhealthy or failed checks alert after retries finish
- Alerting results include `alert: true`
- Non-alerting results include `alert: false`

## Linux Run / Debug Commands

Watch logs live:

```zsh
tail -f logs/monitor.log
```

Show alerting checks:

```zsh
grep '"alert": true' logs/monitor.log
```

Show failed checks:

```zsh
grep '"result": "failed"' logs/monitor.log
```

Check the config file:

```zsh
cat config.json
```

Delete logs and verify they auto-create:

```zsh
rm -rf logs
python3 monitor.py
ls logs
tail -n 3 logs/monitor.log
```

## What This Project Demonstrates

- Python scripting
- Config-driven automation
- HTTP health checks
- Structured JSON logging
- Retry logic
- Alert decision logic
- Basic config validation
- Linux-style log inspection
- Operational troubleshooting workflow