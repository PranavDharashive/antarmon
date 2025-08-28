#!/bin/bash

# This script sets up the AntarMon server as a systemd service.
# It must be run with root privileges.

if [ "$(id -u)" -ne 0 ]; then
    echo "This script must be run as root" >&2
    exit 1
fi

# Create a dedicated user and group for the application
if ! id -u antarmon > /dev/null 2>&1; then
    echo "Creating user and group 'antarmon'..."
    useradd -r -s /bin/false antarmon
fi

# Create the installation directory
APP_DIR="/opt/antarmon-server"
echo "Creating installation directory ${APP_DIR}..."
mkdir -p ${APP_DIR}

# Copy the application files
# Assumes the script is run from the 'server' directory
echo "Copying application files..."
cp -r . ${APP_DIR}

# Generate self-signed certificates
echo "Generating SSL certificates..."
chmod +x ${APP_DIR}/generate_certs.sh
${APP_DIR}/generate_certs.sh

# Create a Python virtual environment and install dependencies
echo "Setting up Python virtual environment..."
python3 -m venv ${APP_DIR}/venv
source ${APP_DIR}/venv/bin/activate
${APP_DIR}/venv/bin/pip install -r ${APP_DIR}/requirements.txt

# Set ownership of the application directory
echo "Setting ownership..."
chown -R antarmon:antarmon ${APP_DIR}

# Copy the systemd service file
SERVICE_FILE="antarmon-server.service"
SERVICE_DEST="/etc/systemd/system/${SERVICE_FILE}"
echo "Installing systemd service file..."
cp ${APP_DIR}/${SERVICE_FILE} ${SERVICE_DEST}

# Reload systemd, enable and start the service
echo "Starting and enabling the AntarMon server service..."
systemctl daemon-reload
systemctl enable ${SERVICE_FILE}
systemctl start ${SERVICE_FILE}

echo "AntarMon server setup complete."
echo "You can check the status of the service with: systemctl status ${SERVICE_FILE}"
