#!/bin/bash

# This script downloads and installs the AntarMon agent.

# In a real-world scenario, this URL would point to a public location
RELEASE_URL="file:///Users/pranavdharashive/antarmon/release/antarmon-agent.tar.gz"

INSTALL_DIR="/tmp/antarmon-installer"
mkdir -p ${INSTALL_DIR}

cd ${INSTALL_DIR}

echo "Downloading AntarMon agent..."
wget -O antarmon-agent.tar.gz ${RELEASE_URL}

echo "Extracting..."
tar -xzf antarmon-agent.tar.gz

cd antarmon-agent

echo "Running setup..."
sudo ./setup_agent.sh

cd /tmp
rm -rf ${INSTALL_DIR}

echo "Installation complete."
