#!/bin/bash
# =============================================================================
# Create New Tenant Organization in ZITADEL
# =============================================================================
# This script creates a new organization (tenant) and optionally invites
# the first admin user.
# =============================================================================

set -e

# Configuration
ZITADEL_AUTHORITY="${ZITADEL_AUTHORITY:-http://localhost:8080}"
ACCESS_TOKEN="${ACCESS_TOKEN:-}"
PROJECT_ID="${PROJECT_ID:-}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

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

log_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

# Usage information
usage() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Create a new tenant organization in ZITADEL"
    echo ""
    echo "Required Environment Variables:"
    echo "  ACCESS_TOKEN    ZITADEL API access token"
    echo "  PROJECT_ID      Project ID for role assignment"
    echo ""
    echo "Options:"
    echo "  --name NAME           Organization name (required)"
    echo "  --domain DOMAIN       Primary domain (optional)"
    echo "  --admin-email EMAIL   First admin email (optional)"
    echo "  --admin-name NAME     First admin display name (optional)"
    echo "  -h, --help            Show this help message"
    echo ""
    echo "Example:"
    echo "  $0 --name \"Acme Corp\" --domain acme.com --admin-email admin@acme.com"
}

# Parse arguments
ORG_NAME=""
ORG_DOMAIN=""
ADMIN_EMAIL=""
ADMIN_NAME=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --name)
            ORG_NAME="$2"
            shift 2
            ;;
        --domain)
            ORG_DOMAIN="$2"
            shift 2
            ;;
        --admin-email)
            ADMIN_EMAIL="$2"
            shift 2
            ;;
        --admin-name)
            ADMIN_NAME="$2"
            shift 2
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        *)
            log_error "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

# Validate inputs
validate() {
    if [ -z "$ACCESS_TOKEN" ]; then
        log_error "ACCESS_TOKEN is required"
        exit 1
    fi

    if [ -z "$ORG_NAME" ]; then
        log_error "--name is required"
        usage
        exit 1
    fi
}

# Create organization
create_organization() {
    log_step "Creating organization: $ORG_NAME"

    local payload="{\"name\": \"${ORG_NAME}\"}"

    response=$(curl -s -w "\n%{http_code}" -X POST \
        "${ZITADEL_AUTHORITY}/admin/v1/orgs" \
        -H "Authorization: Bearer ${ACCESS_TOKEN}" \
        -H "Content-Type: application/json" \
        -d "$payload")

    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | sed '$d')

    if [ "$http_code" -eq 200 ] || [ "$http_code" -eq 201 ]; then
        ORG_ID=$(echo "$body" | grep -o '"id":"[^"]*"' | head -1 | cut -d'"' -f4)
        log_info "✓ Created organization: $ORG_NAME (ID: $ORG_ID)"
    else
        log_error "Failed to create organization: $body"
        exit 1
    fi
}

# Add domain to organization
add_domain() {
    if [ -z "$ORG_DOMAIN" ]; then
        return
    fi

    log_step "Adding domain: $ORG_DOMAIN"

    response=$(curl -s -w "\n%{http_code}" -X POST \
        "${ZITADEL_AUTHORITY}/management/v1/orgs/${ORG_ID}/domains" \
        -H "Authorization: Bearer ${ACCESS_TOKEN}" \
        -H "Content-Type: application/json" \
        -d "{\"domain\": \"${ORG_DOMAIN}\"}")

    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | sed '$d')

    if [ "$http_code" -eq 200 ] || [ "$http_code" -eq 201 ]; then
        log_info "✓ Added domain: $ORG_DOMAIN"
        log_warn "Domain verification required. Check ZITADEL Console."
    else
        log_warn "Could not add domain: $body"
    fi
}

