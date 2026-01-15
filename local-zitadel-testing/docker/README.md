# Local Zitadel with Docker

Run a local Zitadel instance for testing - no 2FA required.

## Quick Start

```bash
# Start Zitadel
docker-compose up -d

# Wait for healthy (about 30-60 seconds first time)
docker-compose ps

# Access console
open http://localhost:8080
```

## Default Credentials

| User | Password | Use |
|------|----------|-----|
| `admin@local.test` | `Admin123!` | Admin console access |

## URLs

- Console: http://localhost:8080/ui/console
- Auth endpoint: http://localhost:8080/oauth/v2/authorize
- Token endpoint: http://localhost:8080/oauth/v2/token
- OIDC Discovery: http://localhost:8080/.well-known/openid-configuration

## Create a Test Application

1. Login to console at http://localhost:8080/ui/console
2. Go to Projects > Create Project > "test-project"
3. Add Application > Web > "test-app"
4. Choose PKCE (for browser) or Code (for server)
5. Set redirect URI: `http://localhost:3000/callback`
6. Save and note the Client ID

## Create a Service Account (for automation)

1. Login to console
2. Go to Users > Service Users > Create
3. Name: `test-automation`
4. Create Personal Access Token or add JWT key
5. Use this token in your tests

## Quick API Token (after setup)

```bash
# With service account PAT
curl -X POST http://localhost:8080/oauth/v2/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=urn:ietf:params:oauth:grant-type:jwt-bearer" \
  -d "scope=openid profile email" \
  -d "assertion=YOUR_JWT_HERE"
```

## Stop/Reset

```bash
# Stop
docker-compose down

# Full reset (delete data)
docker-compose down -v
```

## Differences from Production

| Feature | Local | Production (auth.vmiapps.com) |
|---------|-------|-------------------------------|
| MFA | Disabled | Required |
| TLS | Disabled | Enabled |
| Cloudflare | None | Workers in front |
| Domain | localhost:8080 | auth.vmiapps.com |
