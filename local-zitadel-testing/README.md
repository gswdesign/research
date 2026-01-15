# Local Zitadel Testing

This folder provides solutions for automated testing with Zitadel authentication without manual login/2FA.

## The Problem

When using `auth.vmiapps.com` (production Zitadel with PKCE + 2FA):
- Interactive login required
- 2FA blocks automation
- Cloudflare Workers add complexity
- Cannot run automated tests

## Solutions

### 1. Local Zitadel Instance (Recommended for Development)
Run a local Zitadel with Docker - no 2FA, full control.

```bash
cd docker
docker-compose up -d
```

See `docker/README.md` for setup details.

### 2. Service Account / Machine User (For Production Testing)
Create a service account on `auth.vmiapps.com` with:
- Personal Access Token (PAT), or
- JWT Profile (client credentials)

No interactive login required. See `scripts/README.md`.

### 3. Mock OIDC Server (For Unit Tests)
Lightweight mock that returns valid-looking tokens without any real auth.

```bash
cd mocks
npm install
npm start
```

### 4. Token Caching
Scripts to cache and refresh tokens for test runs.

## Quick Start

```bash
# Option 1: Local Zitadel (full integration testing)
./scripts/setup-local-zitadel.sh

# Option 2: Mock server (unit tests)
cd mocks && npm start

# Option 3: Use service account token (against real Zitadel)
export ZITADEL_SERVICE_TOKEN=$(./scripts/get-service-token.sh)
```

## Directory Structure

```
local-zitadel-testing/
├── docker/          # Docker Compose for local Zitadel
├── scripts/         # Setup and token management scripts
├── mocks/           # Mock OIDC server for offline testing
├── tokens/          # Token cache (gitignored)
└── tests/           # Example test files
```

## Choosing the Right Approach

| Approach | Use Case | Pros | Cons |
|----------|----------|------|------|
| Local Zitadel | Integration tests | Real behavior | Heavier setup |
| Service Account | CI/CD, E2E tests | Works with prod | Need admin access |
| Mock Server | Unit tests | Fast, no deps | Not real auth |
| Token Cache | Quick iteration | Simple | Tokens expire |