# Create admin user
create_admin_user() {
    if [ -z "$ADMIN_EMAIL" ]; then
        return
    fi

    log_step "Creating admin user: $ADMIN_EMAIL"

    local name="${ADMIN_NAME:-Administrator}"
    local username="${ADMIN_EMAIL}"

    response=$(curl -s -w "\n%{http_code}" -X POST \
        "${ZITADEL_AUTHORITY}/management/v1/users/human/_import" \
        -H "Authorization: Bearer ${ACCESS_TOKEN}" \
        -H "x-zitadel-orgid: ${ORG_ID}" \
        -H "Content-Type: application/json" \
        -d "{
            \"userName\": \"${username}\",
            \"profile\": {
                \"firstName\": \"${name}\",
                \"lastName\": \"Admin\",
                \"displayName\": \"${name}\"
            },
            \"email\": {
                \"email\": \"${ADMIN_EMAIL}\",
                \"isEmailVerified\": false
            },
            \"passwordChangeRequired\": true
        }")

    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | sed '$d')

    if [ "$http_code" -eq 200 ] || [ "$http_code" -eq 201 ]; then
        USER_ID=$(echo "$body" | grep -o '"userId":"[^"]*"' | head -1 | cut -d'"' -f4)
        log_info "✓ Created user: $ADMIN_EMAIL (ID: $USER_ID)"

        # Assign org_admin role
        assign_role
    else
        log_warn "Could not create user: $body"
    fi
}

# Assign org_admin role to user
assign_role() {
    if [ -z "$USER_ID" ] || [ -z "$PROJECT_ID" ]; then
        log_warn "Skipping role assignment (no USER_ID or PROJECT_ID)"
        return
    fi

    log_step "Assigning org_admin role to user"

    response=$(curl -s -w "\n%{http_code}" -X POST \
        "${ZITADEL_AUTHORITY}/management/v1/users/${USER_ID}/grants" \
        -H "Authorization: Bearer ${ACCESS_TOKEN}" \
        -H "x-zitadel-orgid: ${ORG_ID}" \
        -H "Content-Type: application/json" \
        -d "{
            \"projectId\": \"${PROJECT_ID}\",
            \"roleKeys\": [\"org_admin\"]
        }")

    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | sed '$d')

    if [ "$http_code" -eq 200 ] || [ "$http_code" -eq 201 ]; then
        log_info "✓ Assigned org_admin role"
    else
        log_warn "Could not assign role: $body"
    fi
}

# Grant project to organization
grant_project() {
    if [ -z "$PROJECT_ID" ]; then
        return
    fi

    log_step "Granting project access to organization"

    response=$(curl -s -w "\n%{http_code}" -X POST \
        "${ZITADEL_AUTHORITY}/management/v1/projects/${PROJECT_ID}/grants" \
        -H "Authorization: Bearer ${ACCESS_TOKEN}" \
        -H "Content-Type: application/json" \
        -d "{
            \"grantedOrgId\": \"${ORG_ID}\",
            \"roleKeys\": [\"org_admin\", \"editor\", \"viewer\"]
        }")

    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | sed '$d')

    if [ "$http_code" -eq 200 ] || [ "$http_code" -eq 201 ]; then
        log_info "✓ Granted project access"
    else
        log_warn "Could not grant project: $body"
    fi
}

# Main execution
main() {
    echo "========================================"
    echo "ZITADEL Tenant Onboarding"
    echo "========================================"
    echo ""

    validate

    log_info "ZITADEL Authority: $ZITADEL_AUTHORITY"
    echo ""

    create_organization
    add_domain
    grant_project
    create_admin_user

    echo ""
    echo "========================================"
    log_info "Tenant onboarding complete!"
    echo "========================================"
    echo ""
    echo "Organization ID: $ORG_ID"
    echo "Organization Name: $ORG_NAME"
    [ -n "$ORG_DOMAIN" ] && echo "Domain: $ORG_DOMAIN"
    [ -n "$ADMIN_EMAIL" ] && echo "Admin: $ADMIN_EMAIL"
    echo ""
    log_info "Next steps:"
    echo "  1. Admin should receive email to set password"
    echo "  2. Verify domain ownership (if domain added)"
    echo "  3. Admin can invite additional users"
}

main "$@"
