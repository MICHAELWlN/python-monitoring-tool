import json
import os
from datetime import datetime, timezone

import requests


def load_config():
    """Load monitor settings from config.json."""
    with open("config.json", "r") as file:
        return json.load(file)

def validate_config(config):
    """Validate required config settings before the monitor runs."""
    required_keys = ["target_urls", "timeout_seconds", "max_retries"]
    missing_keys = []

    for key in required_keys:
        if key not in config:
            missing_keys.append(key)

    if missing_keys:
        raise ValueError("Missing required config settings: " + ", ".join(missing_keys))


def check_website(url, timeout):
    """Run one HTTP check and return one structured log entry."""
    try:
        response = requests.get(url, timeout=timeout)
        response_time_ms = response.elapsed.total_seconds() * 1000

        if response.status_code == 200:
            result = "healthy"
        else:
            result = "unhealthy"

        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "target": url,
            "status_code": response.status_code,
            "response_time_ms": response_time_ms,
            "result": result,
            "timeout_seconds": timeout,
            "error": None,
        }

        return log_entry

    except requests.RequestException as error:
        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "target": url,
            "status_code": None,
            "response_time_ms": None,
            "result": "failed",
            "timeout_seconds": timeout,
            "error": str(error),
        }

        return log_entry


def print_summary(entry):
    """Print one short human-readable summary for a final log entry."""
    if entry["alert"]:
        print("Checked", entry["target"], "-", entry["result"], "ALERT")
    else:
        print("Checked", entry["target"], "-", entry["result"])


def write_log(entry):
    """Append one structured JSON log entry to logs/monitor.log."""
    os.makedirs("logs", exist_ok=True)

    with open("logs/monitor.log", "a") as file:
        file.write(json.dumps(entry) + "\n")


def main():
    """Control the full monitoring run."""
    config = load_config()
    validate_config(config)

    timeout = config["timeout_seconds"]
    max_retries = config["max_retries"]

    total_checked = 0
    total_healthy = 0
    total_alert = 0

    for url in config["target_urls"]:
        for attempt in range(max_retries + 1):
            entry = check_website(url, timeout)

            if entry["result"] == "healthy":
                break

        entry["attempts"] = attempt + 1

        if entry["result"] == "healthy":
            entry["alert"] = False
            entry["alert_reason"] = None
        else:
            entry["alert"] = True
            entry["alert_reason"] = "non_healthy_after_retries"

        write_log(entry)
        print_summary(entry)

        total_checked += 1

        if entry["result"] == "healthy":
            total_healthy += 1

        if entry["alert"]:
            total_alert += 1

    print(
        "Summary:",
        total_checked,
        "checked |",
        total_alert,
        "alerts |",
        total_healthy,
        "healthy",
    )


if __name__ == "__main__":
    main()
