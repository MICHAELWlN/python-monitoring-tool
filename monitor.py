import json #Lets python read JSON file
import requests #Allows get requests to be made
from datetime import datetime, timezone


def load_config(): #Reads config settings
    with open("config.json", "r") as file: #Opens config.json in read mode
        return json.load(file) #Returns config settings


def check_website(url, timeout): #Defines website check, allowed by main function
    try: #Attempts get request, checks website health with max timeout of 5 sec
        response = requests.get(url, timeout=timeout) 
        healthy = response.status_code == 200
        print("Status code:", response.status_code) 
        if healthy: #If response returns status code = 200 = healthy
            print("Result: healthy")
        else:
            print("Result: unhealthy")

        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "target": url,
            "status_code": response.status_code,
            "healthy": healthy,
            "error": None
        }

    except requests.RequestException as error: #If get request process fails, outputs as failed + error state
        print("Result: failed")
        print("Error:", error)

        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "target": url,
            "status_code": None,
            "healthy": False,
            "error": str(error)
        }
    
    write_log(log_entry)

def write_log(entry):
    with open("logs/monitor.log", "a") as file:
        file.write(json.dumps(entry) + "\n")




def main(): #controls program flow
    config = load_config() #Allows config to be read
    check_website(config["target_url"], config["timeout_seconds"]) #Allows website to be checked with max timeout of 5 sec


if __name__ == "__main__": #Run main function only if this specific file is executed
    main()
