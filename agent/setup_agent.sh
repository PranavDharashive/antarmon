#!/bin/bash

# This script sets up the AntarMon agent as a systemd service.
# It must be run with root privileges.

if [ "$(id -u)" -ne 0 ]; then
    echo "This script must be run as root" >&2
    exit 1
fi

# Create a dedicated user and group for the application
if ! id -u antarmon-agent > /dev/null 2>&1; then
    echo "Creating user and group 'antarmon-agent'..."
    useradd -r -s /bin/false antarmon-agent
fi

# Create the installation directory
APP_DIR="/opt/antarmon-agent"
echo "Creating installation directory ${APP_DIR}..."
mkdir -p ${APP_DIR}

# Copy the application files
# Assumes the script is run from the 'agent' directory
echo "Copying application files..."
cp -r . ${APP_DIR}

# Create a Python virtual environment and install dependencies
echo "Setting up Python virtual environment..."
python3 -m venv ${APP_DIR}/venv
source ${APP_DIR}/venv/bin/activate
${APP_DIR}/venv/bin/pip install -r ${APP_DIR}/requirements.txt

# Configure the API key and server
CONFIG_FILE="${APP_DIR}/config.ini"
CERT_DEST="${APP_DIR}/antarmon.crt"

if [ ! -f "${CONFIG_FILE}" ]; then
    read -p "Please enter the API key for this agent: " api_key
    read -p "Please enter the server IP or domain name: " server_ip
    read -p "Please enter the full path to the server certificate (antarmon.crt): " cert_path

    echo "[DEFAULT]" > ${CONFIG_FILE}
    echo "API_KEY = ${api_key}" >> ${CONFIG_FILE}
    echo "SERVER_IP = ${server_ip}" >> ${CONFIG_FILE}

    echo "Copying server certificate..."
    cp "${cert_path}" "${CERT_DEST}"
fi

# Set ownership of the application directory
echo "Setting ownership..."
chown -R antarmon-agent:antarmon-agent ${APP_DIR}

# Copy the systemd service file
SERVICE_FILE="antarmon-agent.service"
SERVICE_DEST="/etc/systemd/system/${SERVICE_FILE}"
echo "Installing systemd service file..."
cp ${APP_DIR}/${SERVICE_FILE} ${SERVICE_DEST}

# Reload systemd, enable and start the service
echo "Starting and enabling the AntarMon agent service..."
systemctl daemon-reload
systemctl enable ${SERVICE_FILE}
systemctl start ${SERVICE_FILE}

echo "AntarMon agent setup complete."
echo "You can check the status of the service with: systemctl status ${SERVICE_FILE}"
