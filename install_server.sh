#!/bin/bash

# This script downloads and installs the AntarMon server.

# In a real-world scenario, this URL would point to a public location
RELEASE_URL="file:///Users/pranavdharashive/antarmon/release/antarmon-server.tar.gz"

INSTALL_DIR="/tmp/antarmon-installer"
mkdir -p ${INSTALL_DIR}

cd ${INSTALL_DIR}

echo "Downloading AntarMon server..."
wget -O antarmon-server.tar.gz ${RELEASE_URL}

echo "Extracting..."
tar -xzf antarmon-server.tar.gz

cd antarmon-server

echo "Running setup..."
sudo ./setup_server.sh

cd /tmp
rm -rf ${INSTALL_DIR}

echo "Installation complete."
