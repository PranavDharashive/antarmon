import psutil
import requests
import time
import os
import configparser

SERVER_URL = "https://127.0.0.1:8000/metrics"
CONFIG_FILE = "config.ini"
CERT_FILE = "antarmon.crt"

def get_config():
    config = configparser.ConfigParser()
    if not os.path.exists(CONFIG_FILE):
        api_key = input("Please enter your API key: ")
        server_ip = input("Please enter your server IP or domain: ")
        cert_path = input("Please enter the path to the server certificate (antarmon.crt): ")
        
        config['DEFAULT'] = {
            'API_KEY': api_key,
            'SERVER_IP': server_ip
        }
        with open(CONFIG_FILE, 'w') as configfile:
            config.write(configfile)
        
        # Copy the certificate
        import shutil
        shutil.copy(cert_path, CERT_FILE)

    config.read(CONFIG_FILE)
    return config['DEFAULT']

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
    config = get_config()
    api_key = config['API_KEY']
    server_ip = config['SERVER_IP']
    server_url = f"https://{server_ip}:8000/metrics"
    headers = {"X-API-Key": api_key}

    while True:
        metrics = get_metrics()
        try:
            response = requests.post(server_url, json={"metrics": metrics}, headers=headers, verify=CERT_FILE)
            response.raise_for_status()
            print(f"Successfully sent metrics: {metrics}")
        except requests.exceptions.RequestException as e:
            print(f"Failed to send metrics: {e}")
        
        time.sleep(10)

if __name__ == "__main__":
    main()
