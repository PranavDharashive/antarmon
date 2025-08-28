# AntarMon - VM Monitoring Utility

AntarMon (Antar = Insight, Mon = Monitor) is a lightweight, cross-platform monitoring utility built with an agent–server architecture. It is designed to provide deep insights into VM/system health while being easy to install, secure by default, and minimal in resource usage.

## One-Command Installation

For a more streamlined setup, you can use the provided release and installation scripts.

### 1. Create the Release Packages

First, run the `create_release.sh` script to bundle the server and agent into distributable packages.

```bash
chmod +x create_release.sh
./create_release.sh
```

This will create `antarmon-server.tar.gz` and `antarmon-agent.tar.gz` in a `release` directory.

### 2. Host the Release Packages

Upload the `.tar.gz` files to a location where your target machines can access them via a URL (e.g., a web server, GitHub Releases).

### 3. Update the Installer Scripts

Edit the `RELEASE_URL` variable in `install_server.sh` and `install_agent.sh` to point to the public URLs of your hosted packages.

### 4. Run the Installer

On your target server or agent machine, you can now run the installation with a single command.

**For the server:**
```bash
curl -sL https://your-url.com/install_server.sh | sudo bash
```

**For the agent:**
```bash
curl -sL https://your-url.com/install_agent.sh | sudo bash
```

## Manual Setup

If you prefer to set up the components manually, follow the instructions below.

### Prerequisites

### Hardware Requirements

These are general recommendations and may vary based on the number of agents and the frequency of data collection.

**Server:**
-   **Minimum:** 1 vCPU, 512MB RAM, 1GB Disk Space
-   **Recommended:** 2 vCPUs, 1GB RAM, 5GB Disk Space

**Agent:**
-   The agent is very lightweight and should have a negligible impact on system resources.

### Operating System

-   **Server:** Linux (Ubuntu, CentOS, etc.) is recommended for running as a systemd service. Can be run on macOS or Windows for development.
-   **Agent:** Linux, macOS, or Windows.

### Software Dependencies

-   **Python 3.7+** and `pip`
-   **Node.js and npm** (for the web interface)
-   `git` (for cloning the repository)

## Security

Communication between the agent and server is secured using HTTPS with self-signed SSL certificates, making it suitable for offline or private network deployments.

-   The server setup script automatically generates a private key (`antarmon.key`) and a self-signed public certificate (`antarmon.crt`).
-   The agent must be configured with the server's public certificate to ensure it is connecting to the correct server.

## Server Setup

### Development Mode

1.  **Navigate to the `server` directory:**
    ```bash
    cd server
    ```
2.  **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Run the server:**
    ```bash
    uvicorn main:app --reload
    ```

### As a Systemd Service (Linux)

1.  **Navigate to the `server` directory.**
2.  **Make the setup script executable:**
    ```bash
    chmod +x setup_server.sh
    ```
3.  **Run the script with `sudo`:**
    ```bash
    sudo ./setup_server.sh
    ```

## Agent Setup

### Development Mode

1.  **Get an API Key:** Register a new agent in the web interface to get an API key.
2.  **Navigate to the `agent` directory:**
    ```bash
    cd agent
    ```
3.  **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Run the agent:**
    ```bash
    python agent.py
    ```
    The first time you run it, you will be prompted to enter the API key.

### As a Systemd Service (Linux)

1.  **Navigate to the `agent` directory.**
2.  **Make the setup script executable:**
    ```bash
    chmod +x setup_agent.sh
    ```
3.  **Run the script with `sudo`:**
    ```bash
    sudo ./setup_agent.sh
    ```
    The script will prompt you for the API key during installation.

## Web Interface

1.  **Navigate to the `server/ui` directory:**
    ```bash
    cd server/ui
    ```
2.  **Install Node.js dependencies:**
    ```bash
    npm install
    ```
3.  **Start the development server:**
    ```bash
    npm start
    ```
4.  The web interface will be available at `http://localhost:3000`.

### Using the Interface

-   **Register/Login:** Create a user account and log in.
-   **Manage Agents:** Register new agents and view their API keys.
-   **Manage Alerts:** Create and delete alerts for different metrics and thresholds.
-   **Dashboard:** View real-time metrics from your agents.
