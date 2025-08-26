import psutil
import requests
import time
import os

SERVER_URL = "http://127.0.0.1:8000/metrics"

def get_metrics():
    cpu_percent = psutil.cpu_percent(interval=1)
    memory_info = psutil.virtual_memory()
    disk_info = psutil.disk_usage('/')

    return {
        "cpu_percent": cpu_percent,
        "memory_percent": memory_info.percent,
        "disk_percent": disk_info.percent,
        "hostname": os.uname().nodename
    }

def main():
    while True:
        metrics = get_metrics()
        try:
            response = requests.post(SERVER_URL, json={"metrics": metrics})
            response.raise_for_status()
            print(f"Successfully sent metrics: {metrics}")
        except requests.exceptions.RequestException as e:
            print(f"Failed to send metrics: {e}")
        
        time.sleep(10)

if __name__ == "__main__":
    main()
