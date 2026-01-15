# Token Scripts

Scripts for getting tokens without interactive login.

## For Production (auth.vmiapps.com)

### Option 1: Personal Access Token (PAT) - Simplest

1. Login to https://auth.vmiapps.com/ui/console
2. Go to Users > Service Users > Create New
3. Name: `test-automation` (or similar)
4. Click on the new user > Personal Access Tokens > Create
5. Copy the token

```bash
export ZITADEL_PAT="your-token-here"
export ZITADEL_URL="https://auth.vmiapps.com"
./get-service-token.sh
```

### Option 2: JWT Key (More Secure)

1. Login to console
2. Create Service User
3. Go to Keys > Create Key
4. Download the JSON key file

```bash
export ZITADEL_KEY_FILE="/path/to/downloaded-key.json"
export ZITADEL_URL="https://auth.vmiapps.com"
./get-service-token.sh
```

## For Local Testing

### Local Zitadel

```bash
# Start local Zitadel first
./setup-local-zitadel.sh

# Then create service user via console and get token
export ZITADEL_PAT="local-pat"
./get-service-token.sh
```

### Mock Server (Fastest)

```bash
# Start mock server
cd ../mocks && npm start &

# Get instant tokens
./get-mock-token.sh
./get-mock-token.sh --email custom@test.com
```

## Using in Tests

```bash
# In your test setup
export AUTH_TOKEN=$(./get-service-token.sh)

# Or for mock
export AUTH_TOKEN=$(./get-mock-token.sh)

# Use in API calls
curl -H "Authorization: Bearer $AUTH_TOKEN" https://your-api.com/endpoint
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `ZITADEL_URL` | Zitadel instance URL | `http://localhost:8080` |
| `ZITADEL_PAT` | Personal Access Token | - |
| `ZITADEL_KEY_FILE` | Path to JWT key JSON | - |
| `TOKEN_CACHE` | Path to cache tokens | `../tokens/cached-token.json` |
| `MOCK_URL` | Mock server URL | `http://localhost:9000` |
