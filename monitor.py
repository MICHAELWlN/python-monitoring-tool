import json

import requests


def load_config():
    with open("config.json", "r") as file:
        return json.load(file)


def check_website(url, timeout):
    try:
        response = requests.get(url, timeout=timeout)
        print("URL:", url)
        print("Status code:", response.status_code)

        if response.status_code == 200:
            print("Result: healthy")
        else:
            print("Result: unhealthy")

    except requests.RequestException as error:
        print("Result: failed")
        print("Error:", error)


def main():
    config = load_config()
    check_website(config["target_url"], config["timeout_seconds"])


if __name__ == "__main__":
    main()
