# Railway Deployment Guide

Deploy ZITADEL and the custom login UI to Railway for production use.

## Prerequisites

- Railway account (https://railway.app)
- Railway CLI installed (`npm i -g @railway/cli`)
- Domain name configured
- Google Cloud Console project (for SSO)

## Architecture on Railway

```
Railway Project
├── ZITADEL Service (Docker)
│   └── PostgreSQL (Railway Addon)
├── Login UI Service (Docker)
└── (Optional) Your App Services
```

## Step 1: Initial Setup

### Login to Railway

```bash
railway login
```

### Create New Project

```bash
# Create a new project
railway init

# Or link to existing project
railway link
```

## Step 2: Deploy PostgreSQL

Railway has a built-in PostgreSQL addon:

1. Go to your Railway project dashboard
2. Click "New Service" → "Database" → "PostgreSQL"
3. Railway provides `DATABASE_URL` automatically

Note the connection details for ZITADEL configuration.

## Step 3: Deploy ZITADEL

### Create ZITADEL Service

```bash
cd zitadel-setup
railway up
```

Railway will auto-detect the `docker-compose.yml` and ask which service to deploy.
Select `zitadel`.

### Configure Environment Variables

In Railway dashboard, set these variables for the ZITADEL service:

```bash
# Database (use Railway's DATABASE_URL parsing or set manually)
ZITADEL_DATABASE_POSTGRES_HOST=<from-railway-postgres>
ZITADEL_DATABASE_POSTGRES_PORT=5432
ZITADEL_DATABASE_POSTGRES_DATABASE=zitadel
ZITADEL_DATABASE_POSTGRES_USER_USERNAME=<from-railway>
ZITADEL_DATABASE_POSTGRES_USER_PASSWORD=<from-railway>
ZITADEL_DATABASE_POSTGRES_USER_SSL_MODE=require
ZITADEL_DATABASE_POSTGRES_ADMIN_USERNAME=<from-railway>
ZITADEL_DATABASE_POSTGRES_ADMIN_PASSWORD=<from-railway>
ZITADEL_DATABASE_POSTGRES_ADMIN_SSL_MODE=require

# External Access
ZITADEL_EXTERNALDOMAIN=auth.yourdomain.com
ZITADEL_EXTERNALSECURE=true
ZITADEL_EXTERNALPORT=443

# Security
ZITADEL_MASTERKEY=<generate-with-openssl-rand-base64-32>

# Initial Admin
ZITADEL_FIRSTINSTANCE_ORG_NAME=YourCompany
ZITADEL_FIRSTINSTANCE_ORG_HUMAN_USERNAME=admin@yourdomain.com
ZITADEL_FIRSTINSTANCE_ORG_HUMAN_PASSWORD=<secure-password>
```

### Generate Master Key

```bash
openssl rand -base64 32
```

Copy the output to `ZITADEL_MASTERKEY`.

### Configure Custom Domain

1. In Railway dashboard, go to ZITADEL service settings
2. Add custom domain: `auth.yourdomain.com`
3. Railway provides the CNAME record to add to your DNS
4. Wait for SSL certificate provisioning

## Step 4: Deploy Login UI

### Build and Deploy

```bash
cd login-ui
railway up
```

### Configure Environment Variables

```bash
VITE_ZITADEL_AUTHORITY=https://auth.yourdomain.com
VITE_ZITADEL_CLIENT_ID=<from-zitadel-console>
VITE_REDIRECT_URI=https://login.yourdomain.com/callback
VITE_POST_LOGOUT_REDIRECT_URI=https://login.yourdomain.com
```

### Configure Custom Domain

Add custom domain: `login.yourdomain.com`

## Step 5: Configure ZITADEL Console

1. Access ZITADEL Console at `https://auth.yourdomain.com/ui/console`
2. Login with admin credentials
3. Create Project for your applications
4. Create OIDC Application for login UI (PKCE, Web)
5. Set redirect URIs
6. Copy Client ID to login UI environment variables

## Step 6: Configure Google SSO

See [GOOGLE-SSO-SETUP.md](./GOOGLE-SSO-SETUP.md) for detailed instructions.

## Environment Variables Reference

### ZITADEL Service

| Variable | Description | Example |
|----------|-------------|---------|
| `ZITADEL_EXTERNALDOMAIN` | Public domain | `auth.example.com` |
| `ZITADEL_EXTERNALSECURE` | Use HTTPS | `true` |
| `ZITADEL_EXTERNALPORT` | Public port | `443` |
| `ZITADEL_MASTERKEY` | Encryption key (32 bytes base64) | Generate with openssl |
| `ZITADEL_DATABASE_POSTGRES_*` | Database connection | From Railway PostgreSQL |

### Login UI Service

| Variable | Description | Example |
|----------|-------------|---------|
| `VITE_ZITADEL_AUTHORITY` | ZITADEL server URL | `https://auth.example.com` |
| `VITE_ZITADEL_CLIENT_ID` | OIDC Client ID | From ZITADEL Console |
| `VITE_REDIRECT_URI` | Callback URL | `https://login.example.com/callback` |

## Updating Services

```bash
# Deploy updates
railway up

# View logs
railway logs

# Open dashboard
railway open
```

## Rollback

Railway keeps deployment history. To rollback:

1. Go to service in Railway dashboard
2. Click "Deployments"
3. Find the working deployment
4. Click "Rollback"

## Monitoring

### Health Checks

ZITADEL exposes health endpoints:
- `/healthz` - Basic health
- `/ready` - Ready check

Configure in Railway service settings.

### Logs

```bash
# Stream logs
railway logs -f

# View in dashboard
railway open
```

## Backup

### Database Backup

Railway PostgreSQL includes automatic backups. For manual backup:

```bash
# Connect to Railway PostgreSQL
railway connect postgres

# Run pg_dump
pg_dump -Fc zitadel > backup.dump
```

### Configuration Backup

Keep your `.env` file and Railway configuration in a secure location.

## Troubleshooting

### ZITADEL won't start

1. Check logs: `railway logs`
2. Verify DATABASE_URL is correct
3. Ensure MASTERKEY is exactly 32 bytes base64
4. Check PostgreSQL is accessible

### SSL/TLS Issues

1. Ensure `ZITADEL_EXTERNALSECURE=true`
2. Verify custom domain SSL is provisioned
3. Check CNAME records in DNS

### Login Redirect Issues

1. Verify redirect URIs match exactly
2. Check OIDC client configuration
3. Ensure EXTERNALDOMAIN matches actual domain

### Database Connection Failed

1. Check Railway PostgreSQL is running
2. Verify SSL mode is `require` for Railway
3. Test connection with `railway connect postgres`

## Cost Estimation

Railway pricing (as of 2024):
- Starter: $5/month + usage
- ZITADEL: ~$10-20/month (depends on traffic)
- PostgreSQL: ~$5-15/month
- Login UI: ~$5-10/month

Total estimated: ~$20-50/month for small-medium deployment

## Security Checklist

- [ ] Changed default admin password
- [ ] ZITADEL_MASTERKEY is unique and secure
- [ ] EXTERNALSECURE=true
- [ ] Database uses SSL
- [ ] MFA enabled for admin accounts
- [ ] Custom domain with valid SSL
- [ ] Audit logging enabled
- [ ] Regular backup schedule
