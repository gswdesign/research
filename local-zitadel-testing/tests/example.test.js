/**
 * Example tests demonstrating Zitadel token usage
 *
 * Run with:
 *   # Against mock server
 *   MOCK_URL=http://localhost:9000 npm test
 *
 *   # Against local Zitadel
 *   ZITADEL_URL=http://localhost:8080 npm test
 */

const assert = require('assert');
const https = require('https');
const http = require('http');

// Configuration
const MOCK_URL = process.env.MOCK_URL || 'http://localhost:9000';
const ZITADEL_URL = process.env.ZITADEL_URL;
const AUTH_TOKEN = process.env.AUTH_TOKEN;

/**
 * Get a test token from mock server
 */
async function getMockToken(options = {}) {
  const url = new URL('/test/token', MOCK_URL);

  return new Promise((resolve, reject) => {
    const req = http.request(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }
    }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const json = JSON.parse(data);
          resolve(json.access_token);
        } catch (e) {
          reject(new Error('Failed to parse token response'));
        }
      });
    });

    req.on('error', reject);
    req.write(JSON.stringify({
      client_id: options.clientId || 'test-client',
      email: options.email || 'test@local.test',
      name: options.name || 'Test User',
      scope: options.scope || 'openid profile email'
    }));
    req.end();
  });
}

/**
 * Verify a token with userinfo endpoint
 */
async function verifyToken(token, baseUrl) {
  const url = new URL('/oidc/v1/userinfo', baseUrl);
  const protocol = url.protocol === 'https:' ? https : http;

  return new Promise((resolve, reject) => {
    const req = protocol.request(url, {
      headers: { 'Authorization': `Bearer ${token}` }
    }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        if (res.statusCode === 200) {
          resolve(JSON.parse(data));
        } else {
          reject(new Error(`Userinfo failed: ${res.statusCode}`));
        }
      });
    });

    req.on('error', reject);
    req.end();
  });
}

/**
 * Decode JWT without verification (for testing claims)
 */
function decodeJwt(token) {
  const [, payload] = token.split('.');
  const decoded = Buffer.from(payload, 'base64url').toString();
  return JSON.parse(decoded);
}

// Tests
describe('Zitadel Token Tests', function() {
  this.timeout(10000);

  describe('Mock Server', function() {
    it('should get a token from mock server', async function() {
      const token = await getMockToken();
      assert(token, 'Token should not be empty');
      assert(token.split('.').length === 3, 'Token should be a JWT');
    });

    it('should include custom claims in token', async function() {
      const token = await getMockToken({
        email: 'custom@example.com',
        name: 'Custom User'
      });

      const claims = decodeJwt(token);
      assert.strictEqual(claims.email, 'custom@example.com');
      assert.strictEqual(claims.name, 'Custom User');
    });

    it('should verify token with userinfo endpoint', async function() {
      const token = await getMockToken();
      const userinfo = await verifyToken(token, MOCK_URL);

      assert(userinfo.sub, 'Userinfo should have sub claim');
      assert(userinfo.email, 'Userinfo should have email');
    });
  });

  describe('Token Validation', function() {
    it('should have valid JWT structure', async function() {
      const token = await getMockToken();
      const parts = token.split('.');

      assert.strictEqual(parts.length, 3, 'JWT should have 3 parts');

      const header = JSON.parse(Buffer.from(parts[0], 'base64url').toString());
      assert.strictEqual(header.alg, 'RS256', 'Should use RS256 algorithm');
    });

    it('should have correct expiration', async function() {
      const token = await getMockToken();
      const claims = decodeJwt(token);

      const now = Math.floor(Date.now() / 1000);
      assert(claims.exp > now, 'Token should not be expired');
      assert(claims.exp <= now + 7200, 'Token should expire within 2 hours');
    });
  });
});

// Simple test runner if not using a framework
if (require.main === module) {
  console.log('Running basic tests...\n');

  (async () => {
    try {
      // Test 1: Get mock token
      console.log('Test 1: Get mock token');
      const token = await getMockToken();
      console.log('  ✓ Got token:', token.substring(0, 50) + '...\n');

      // Test 2: Decode and check claims
      console.log('Test 2: Decode JWT claims');
      const claims = decodeJwt(token);
      console.log('  ✓ Claims:', JSON.stringify(claims, null, 2), '\n');

      // Test 3: Verify with userinfo
      console.log('Test 3: Verify with userinfo endpoint');
      const userinfo = await verifyToken(token, MOCK_URL);
      console.log('  ✓ Userinfo:', JSON.stringify(userinfo, null, 2), '\n');

      console.log('All tests passed!');
    } catch (err) {
      console.error('Test failed:', err.message);
      console.error('\nMake sure the mock server is running:');
      console.error('  cd mocks && npm start');
      process.exit(1);
    }
  })();
}
