"""
Example Python tests demonstrating Zitadel token usage.

Run with:
    # Start mock server first
    cd mocks && npm start

    # Then run tests
    python example_test.py

    # Or with pytest
    pytest example_test.py -v
"""

import os
import json
import base64
import urllib.request
import urllib.error
from typing import Optional, Dict, Any


# Configuration
MOCK_URL = os.environ.get("MOCK_URL", "http://localhost:9000")
ZITADEL_URL = os.environ.get("ZITADEL_URL", "http://localhost:8080")
AUTH_TOKEN = os.environ.get("AUTH_TOKEN")


def get_mock_token(
    email: str = "test@local.test",
    name: str = "Test User",
    client_id: str = "test-client",
    scope: str = "openid profile email"
) -> str:
    """Get a token from the mock OIDC server."""
    url = f"{MOCK_URL}/test/token"
    data = json.dumps({
        "client_id": client_id,
        "email": email,
        "name": name,
        "scope": scope
    }).encode()

    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"}
    )

    with urllib.request.urlopen(req, timeout=5) as response:
        result = json.loads(response.read())
        return result["access_token"]


def get_service_token(
    pat: Optional[str] = None,
    key_file: Optional[str] = None,
    zitadel_url: Optional[str] = None
) -> str:
    """Get a token using service account credentials."""
    pat = pat or os.environ.get("ZITADEL_PAT")

    if pat:
        return pat

    # For JWT key auth, use the shell script or implement JWT signing
    raise ValueError("Set ZITADEL_PAT or use get_mock_token() for testing")


def decode_jwt(token: str) -> Dict[str, Any]:
    """Decode a JWT without verification (for testing only)."""
    parts = token.split(".")
    if len(parts) != 3:
        raise ValueError("Invalid JWT format")

    # Add padding if needed
    payload = parts[1]
    padding = 4 - len(payload) % 4
    if padding != 4:
        payload += "=" * padding

    decoded = base64.urlsafe_b64decode(payload)
    return json.loads(decoded)


def verify_token(token: str, base_url: str) -> Dict[str, Any]:
    """Verify token by calling userinfo endpoint."""
    url = f"{base_url}/oidc/v1/userinfo"
    req = urllib.request.Request(
        url,
        headers={"Authorization": f"Bearer {token}"}
    )

    with urllib.request.urlopen(req, timeout=5) as response:
        return json.loads(response.read())


class TestMockServer:
    """Tests using the mock OIDC server."""

    def test_get_token(self):
        """Should get a valid JWT from mock server."""
        token = get_mock_token()
        assert token
        assert len(token.split(".")) == 3

    def test_token_claims(self):
        """Should have correct claims in token."""
        token = get_mock_token(email="custom@test.com", name="Custom User")
        claims = decode_jwt(token)

        assert claims["email"] == "custom@test.com"
        assert claims["name"] == "Custom User"
        assert "sub" in claims
        assert "iss" in claims

    def test_verify_with_userinfo(self):
        """Should be able to verify token with userinfo endpoint."""
        token = get_mock_token()
        userinfo = verify_token(token, MOCK_URL)

        assert "sub" in userinfo
        assert "email" in userinfo

    def test_token_expiration(self):
        """Token should have valid expiration."""
        import time

        token = get_mock_token()
        claims = decode_jwt(token)

        now = int(time.time())
        assert claims["exp"] > now, "Token should not be expired"
        assert claims["exp"] <= now + 7200, "Token should expire within 2 hours"


class TestTokenHelper:
    """Helper class for managing test tokens."""

    def __init__(self, use_mock: bool = True):
        self.use_mock = use_mock
        self._cached_token: Optional[str] = None

    def get_token(self, **kwargs) -> str:
        """Get a token for testing."""
        if self._cached_token:
            # Check if still valid
            try:
                claims = decode_jwt(self._cached_token)
                import time
                if claims["exp"] > time.time() + 60:
                    return self._cached_token
            except Exception:
                pass

        if self.use_mock:
            self._cached_token = get_mock_token(**kwargs)
        else:
            self._cached_token = get_service_token()

        return self._cached_token

    def get_auth_header(self, **kwargs) -> Dict[str, str]:
        """Get authorization header for API calls."""
        token = self.get_token(**kwargs)
        return {"Authorization": f"Bearer {token}"}


# Usage example
def example_api_call():
    """Example of making an authenticated API call."""
    helper = TestTokenHelper(use_mock=True)

    # Your API endpoint
    api_url = "https://your-api.example.com/protected/endpoint"

    # Make authenticated request
    headers = helper.get_auth_header()
    # req = urllib.request.Request(api_url, headers=headers)
    # response = urllib.request.urlopen(req)

    print(f"Would call {api_url}")
    print(f"With headers: {headers}")


if __name__ == "__main__":
    print("Running basic tests...\n")

    try:
        # Test 1: Get mock token
        print("Test 1: Get mock token")
        token = get_mock_token()
        print(f"  ✓ Got token: {token[:50]}...\n")

        # Test 2: Decode and check claims
        print("Test 2: Decode JWT claims")
        claims = decode_jwt(token)
        print(f"  ✓ Claims: {json.dumps(claims, indent=2)}\n")

        # Test 3: Verify with userinfo
        print("Test 3: Verify with userinfo endpoint")
        userinfo = verify_token(token, MOCK_URL)
        print(f"  ✓ Userinfo: {json.dumps(userinfo, indent=2)}\n")

        # Test 4: Test helper class
        print("Test 4: Token helper class")
        helper = TestTokenHelper()
        headers = helper.get_auth_header()
        print(f"  ✓ Auth header: {headers}\n")

        print("All tests passed!")

    except urllib.error.URLError as e:
        print(f"Connection error: {e}")
        print("\nMake sure the mock server is running:")
        print("  cd mocks && npm start")
        exit(1)
    except Exception as e:
        print(f"Test failed: {e}")
        exit(1)
