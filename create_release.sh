#!/bin/bash

# This script creates release packages for the AntarMon server and agent.

# Get the absolute path of the project root
PROJECT_ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
RELEASE_DIR="${PROJECT_ROOT}/release"
mkdir -p ${RELEASE_DIR}

# --- Create Server Release ---
echo "Creating server release..."
SERVER_RELEASE_NAME="antarmon-server"
SERVER_SOURCE_DIR="${PROJECT_ROOT}/server"
SERVER_TEMP_DIR="/tmp/${SERVER_RELEASE_NAME}"

# Ensure temp dir is clean
rm -rf ${SERVER_TEMP_DIR}
mkdir -p ${SERVER_TEMP_DIR}

# Copy server files to temp location
cp -r ${SERVER_SOURCE_DIR}/* ${SERVER_TEMP_DIR}

# We don't need the node_modules in the release package
rm -rf ${SERVER_TEMP_DIR}/ui/node_modules

# Go to the temp directory to create the archive with correct paths
cd /tmp
tar -czf ${RELEASE_DIR}/${SERVER_RELEASE_NAME}.tar.gz ${SERVER_RELEASE_NAME}

# Clean up
rm -rf ${SERVER_TEMP_DIR}

echo "Server release created: ${RELEASE_DIR}/${SERVER_RELEASE_NAME}.tar.gz"

# --- Create Agent Release ---
echo "Creating agent release..."
AGENT_RELEASE_NAME="antarmon-agent"
AGENT_SOURCE_DIR="${PROJECT_ROOT}/agent"
AGENT_TEMP_DIR="/tmp/${AGENT_RELEASE_NAME}"

# Ensure temp dir is clean
rm -rf ${AGENT_TEMP_DIR}
mkdir -p ${AGENT_TEMP_DIR}

# Copy agent files to temp location
cp -r ${AGENT_SOURCE_DIR}/* ${AGENT_TEMP_DIR}

# Go to the temp directory to create the archive
cd /tmp
tar -czf ${RELEASE_DIR}/${AGENT_RELEASE_NAME}.tar.gz ${AGENT_RELEASE_NAME}

# Clean up
rm -rf ${AGENT_TEMP_DIR}

echo "Agent release created: ${RELEASE_DIR}/${AGENT_RELEASE_NAME}.tar.gz"

# Return to the original directory
cd ${PROJECT_ROOT}