#!/bin/bash
# Get a token from the mock OIDC server
#
# Usage:
#   ./get-mock-token.sh
#   ./get-mock-token.sh --email user@test.com --name "Test User"

set -e

MOCK_URL="${MOCK_URL:-http://localhost:9000}"
CLIENT_ID="${CLIENT_ID:-test-client}"
EMAIL="${EMAIL:-test@local.test}"
NAME="${NAME:-Test User}"

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --email) EMAIL="$2"; shift 2 ;;
        --name) NAME="$2"; shift 2 ;;
        --client-id) CLIENT_ID="$2"; shift 2 ;;
        *) echo "Unknown option: $1" >&2; exit 1 ;;
    esac
done

# Get token from mock server
RESPONSE=$(curl -sf -X POST "$MOCK_URL/test/token" \
    -H "Content-Type: application/json" \
    -d '{
        "client_id": "'"$CLIENT_ID"'",
        "email": "'"$EMAIL"'",
        "name": "'"$NAME"'",
        "scope": "openid profile email"
    }')

if [ -z "$RESPONSE" ]; then
    echo "Error: Mock server not responding at $MOCK_URL" >&2
    echo "Start it with: cd mocks && npm start" >&2
    exit 1
fi

echo "$RESPONSE" | jq -r '.access_token'
