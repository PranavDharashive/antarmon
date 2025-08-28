#!/bin/bash

# This script generates a self-signed SSL certificate valid for 365 days.

# Set the output directory to be the same as the script's directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

KEY_FILE="${DIR}/antarmon.key"
CERT_FILE="${DIR}/antarmon.crt"

if [ -f "${CERT_FILE}" ]; then
    echo "Certificate already exists. Skipping generation."
    exit 0
fi

echo "Generating self-signed certificate..."

openssl req -x509 -newkey rsa:2048 -nodes \
    -keyout "${KEY_FILE}" \
    -out "${CERT_FILE}" \
    -days 365 \
    -subj "/C=US/ST=California/L=San Francisco/O=AntarMon/OU=IT Department/CN=antarmon.local"

echo "Certificate generated successfully:"
echo "  Key: ${KEY_FILE}"
echo "  Cert: ${CERT_FILE}"
