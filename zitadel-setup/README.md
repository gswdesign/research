# ZITADEL Enterprise Auth Setup

Enterprise-grade authentication and authorization system using ZITADEL with:
- Google SSO (primary) + Email/Password (backup)
- Custom branded login UI (React + Vike)
- Multi-tenant B2B architecture with hierarchical RBAC
- Cloudflare Pages + Workers integration
- Railway deployment ready

## Quick Start (Local Development)

### Prerequisites
- Docker & Docker Compose
- Node.js 20+
- pnpm (or npm/yarn)

### 1. Setup Environment

```bash
# Copy environment template
cp .env.example .env

# Generate a master key (REQUIRED)
openssl rand -base64 32
# Copy the output to ZITADEL_MASTERKEY in .env

# Edit .env with your values
nano .env
```

### 2. Start Services

```bash
# Start ZITADEL + PostgreSQL
docker compose up -d

# Wait for ZITADEL to be ready (check logs)
docker compose logs -f zitadel
```

### 3. Access ZITADEL Console

Open http://localhost:8080/ui/console

**Default Credentials:**
- Username: `admin@zitadel.localhost` (or your ZITADEL_ADMIN_USERNAME)
- Password: `Password1!` (or your ZITADEL_ADMIN_PASSWORD)

### 4. Create OIDC Application

1. Go to Projects → Create New Project → "Login App"
2. Create Application → Web → PKCE
3. Set Redirect URIs: `http://localhost:3000/callback`
4. Copy the Client ID to your `.env` file

### 5. Start Custom Login UI

```bash
cd login-ui
pnpm install
pnpm dev
```

Open http://localhost:3000

## Project Structure

```
zitadel-setup/
├── docker-compose.yml        # Local development stack
├── .env.example              # Environment template
├── config/
│   ├── zitadel-config.yaml  # ZITADEL configuration
│   └── init.sql             # PostgreSQL initialization
├── login-ui/                 # Custom React + Vike login
├── cloudflare/
│   ├── spa-example/         # Cloudflare Pages SPA
│   └── worker-example/      # Cloudflare Worker API
├── docs/
│   ├── DEPLOYMENT.md        # Railway deployment guide
│   ├── GOOGLE-SSO-SETUP.md  # Google OAuth setup
│   └── PERMISSIONS.md       # RBAC configuration
└── scripts/
    ├── setup-roles.sh       # Create default roles
    └── create-org.sh        # Onboard new tenant
```

## Multi-Tenant Architecture

```
ZITADEL Instance
├── Default Org (super admins)
├── Tenant A (Organization)
│   ├── Users
│   │   ├── org_admin → Full access
│   │   ├── editor → Create/edit
│   │   └── viewer → Read-only
│   └── Projects
├── Tenant B (Organization)
│   └── ...
```

### Role Hierarchy

| Role | Scope | Permissions |
|------|-------|-------------|
| super_admin | Cross-tenant | Full access to all tenants |
| org_admin | Single tenant | Full access within org |
| editor | Single tenant | Create, edit, view |
| viewer | Single tenant | View only |

## Production Deployment (Railway)

See [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) for full instructions.

```bash
# Login to Railway
railway login

# Link to project
railway link

# Deploy
railway up
```

Railway auto-detects Dockerfile and configures:
- TLS/HTTPS automatically
- Custom domain support
- PostgreSQL addon available

## Google SSO Setup

See [docs/GOOGLE-SSO-SETUP.md](docs/GOOGLE-SSO-SETUP.md) for detailed walkthrough.

Quick steps:
1. Create project in Google Cloud Console
2. Configure OAuth consent screen
3. Create OAuth 2.0 credentials
4. Add redirect URI: `https://your-domain/ui/login/login/externalidp/callback`
5. Configure in ZITADEL Console → Identity Providers → Google

## Cloudflare Integration

### SPA on Cloudflare Pages
See `cloudflare/spa-example/` for a complete example using:
- `@zitadel/react` SDK
- PKCE flow (no client secret)
- Silent refresh

### API on Cloudflare Workers
See `cloudflare/worker-example/` for JWT validation middleware:
- JWKS caching
- Role extraction
- Multi-tenant context

## Troubleshooting

### ZITADEL won't start
```bash
# Check logs
docker compose logs zitadel

# Common issues:
# - Master key not 32 bytes
# - PostgreSQL not ready (wait longer)
# - Port 8080 already in use
```

### Can't login
- Ensure ZITADEL_EXTERNALDOMAIN matches your access URL
- Check ZITADEL_EXTERNALSECURE matches HTTP/HTTPS
- Verify redirect URIs in OIDC app settings

### Database connection failed
```bash
# Check PostgreSQL is healthy
docker compose ps
docker compose logs postgres
```

## Security Considerations

- [ ] Change default admin password immediately
- [ ] Use strong ZITADEL_MASTERKEY (32 bytes)
- [ ] Enable MFA for admin accounts
- [ ] Use HTTPS in production (Railway handles this)
- [ ] Rotate secrets periodically
- [ ] Review audit logs regularly

## License

MIT
