/**
 * Mock OIDC Server
 *
 * Simulates Zitadel OIDC endpoints for offline testing.
 * Returns valid JWT tokens without real authentication.
 *
 * Usage:
 *   npm start
 *   # Server runs on http://localhost:9000
 */

const express = require('express');
const jwt = require('jsonwebtoken');
const { v4: uuidv4 } = require('uuid');
const crypto = require('crypto');

const app = express();
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

const PORT = process.env.PORT || 9000;
const ISSUER = process.env.ISSUER || `http://localhost:${PORT}`;

// Mock RSA key pair (for development only!)
const PRIVATE_KEY = `-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEA2Z3qX2BTLS4e0rYtOz5M4VaJKh7v2p5XhQfMl0TbTiMH1nlY
mLt8QS1L0bXMzMFwq8rX8OFNXcrLj7tLh3qTbzjadMPvo3dPHxTv0vXgQ7LD6O8u
M6knXsLJj7N0aPgPpw3IZhHB2Y1KQ3sAY2VtLBhm/b9X1U6rHWWLQkxJKVNz3eQR
YZzM7TYNDgZUEP2Q3S5LLqPv5X4t/wdPzMJU7n7YB7BLYG1tL5k5pPZfm5T5eJwA
K8eOSE9GvP+pX3eZqvJ/xTLWCfCvwDLvYQ0dULFF7nF8jL6X3Q2o9X1XEhZnLqCD
FU2jQu1T1oZzQ3mXLzECLvJStnSBKlmHZTf/awIDAQABAoIBAC5RgZ+hBx7xHnFZ
nQmY03fr3EXuHlqWHhyfEzUh5kP9EnRCvPqMQMdC2YYz/1ob7Y6bhFP6NwYm9GBv
7X8bhEIEqQz8VuKb/0JmklMloJfvQRKfy2BJFF4QG/pkbhJFfpfSVuoJ5tLBMFyH
7RVMQ5dXtoV9aWbPj9NO5E5f3T5lzqTzLHizQ0cy8vi2RyFT5jlXmqJKyqSg9hig
YXNh5T3f5K1o4X1v9L3h5sUP2a7qS+MHSOZ+EjfpLQEZgvw/USpXXQKn5J2Wamaf
kD4f5M6EammJr0kQbOz8+0D+V//ZnNqpHgc3/5nvB1z7HaKr2EW9ilYJNeT/KQHR
MXA/yMECgYEA8PJYQ7dcI3M9KNTV5ip06J5v3xL5FCR/P2M2XYqLVh8BRz6IVfFE
M0cC3XbPO+FmtEExhztG4bYHZbW8KPCRhFPvjqCqqE/+qy+TvJLJrMvaFOFXqC5n
VqSRz9FI7nMJHH2RYq3i5s5nyH9g9Ehc4TwirkGL6jlALI0BLmZQBGsCgYEA5wHT
UzA9n/FISnm9MJqLKl1KAfynFJQjvKBFXaQOFXClmyjSS8TYdXl1wvPBfSn/KTBH
Fi2D0v5p+BXO0Qo+oSJ0XLw6L8c/1T6LqF6R9jRKCDGnrVCuG9DfVDGOJEz1BnCL
f/bZgZGEm7bVPNLcS2NJ23q2EUlPV/hEz0/lJEECgYEA1vjCn5HlQR/PN4j35Cix
dganPDmE9tPFyczI0GvEetIzlXCNpXPzPCELhngr3D8CB26bxzqvRP0VN9lhMUaM
MAQaKICjKqaBhBPvGF5rPMGRpKJFbuHrLzLxcw6NKtfPT0LyY0r+T0E5SrFltRLq
IQFHB4CJ/N+m3lq7hlnJE0sCgYEAkT0MPLqHNVVfkSLVL7M1K3gd7QUXA3n2VfCz
LwW0TFf0Td5K4fIRbLmPYN0IkLhL8TzNVMXwEgKLqT7q1c9D2gkFIqdKcQ7NXqAP
CGL5UndTfEk3aWLTpRDRrE4p4LnmLhYV8qLW7GNTxOxJ7ILjf1v1K7a6oA3TZOe5
I8iKYwECgYBj0T+S1jVjLGJjzgME7RSEC8FJvBm7a8FYNaELNkLTL7vLIqRVPVz+
WAV0Drv9nuFNcRa2DP3CJ5adqB1Gm+8K7wZSdVnJuQlasjL/Qm/h1VLYLz8pXvdF
OhlaHb/fIVpDij0+R/xjnfHPjXvJz7GJBkFtP3ELBxJrLVrBKvAnkQ==
-----END RSA PRIVATE KEY-----`;

