# Python Monitoring Tool Notes

## Project Goal

Build a Linux-friendly Python monitoring tool that checks website health, retries non-healthy results, writes structured JSON logs, and prints readable terminal summaries.

## Current Features

- Loads settings from `config.json`
- Validates required config settings before running
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
- Prints per-URL summaries and a final run summary

`check_website(url, timeout)`:
- Performs one HTTP check
- Returns one structured log entry
- Does not handle retry counting or alert decisions

`write_log(entry)`:
- Makes sure `logs/` exists
- Appends one JSON log line to `logs/monitor.log`

`print_summary(entry)`:
- Prints one short readable result for a single URL

`validate_config(config)`:
- Checks required config keys before the monitor runs
- Raises a readable error if required settings are missing

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

## Final Run Summary

The tool tracks totals across the full run:
- `total_checked` = number of URLs checked
- `total_alert` = number of alerting results
- `total_healthy` = number of healthy results

Counters start before the URL loop so they do not reset for each URL.

## Config Validation

Required config keys:
- `target_urls`
- `timeout_seconds`
- `max_retries`

Validation prevents unclear errors later in the program.

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