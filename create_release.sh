#!/bin/bash

# This script creates release packages for the AntarMon server and agent.

RELEASE_DIR="release"
mkdir -p ${RELEASE_DIR}

# --- Create Server Release ---
echo "Creating server release..."
SERVER_RELEASE_NAME="antarmon-server"
SERVER_TEMP_DIR="/tmp/${SERVER_RELEASE_NAME}"

mkdir -p ${SERVER_TEMP_DIR}
cp -r server/* ${SERVER_TEMP_DIR}

# We don't need the node_modules in the release package
rm -rf ${SERVER_TEMP_DIR}/ui/node_modules

tar -czf ${RELEASE_DIR}/${SERVER_RELEASE_NAME}.tar.gz -C /tmp ${SERVER_RELEASE_NAME}

rm -rf ${SERVER_TEMP_DIR}

echo "Server release created: ${RELEASE_DIR}/${SERVER_RELEASE_NAME}.tar.gz"

# --- Create Agent Release ---
echo "Creating agent release..."
AGENT_RELEASE_NAME="antarmon-agent"
AGENT_TEMP_DIR="/tmp/${AGENT_RELEASE_NAME}"

mkdir -p ${AGENT_TEMP_DIR}
cp -r agent/* ${AGENT_TEMP_DIR}

tar -czf ${RELEASE_DIR}/${AGENT_RELEASE_NAME}.tar.gz -C /tmp ${AGENT_RELEASE_NAME}

rm -rf ${AGENT_TEMP_DIR}

echo "Agent release created: ${RELEASE_DIR}/${AGENT_RELEASE_NAME}.tar.gz"
