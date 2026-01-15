#!/bin/bash
# Setup local Zitadel for testing

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DOCKER_DIR="$SCRIPT_DIR/../docker"

echo "=== Local Zitadel Setup ==="
echo ""

# Check Docker
if ! command -v docker &> /dev/null; then
    echo "Error: Docker is not installed"
    exit 1
fi

if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "Error: Docker Compose is not installed"
    exit 1
fi

# Start Zitadel
cd "$DOCKER_DIR"

echo "Starting Zitadel..."
docker compose up -d

echo ""
echo "Waiting for Zitadel to be healthy..."

# Wait for health
MAX_ATTEMPTS=60
ATTEMPT=0
while [ $ATTEMPT -lt $MAX_ATTEMPTS ]; do
    if curl -sf http://localhost:8080/debug/healthz > /dev/null 2>&1; then
        echo "Zitadel is ready!"
        break
    fi
    ATTEMPT=$((ATTEMPT + 1))
    echo "  Waiting... ($ATTEMPT/$MAX_ATTEMPTS)"
    sleep 2
done

if [ $ATTEMPT -eq $MAX_ATTEMPTS ]; then
    echo "Error: Zitadel did not become healthy"
    docker compose logs zitadel
    exit 1
fi

echo ""
echo "=== Zitadel is running ==="
echo ""
echo "Console:    http://localhost:8080/ui/console"
echo "Username:   admin@local.test"
echo "Password:   Admin123!"
echo ""
echo "OIDC Discovery: http://localhost:8080/.well-known/openid-configuration"
echo ""
echo "Next steps:"
echo "  1. Login to console"
echo "  2. Create a project and application"
echo "  3. Create a service user for automation"
echo "  4. Use ./create-service-account.sh to set up tokens"
