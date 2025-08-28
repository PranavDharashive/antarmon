# AntarMon Agent

This is the agent for the AntarMon monitoring utility.

## Prerequisites

- Python 3.7+
- pip

## Installation

1.  Navigate to the `agent` directory:
    ```bash
    cd agent
    ```
2.  Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

1.  Before running the agent for the first time, you need to get an API key from the AntarMon web interface.
2.  Run the agent:
    ```bash
    python agent.py
    ```
3.  The agent will prompt you to enter the API key. Paste the key and press Enter.
4.  The agent will save the API key to a `config.ini` file in the same directory.

## Running the Agent as a Service (Linux)

To install and run the AntarMon agent as a systemd service on a Linux system, you can use the provided setup script.

1.  Navigate to the `agent` directory.
2.  Make the setup script executable:
    ```bash
    chmod +x setup_agent.sh
    ```
3.  Run the script with `sudo`:
    ```bash
    sudo ./setup_agent.sh
    ```

This will create a dedicated user, install the application in `/opt/antarmon-agent`, and set it up as a systemd service that starts on boot. The script will prompt you for the following information during installation:
-   The agent's API key (obtained from the web interface).
-   The IP address or domain name of the AntarMon server.
-   The path to the server's public certificate file (`antarmon.crt`).

### Managing the Service

-   **Check Status:** `systemctl status antarmon-agent`
-   **View Logs:** `journalctl -u antarmon-agent -f`
-   **Stop Service:** `sudo systemctl stop antarmon-agent`
-   **Start Service:** `sudo systemctl start antarmon-agent`

## Packaging with PyInstaller

To package the agent as a single executable file, you can use `PyInstaller`.

1.  Install PyInstaller:
    ```bash
    pip install pyinstaller
    ```
2.  Run PyInstaller to create the executable:
    ```bash
    pyinstaller --onefile agent.py
    ```
3.  The executable file will be located in the `dist` directory.
