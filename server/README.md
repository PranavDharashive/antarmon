# AntarMon Server

This is the backend server for the AntarMon monitoring utility.

## Prerequisites

- Python 3.7+
- pip

## Installation

1.  Clone the repository.
2.  Navigate to the `server` directory:
    ```bash
    cd server
    ```
3.  Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

## Running the Server as a Service (Linux)

To install and run the AntarMon server as a systemd service on a Linux system, you can use the provided setup script.

1.  Navigate to the `server` directory.
2.  Make the setup script executable:
    ```bash
    chmod +x setup_server.sh
    ```
3.  Run the script with `sudo`:
    ```bash
    sudo ./setup_server.sh
    ```

This will create a dedicated user, install the application in `/opt/antarmon-server`, generate a self-signed SSL certificate, and set it up as a systemd service that starts on boot.

### Certificate Files

The setup script will generate the following files in the installation directory (`/opt/antarmon-server`):
-   `antarmon.key`: The private key for the server.
-   `antarmon.crt`: The public certificate. This file needs to be copied to any machine where an agent will be installed.

### Managing the Service

-   **Check Status:** `systemctl status antarmon-server`
-   **View Logs:** `journalctl -u antarmon-server -f`
-   **Stop Service:** `sudo systemctl stop antarmon-server`
-   **Start Service:** `sudo systemctl start antarmon-server`

## Authentication

The server uses JWT-based authentication.

### User Registration

-   Register a new user by sending a `POST` request to the `/register` endpoint with a JSON body containing `email` and `password`.

### Login

-   Log in by sending a `POST` request to the `/token` endpoint with a form-data body containing `username` (which is the email) and `password`.
-   The server will respond with an `access_token`.

## Agent Registration

-   To register a new agent, send a `POST` request to the `/agents` endpoint with a JSON body containing the agent's `name`.
-   This endpoint is protected and requires a valid JWT token.
-   The server will respond with an `api_key` for the agent.

## Metrics

-   The server receives metrics from agents via a `POST` request to the `/metrics` endpoint.
-   This endpoint is protected and requires a valid API key in the `X-API-Key` header.

## Alerts

-   The server can be configured to trigger alerts when metrics exceed certain thresholds.
-   Alerts can be managed via the `/alerts` endpoints.
