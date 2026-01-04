#!/bin/bash
# =============================================================================
# Setup ZITADEL Roles for Multi-Tenant Application
# =============================================================================
# This script creates the standard role hierarchy in your ZITADEL project.
# Run after ZITADEL is deployed and you've created a project.
# =============================================================================

set -e

# Configuration
ZITADEL_AUTHORITY="${ZITADEL_AUTHORITY:-http://localhost:8080}"
PROJECT_ID="${PROJECT_ID:-}"
ACCESS_TOKEN="${ACCESS_TOKEN:-}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Helper functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check required variables
check_requirements() {
    if [ -z "$PROJECT_ID" ]; then
        log_error "PROJECT_ID is required. Set it via environment variable."
        echo "  export PROJECT_ID=your-project-id"
        exit 1
    fi

    if [ -z "$ACCESS_TOKEN" ]; then
        log_error "ACCESS_TOKEN is required. Get one from ZITADEL Console."
        echo "  1. Go to ZITADEL Console"
        echo "  2. Create a Service Account with Manager role"
        echo "  3. Generate a Personal Access Token"
        echo "  4. export ACCESS_TOKEN=your-token"
        exit 1
    fi
}

# Create a role in the project
create_role() {
    local role_key=$1
    local display_name=$2
    local group=$3

    log_info "Creating role: $role_key ($display_name)"

    response=$(curl -s -w "\n%{http_code}" -X POST \
        "${ZITADEL_AUTHORITY}/management/v1/projects/${PROJECT_ID}/roles" \
        -H "Authorization: Bearer ${ACCESS_TOKEN}" \
        -H "Content-Type: application/json" \
        -d "{
            \"roleKey\": \"${role_key}\",
            \"displayName\": \"${display_name}\",
            \"group\": \"${group}\"
        }")

    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | sed '$d')

    if [ "$http_code" -eq 200 ] || [ "$http_code" -eq 201 ]; then
        log_info "✓ Created role: $role_key"
    elif [ "$http_code" -eq 409 ]; then
        log_warn "Role already exists: $role_key"
    else
        log_error "Failed to create role $role_key: $body"
    fi
}

# Main execution
main() {
    log_info "Setting up roles in ZITADEL project: $PROJECT_ID"
    log_info "ZITADEL Authority: $ZITADEL_AUTHORITY"
    echo ""

    check_requirements

    # Create roles with hierarchy
    log_info "Creating role hierarchy..."
    echo ""

    # Super Admin - cross-tenant access
    create_role "super_admin" "Super Administrator" "Administration"

    # Org Admin - organization management
    create_role "org_admin" "Organization Administrator" "Administration"

    # Editor - content creation/modification
    create_role "editor" "Editor" "Content"

    # Viewer - read-only access
    create_role "viewer" "Viewer" "Content"

    echo ""
    log_info "Role setup complete!"
    echo ""
    log_info "Next steps:"
    echo "  1. Assign 'super_admin' role to your admin users"
    echo "  2. Create organizations for each tenant"
    echo "  3. Assign 'org_admin' role to tenant administrators"
    echo "  4. Regular users can be assigned 'editor' or 'viewer' roles"
}

main "$@"
