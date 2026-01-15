#!/bin/bash
# Get a token using service account credentials
#
# For production (auth.vmiapps.com), create a service account:
#   1. Login to Zitadel console
#   2. Go to Users > Service Users > Create
#   3. Generate a Personal Access Token (PAT) or JWT key
#
# Usage:
#   # With PAT (simplest)
#   export ZITADEL_PAT="your-personal-access-token"
#   ./get-service-token.sh
#
#   # With JWT key file
#   export ZITADEL_KEY_FILE="/path/to/key.json"
#   ./get-service-token.sh

set -e

# Configuration
ZITADEL_URL="${ZITADEL_URL:-http://localhost:8080}"
TOKEN_CACHE="${TOKEN_CACHE:-$(dirname "$0")/../tokens/cached-token.json}"

# If PAT is set, just return it (PATs work directly as access tokens)
if [ -n "$ZITADEL_PAT" ]; then
    echo "$ZITADEL_PAT"
    exit 0
fi

# If JWT key file is set, use client credentials flow
if [ -n "$ZITADEL_KEY_FILE" ]; then
    if [ ! -f "$ZITADEL_KEY_FILE" ]; then
        echo "Error: Key file not found: $ZITADEL_KEY_FILE" >&2
        exit 1
    fi

    # Check for cached token
    if [ -f "$TOKEN_CACHE" ]; then
        EXPIRES=$(jq -r '.expires_at // 0' "$TOKEN_CACHE" 2>/dev/null || echo "0")
        NOW=$(date +%s)
        if [ "$EXPIRES" -gt "$NOW" ]; then
            jq -r '.access_token' "$TOKEN_CACHE"
            exit 0
        fi
    fi

    # Parse key file
    USER_ID=$(jq -r '.userId' "$ZITADEL_KEY_FILE")
    KEY_ID=$(jq -r '.keyId' "$ZITADEL_KEY_FILE")
    KEY=$(jq -r '.key' "$ZITADEL_KEY_FILE")

    # Create JWT assertion
    NOW=$(date +%s)
    EXP=$((NOW + 3600))

    HEADER=$(echo -n '{"alg":"RS256","kid":"'"$KEY_ID"'"}' | base64 -w0 | tr '+/' '-_' | tr -d '=')
    PAYLOAD=$(echo -n '{"iss":"'"$USER_ID"'","sub":"'"$USER_ID"'","aud":"'"$ZITADEL_URL"'","exp":'"$EXP"',"iat":'"$NOW"'}' | base64 -w0 | tr '+/' '-_' | tr -d '=')

    # Sign with private key
    SIGNATURE=$(echo -n "$HEADER.$PAYLOAD" | openssl dgst -sha256 -sign <(echo "$KEY") | base64 -w0 | tr '+/' '-_' | tr -d '=')
    JWT="$HEADER.$PAYLOAD.$SIGNATURE"

    # Exchange for access token
    RESPONSE=$(curl -sf -X POST "$ZITADEL_URL/oauth/v2/token" \
        -H "Content-Type: application/x-www-form-urlencoded" \
        -d "grant_type=urn:ietf:params:oauth:grant-type:jwt-bearer" \
        -d "scope=openid profile email" \
        -d "assertion=$JWT")

    ACCESS_TOKEN=$(echo "$RESPONSE" | jq -r '.access_token')
    EXPIRES_IN=$(echo "$RESPONSE" | jq -r '.expires_in // 3600')

    # Cache the token
    mkdir -p "$(dirname "$TOKEN_CACHE")"
    echo "$RESPONSE" | jq ". + {expires_at: $((NOW + EXPIRES_IN - 60))}" > "$TOKEN_CACHE"

    echo "$ACCESS_TOKEN"
    exit 0
fi

echo "Error: Set ZITADEL_PAT or ZITADEL_KEY_FILE" >&2
echo "" >&2
echo "For production (auth.vmiapps.com):" >&2
echo "  1. Login to Zitadel console" >&2
echo "  2. Create a Service User" >&2
echo "  3. Generate a Personal Access Token or JWT key" >&2
echo "  4. Set ZITADEL_PAT or ZITADEL_KEY_FILE" >&2
exit 1
