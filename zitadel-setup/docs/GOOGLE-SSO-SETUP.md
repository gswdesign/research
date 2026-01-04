# Google SSO Setup Guide

Configure Google as an identity provider in ZITADEL for "Login with Google" functionality.

## Prerequisites

- ZITADEL instance running and accessible
- Google Cloud Console account
- Admin access to ZITADEL Console

## Step 1: Google Cloud Console Setup

### 1.1 Create or Select Project

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Click project selector dropdown
3. Click "New Project" or select existing
4. Name your project (e.g., "YourApp Auth")
5. Click "Create"

### 1.2 Configure OAuth Consent Screen

1. Go to **APIs & Services** → **OAuth consent screen**
2. Select **External** (unless you have Google Workspace)
3. Click "Create"

Fill in the form:

| Field | Value |
|-------|-------|
| App name | Your App Name |
| User support email | support@yourdomain.com |
| App logo | Upload your logo (optional) |
| App domain | yourdomain.com |
| Developer contact email | dev@yourdomain.com |

4. Click "Save and Continue"

### 1.3 Configure Scopes

1. Click "Add or Remove Scopes"
2. Select these scopes:
   - `openid`
   - `email`
   - `profile`
3. Click "Update"
4. Click "Save and Continue"

### 1.4 Add Test Users (Development)

For development/testing before verification:

1. Click "Add Users"
2. Add email addresses of test users
3. Click "Save and Continue"

Note: In production, submit app for verification to allow all users.

### 1.5 Create OAuth Credentials

1. Go to **APIs & Services** → **Credentials**
2. Click **"+ Create Credentials"** → **"OAuth client ID"**
3. Select **"Web application"**
4. Name it (e.g., "ZITADEL SSO")

**Configure Authorized redirect URIs:**

Add these URIs based on your ZITADEL domain:

```
https://auth.yourdomain.com/ui/login/login/externalidp/callback
```

For local development, also add:
```
http://localhost:8080/ui/login/login/externalidp/callback
```

5. Click "Create"
6. **Copy the Client ID and Client Secret** - you'll need these next

## Step 2: ZITADEL Configuration

### 2.1 Access ZITADEL Console

1. Go to `https://auth.yourdomain.com/ui/console`
2. Login with admin account

### 2.2 Navigate to Identity Providers

For **instance-level** (all organizations):
1. Click your profile icon → "Instance Settings"
2. Go to "Identity Providers"

For **organization-level** (specific org):
1. Select the organization
2. Go to "Settings" → "Identity Providers"

### 2.3 Add Google Provider

1. Click on the **Google** template card
2. Fill in the configuration:

| Field | Value |
|-------|-------|
| Name | Google |
| Client ID | Your Google Client ID |
| Client Secret | Your Google Client Secret |
| Scopes | openid, email, profile |

3. Configure options:
   - **Link existing users**: ✅ Enabled (links by email)
   - **Auto-creation**: Choose based on your needs
   - **Account creation allowed**: ✅ If you want new accounts

4. Click "Save"

### 2.4 Activate the Provider

After saving, the provider appears in the list.

1. Ensure it's **enabled** (toggle on)
2. The provider will now appear on your login screen

## Step 3: Test the Integration

### 3.1 Test Login Flow

1. Open an incognito/private browser window
2. Go to your login page
3. You should see "Continue with Google" button
4. Click it and verify:
   - Redirect to Google sign-in
   - After Google auth, redirect back to ZITADEL
   - User is logged in or account is linked

### 3.2 Verify User in Console

1. Go to ZITADEL Console → Users
2. Find the user who logged in with Google
3. Verify their profile shows Google as linked identity

## Step 4: Custom Login UI Integration

If using the custom login UI, the Google SSO is initiated via ZITADEL's OIDC flow.

### Option A: Use ZITADEL's Built-in Flow

The `loginWithGoogle()` function in the auth library redirects to ZITADEL, which shows the Google button:

```typescript
// In lib/auth.ts
export async function loginWithGoogle(): Promise<void> {
  const manager = getUserManager()
  // ZITADEL handles showing Google option
  await manager.signinRedirect()
}
```

### Option B: Direct IdP Redirect

To skip ZITADEL login page and go directly to Google:

```typescript
export async function loginWithGoogle(idpId: string): Promise<void> {
  const manager = getUserManager()
  await manager.signinRedirect({
    extraQueryParams: {
      idp: idpId, // Your Google IdP ID from ZITADEL
    },
  })
}
```

Get the IdP ID from ZITADEL Console → Identity Providers → Google → copy the ID from the URL.

## Troubleshooting

### "Access blocked: This app's request is invalid"

**Cause**: Redirect URI mismatch

**Solution**:
1. Check exact redirect URI in Google Console
2. Must match exactly including trailing slash
3. Ensure protocol (http/https) matches

### "User not found" after Google login

**Cause**: Auto-creation disabled and user doesn't exist

**Solution**:
1. Enable "Account creation allowed" in ZITADEL
2. Or pre-create users before they log in

### Google login works but user has no roles

**Cause**: Auto-provisioning doesn't assign roles

**Solution**:
1. Use ZITADEL Actions to auto-assign roles
2. Or manually assign roles after first login
3. Or use ZITADEL's organization auto-assignment

### "Error 400: redirect_uri_mismatch"

**Cause**: The redirect URI in the request doesn't match Google's configuration

**Solution**:
1. Copy the exact URI from the error message
2. Add it to Google Console authorized redirect URIs
3. Wait a few minutes for propagation

## Production Checklist

- [ ] App verified with Google (if more than 100 users)
- [ ] Production redirect URI configured
- [ ] Logo and branding set in OAuth consent screen
- [ ] Privacy policy and Terms of Service URLs added
- [ ] Test with real users before launch
- [ ] Removed localhost URIs from production credentials

## Security Considerations

1. **Client Secret**: Never expose in client-side code
2. **Scopes**: Request only what you need
3. **Domain Verification**: Verify your domain in Google Console
4. **User Verification**: Consider requiring email verification
5. **Audit Logs**: Monitor login attempts in ZITADEL

## Multi-Tenant Configuration

For B2B multi-tenant setup, you can:

### Option 1: Single Google IdP (All Tenants)

Configure Google at instance level. All organizations use the same Google credentials.

### Option 2: Per-Organization IdP

1. Go to each organization's settings
2. Add Google IdP with org-specific credentials
3. Useful when tenants want their own Google Workspace SSO

### Option 3: Google Workspace SSO

For tenants with Google Workspace:

1. They configure ZITADEL as SAML/OIDC provider in their Workspace
2. Their users login via their Workspace domain
3. Provides SSO with their existing Google accounts

## Related Resources

- [Google OAuth Documentation](https://developers.google.com/identity/protocols/oauth2)
- [ZITADEL Google IdP Docs](https://zitadel.com/docs/guides/integrate/identity-providers/google)
- [OAuth Consent Screen](https://console.cloud.google.com/apis/credentials/consent)
