#!/bin/bash

# Endereço do servidor
SERVER_URL="http://192.168.15.80:5000"

# Endpoint Register
REGISTER_ENDPOINT="$SERVER_URL/register"

# Endpoint Generate QRCode
QRCODE_ENDPOINT="$SERVER_URL/generate_qrcode"

# Solicitação ao endpoint Register
response=$(curl -s -o - -w "\n%{http_code}" -H "Content-Type: application/json" -X POST -d '{"username": "testUser", "password": "testPass"}' $REGISTER_ENDPOINT)

http_code=$(echo "$response" | tail -n1)
response_body=$(echo "$response" | head -n -1)

# Imprime a resposta do endpoint Register
echo "===== RESPONSE FROM /register ====="
echo "HTTP Code: $http_code"
echo "Response Body:"
echo "$response_body"
echo "==================================="

if [[ $http_code -ne 200 ]]; then
    echo "Failed to register. Response code: $http_code"
    exit 1
fi

# Extrai a api_key da resposta
api_key=$(echo "$response_body" | jq -r '.api_key')

if [[ -z "$api_key" ]]; then
    echo "Failed to extract api_key from response."
    exit 1
fi

# Solicitação ao endpoint Generate QRCode
response=$(curl -s -o - -w "\n%{http_code}" -H "Content-Type: application/json" -H "x-api-key: $api_key" -X POST -d '{"content": "www.linkedin.com/in/caiohenrks"}' $QRCODE_ENDPOINT)

http_code=$(echo "$response" | tail -n1)
response_body=$(echo "$response" | head -n -1)

# Imprime a resposta do endpoint Generate QRCode
echo "===== RESPONSE FROM /generate_qrcode ====="
echo "HTTP Code: $http_code"
echo "Response Body:"
# echo "$response_body"
echo "=========================================="

if [[ $http_code -ne 200 && $http_code -ne 401 ]]; then
    echo "Failed to generate QRCode. Response code: $http_code"
    exit 1
fi


echo "Script completed successfully!"
