import json #Lets python read JSON file
import requests #Allows get requests to be made
from datetime import datetime, timezone


def load_config(): #Reads config settings
    with open("config.json", "r") as file: #Opens config.json in read mode
        return json.load(file) #Returns config settings

def check_website(url, timeout): #Defines website check, allowed by main function
    try: #Attempts get request, checks website health with max timeout of 5 sec
        response = requests.get(url, timeout=timeout) 
        response_seconds = response.elapsed.total_seconds() * 1000 #Log time in ms

        if response.status_code==200: #If response returns status code = 200 = healthy, if not = unhealthy

            result = "healthy"
        
        else:

            result = "unhealthy"

        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "target": url,
            "status_code": response.status_code,
            "response_time": response_seconds,
            "result": result,
            "timeout_seconds": timeout,
            "error": None
        }

        return log_entry

    except requests.RequestException as error: #Case of failure

        result = "failed" #Variable for clean log entry use

        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "target": url,
            "status_code": None,
            "response_time": None,
            "result": result,
            "timeout_seconds": timeout,
            "error": str(error)
        }
    
        return log_entry
    
def print_summary(entry):

    print("Checked", entry["target"], "-", entry["result"])

def write_log(entry):
    with open("logs/monitor.log", "a") as file:
        file.write(json.dumps(entry) + "\n")




def main(): #controls program flow
    config = load_config() #Allows config to be read
#Pull values from check website function + store in entry
    timeout = config["timeout_seconds"]
    for url in config["target_urls"]:
        entry = check_website(url,timeout)
        write_log(entry)
        print_summary(entry)

if __name__ == "__main__": #Run main function only if this specific file is executed
    main()