const PUBLIC_KEY = `-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA2Z3qX2BTLS4e0rYtOz5M
4VaJKh7v2p5XhQfMl0TbTiMH1nlYmLt8QS1L0bXMzMFwq8rX8OFNXcrLj7tLh3qT
bzjadMPvo3dPHxTv0vXgQ7LD6O8uM6knXsLJj7N0aPgPpw3IZhHB2Y1KQ3sAY2Vt
LBhm/b9X1U6rHWWLQkxJKVNz3eQRYZzM7TYNDgZUEP2Q3S5LLqPv5X4t/wdPzMJU
7n7YB7BLYG1tL5k5pPZfm5T5eJwAK8eOSE9GvP+pX3eZqvJ/xTLWCfCvwDLvYQ0d
ULFF7nF8jL6X3Q2o9X1XEhZnLqCDFU2jQu1T1oZzQ3mXLzECLvJStnSBKlmHZTf/
awIDAQAB
-----END PUBLIC KEY-----`;

const KEY_ID = 'mock-key-1';

// Store for PKCE and auth codes
const authCodes = new Map();
const pkceStore = new Map();

// OIDC Discovery
app.get('/.well-known/openid-configuration', (req, res) => {
  res.json({
    issuer: ISSUER,
    authorization_endpoint: `${ISSUER}/oauth/v2/authorize`,
    token_endpoint: `${ISSUER}/oauth/v2/token`,
    userinfo_endpoint: `${ISSUER}/oidc/v1/userinfo`,
    jwks_uri: `${ISSUER}/.well-known/jwks.json`,
    response_types_supported: ['code', 'token', 'id_token'],
    subject_types_supported: ['public'],
    id_token_signing_alg_values_supported: ['RS256'],
    scopes_supported: ['openid', 'profile', 'email', 'offline_access'],
    token_endpoint_auth_methods_supported: ['none', 'client_secret_basic', 'client_secret_post'],
    code_challenge_methods_supported: ['S256', 'plain']
  });
});

// JWKS endpoint
app.get('/.well-known/jwks.json', (req, res) => {
  const publicKeyBuffer = crypto.createPublicKey(PUBLIC_KEY);
  const jwk = publicKeyBuffer.export({ format: 'jwk' });

  res.json({
    keys: [{
      ...jwk,
      kid: KEY_ID,
      use: 'sig',
      alg: 'RS256'
    }]
  });
});

// Authorization endpoint (simplified - auto-approves)
app.get('/oauth/v2/authorize', (req, res) => {
  const {
    client_id,
    redirect_uri,
    response_type,
    scope,
    state,
    code_challenge,
    code_challenge_method,
    nonce
  } = req.query;

  if (response_type !== 'code') {
    return res.status(400).json({ error: 'unsupported_response_type' });
  }

  // Generate auth code
  const code = uuidv4();

  // Store auth code with metadata
  authCodes.set(code, {
    client_id,
    redirect_uri,
    scope,
    nonce,
    created: Date.now()
  });

  // Store PKCE challenge
  if (code_challenge) {
    pkceStore.set(code, {
      challenge: code_challenge,
      method: code_challenge_method || 'plain'
    });
  }

  // Redirect back with code
  const redirectUrl = new URL(redirect_uri);
  redirectUrl.searchParams.set('code', code);
  if (state) redirectUrl.searchParams.set('state', state);

  res.redirect(redirectUrl.toString());
});

// Token endpoint
app.post('/oauth/v2/token', (req, res) => {
  const {
    grant_type,
    code,
    redirect_uri,
    client_id,
    code_verifier,
    refresh_token
  } = req.body;

  // Handle refresh token
  if (grant_type === 'refresh_token') {
    return generateTokens(res, { client_id, scope: 'openid profile email' });
  }

  // Handle authorization code
  if (grant_type !== 'authorization_code') {
    return res.status(400).json({ error: 'unsupported_grant_type' });
  }

  const authCode = authCodes.get(code);
  if (!authCode) {
    return res.status(400).json({ error: 'invalid_grant', error_description: 'Invalid authorization code' });
  }

  // Verify PKCE
  const pkce = pkceStore.get(code);
  if (pkce) {
    let valid = false;
    if (pkce.method === 'plain') {
      valid = code_verifier === pkce.challenge;
    } else if (pkce.method === 'S256') {
      const hash = crypto
        .createHash('sha256')
        .update(code_verifier)
        .digest('base64url');
      valid = hash === pkce.challenge;
    }

    if (!valid) {
      return res.status(400).json({ error: 'invalid_grant', error_description: 'PKCE verification failed' });
    }
  }

  // Clean up
  authCodes.delete(code);
  pkceStore.delete(code);

  generateTokens(res, authCode);
});

function generateTokens(res, authCode) {
  const now = Math.floor(Date.now() / 1000);
  const userId = uuidv4();

  // Generate ID token
  const idToken = jwt.sign({
    iss: ISSUER,
    sub: userId,
    aud: authCode.client_id,
    exp: now + 3600,
    iat: now,
    nonce: authCode.nonce,
    email: 'test@local.test',
    email_verified: true,
    name: 'Test User',
    preferred_username: 'testuser'
  }, PRIVATE_KEY, { algorithm: 'RS256', keyid: KEY_ID });

  // Generate access token
  const accessToken = jwt.sign({
    iss: ISSUER,
    sub: userId,
    aud: authCode.client_id,
    exp: now + 3600,
    iat: now,
    scope: authCode.scope || 'openid profile email'
  }, PRIVATE_KEY, { algorithm: 'RS256', keyid: KEY_ID });

  // Generate refresh token
  const refreshToken = uuidv4();

  res.json({
    access_token: accessToken,
    token_type: 'Bearer',
    expires_in: 3600,
    id_token: idToken,
    refresh_token: refreshToken,
    scope: authCode.scope || 'openid profile email'
  });
}

// Userinfo endpoint
app.get('/oidc/v1/userinfo', (req, res) => {
  const auth = req.headers.authorization;
  if (!auth || !auth.startsWith('Bearer ')) {
    return res.status(401).json({ error: 'invalid_token' });
  }

  // Verify token (basic check)
  const token = auth.substring(7);
  try {
    const decoded = jwt.verify(token, PUBLIC_KEY, { algorithms: ['RS256'] });
    res.json({
      sub: decoded.sub,
      email: 'test@local.test',
      email_verified: true,
      name: 'Test User',
      preferred_username: 'testuser'
    });
  } catch (err) {
    res.status(401).json({ error: 'invalid_token' });
  }
});

// Quick token endpoint (bypass PKCE for testing)
app.post('/test/token', (req, res) => {
  const { client_id, scope, user_id, email, name } = req.body;

  const now = Math.floor(Date.now() / 1000);
  const userId = user_id || uuidv4();

  const accessToken = jwt.sign({
    iss: ISSUER,
    sub: userId,
    aud: client_id || 'test-client',
    exp: now + 3600,
    iat: now,
    scope: scope || 'openid profile email',
    email: email || 'test@local.test',
    name: name || 'Test User'
  }, PRIVATE_KEY, { algorithm: 'RS256', keyid: KEY_ID });

  const idToken = jwt.sign({
    iss: ISSUER,
    sub: userId,
    aud: client_id || 'test-client',
    exp: now + 3600,
    iat: now,
    email: email || 'test@local.test',
    email_verified: true,
    name: name || 'Test User',
    preferred_username: (email || 'test@local.test').split('@')[0]
  }, PRIVATE_KEY, { algorithm: 'RS256', keyid: KEY_ID });

  res.json({
    access_token: accessToken,
    id_token: idToken,
    token_type: 'Bearer',
    expires_in: 3600
  });
});

// Health check
app.get('/health', (req, res) => {
  res.json({ status: 'ok', issuer: ISSUER });
});

app.listen(PORT, () => {
  console.log(`Mock OIDC Server running at ${ISSUER}`);
  console.log('');
  console.log('Endpoints:');
  console.log(`  Discovery: ${ISSUER}/.well-known/openid-configuration`);
  console.log(`  Authorize: ${ISSUER}/oauth/v2/authorize`);
  console.log(`  Token:     ${ISSUER}/oauth/v2/token`);
  console.log(`  Userinfo:  ${ISSUER}/oidc/v1/userinfo`);
  console.log('');
  console.log('Quick token (no PKCE):');
  console.log(`  POST ${ISSUER}/test/token`);
  console.log('  Body: { "client_id": "your-app", "email": "user@test.com" }');
});
