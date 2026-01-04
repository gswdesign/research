# Permissions and RBAC Guide

Configure role-based access control (RBAC) for multi-tenant B2B applications with ZITADEL.

## Role Hierarchy

```
super_admin
    ├── Can access ALL tenants
    ├── Can manage instance settings
    └── Can create/delete organizations

org_admin
    ├── Full access within their organization
    ├── Can invite users to their org
    └── Can assign roles (up to org_admin)

editor
    ├── Can create and edit resources
    ├── Cannot manage users
    └── Scoped to their organization

viewer
    ├── Read-only access
    ├── Cannot create or modify
    └── Scoped to their organization
```

## ZITADEL Concepts

### Organizations

Each tenant is a separate ZITADEL Organization:

```
ZITADEL Instance
├── Default Org (your company)
│   └── super_admin users
├── Acme Corp (Tenant A)
│   ├── org_admin
│   ├── editors
│   └── viewers
└── Widget Inc (Tenant B)
    ├── org_admin
    ├── editors
    └── viewers
```

### Projects

Projects contain your applications and role definitions:

```
Project: YourApp
├── Roles
│   ├── super_admin
│   ├── org_admin
│   ├── editor
│   └── viewer
├── Applications
│   ├── Login UI (OIDC)
│   ├── SPA (OIDC)
│   └── API (API)
└── Grants (per-org role assignments)
```

### Authorizations (User Grants)

Authorizations connect users to roles within projects:

```
User: john@acme.com
└── Authorization
    ├── Project: YourApp
    ├── Role: org_admin
    └── Organization: Acme Corp
```

## Setting Up Roles

### Step 1: Create Project

1. Go to ZITADEL Console
2. Select your organization (Default Org for super admins)
3. Go to **Projects** → **Create New Project**
4. Name it (e.g., "YourApp")
5. Click "Create"

### Step 2: Define Roles

1. In the project, go to **Roles**
2. Create these roles:

| Role Key | Display Name | Description |
|----------|--------------|-------------|
| `super_admin` | Super Administrator | Full access across all tenants |
| `org_admin` | Organization Admin | Full access within organization |
| `editor` | Editor | Create and edit content |
| `viewer` | Viewer | Read-only access |

Click "Add Role" for each.

### Step 3: Configure Role Claims

Ensure roles are included in tokens:

1. Go to project settings
2. Enable "Assert Roles on Authentication"
3. This adds roles to the JWT claims

## Assigning Roles

### Via Console (Manual)

1. Go to **Users**
2. Select a user
3. Go to **Authorizations**
4. Click "New Authorization"
5. Select Project, Organization, and Role(s)
6. Click "Create"

### Via API (Programmatic)

```bash
# Create user grant (authorization)
curl -X POST "https://your-zitadel/management/v1/users/{userId}/grants" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "projectId": "your-project-id",
    "roleKeys": ["editor"]
  }'
```

### Via Script

See [scripts/setup-roles.sh](../scripts/setup-roles.sh) for automated role creation.

## Checking Permissions

### In JWT Claims

After login, the JWT contains role information:

```json
{
  "sub": "user-id",
  "email": "john@acme.com",
  "urn:zitadel:iam:org:id": "org-123",
  "urn:zitadel:iam:org:name": "Acme Corp",
  "urn:zitadel:iam:org:project:roles": {
    "editor": {
      "org-123": "Acme Corp"
    }
  }
}
```

### In Application Code

```typescript
// Parse roles from JWT
const rolesObj = claims['urn:zitadel:iam:org:project:roles']
const roles = rolesObj ? Object.keys(rolesObj) : []

// Check permissions
const isSuperAdmin = roles.includes('super_admin')
const isOrgAdmin = roles.includes('org_admin') || isSuperAdmin
const isEditor = roles.includes('editor') || isOrgAdmin
const isViewer = roles.includes('viewer') || isEditor
```

### In Cloudflare Worker

```typescript
// See cloudflare/worker-example/src/middleware/auth.ts
import { requireRole } from './middleware/auth'

// Protect routes
app.get('/admin', requireRole('org_admin'), handler)
app.post('/resources', requireRole('editor'), handler)
app.get('/resources', requireRole('viewer'), handler)
```

## Multi-Tenant Isolation

### Automatic Tenant Context

ZITADEL includes organization info in tokens:

```typescript
const orgId = claims['urn:zitadel:iam:org:id']
const orgName = claims['urn:zitadel:iam:org:name']
```

### Database Queries

Always filter by organization:

```typescript
// Good - tenant isolated
const resources = await db.query(
  'SELECT * FROM resources WHERE org_id = $1',
  [auth.organizationId]
)

// Bad - no isolation
const resources = await db.query('SELECT * FROM resources')
```

### API Middleware

```typescript
// Ensure users can only access their org's resources
function requireTenantAccess(resourceOrgId: string) {
  return (c: Context) => {
    const auth = c.get('auth')

    // Super admins bypass tenant check
    if (auth.isSuperAdmin) return next()

    // Others must match org
    if (auth.organizationId !== resourceOrgId) {
      return c.json({ error: 'Forbidden' }, 403)
    }

    return next()
  }
}
```

## Advanced Permission Patterns

### "View Own Only"

For viewers who should only see their own resources:

```typescript
// In API handler
app.get('/resources', requireRole('viewer'), async (c) => {
  const auth = c.get('auth')

  let query = 'SELECT * FROM resources WHERE org_id = $1'
  const params = [auth.organizationId]

  // Viewers can only see their own
  if (!auth.isEditor && !auth.isOrgAdmin) {
    query += ' AND owner_id = $2'
    params.push(auth.userId)
  }

  const resources = await db.query(query, params)
  return c.json({ data: resources })
})
```

### Hierarchical Access

For editors who can see their subordinates' resources:

```typescript
// Assuming you have a user hierarchy table
app.get('/resources', requireRole('editor'), async (c) => {
  const auth = c.get('auth')

  if (auth.isOrgAdmin) {
    // Admins see everything in org
    return queryAllOrgResources(auth.organizationId)
  }

  // Get subordinate user IDs
  const subordinates = await getSubordinates(auth.userId)
  const allowedUsers = [auth.userId, ...subordinates]

  // Query resources owned by self or subordinates
  const resources = await db.query(
    'SELECT * FROM resources WHERE org_id = $1 AND owner_id = ANY($2)',
    [auth.organizationId, allowedUsers]
  )

  return c.json({ data: resources })
})
```

### Resource-Level Permissions

For fine-grained access to specific resources:

```typescript
// Store permissions in database
interface ResourcePermission {
  resourceId: string
  userId: string
  permission: 'read' | 'write' | 'admin'
}

// Check before access
async function canAccess(
  userId: string,
  resourceId: string,
  requiredPermission: 'read' | 'write' | 'admin'
): Promise<boolean> {
  const permission = await db.query(
    'SELECT permission FROM resource_permissions WHERE resource_id = $1 AND user_id = $2',
    [resourceId, userId]
  )

  const levels = { read: 1, write: 2, admin: 3 }
  return levels[permission] >= levels[requiredPermission]
}
```

## Onboarding New Tenants

### Create Organization

1. Console: Organizations → Create
2. API: See [scripts/create-org.sh](../scripts/create-org.sh)

### Invite First Admin

```bash
# Via API
curl -X POST "https://your-zitadel/management/v1/users/_import" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "userName": "admin@newtenant.com",
    "profile": { ... },
    "email": { "email": "admin@newtenant.com", "isEmailVerified": true }
  }'

# Assign org_admin role
curl -X POST "https://your-zitadel/management/v1/users/{userId}/grants" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "projectId": "your-project-id",
    "roleKeys": ["org_admin"]
  }'
```

### Let Them Invite Their Team

Org admins can invite users via:
- ZITADEL Console (with proper org context)
- Your application's admin UI
- API calls with their token

## Audit and Compliance

### Audit Logs

ZITADEL logs all authentication and authorization events:

1. Console: Audit Log
2. API: `/admin/v1/events`

### Regular Access Reviews

Recommend periodic review:
- Quarterly: Review all org_admin assignments
- Monthly: Review super_admin assignments
- As-needed: When employees leave

### Compliance Reports

Export user grants for compliance:

```bash
# List all user grants in organization
curl "https://your-zitadel/management/v1/users/grants/_search" \
  -H "Authorization: Bearer $TOKEN" \
  -H "x-zitadel-orgid: $ORG_ID"
```

## Best Practices

1. **Principle of Least Privilege**: Start with `viewer`, escalate as needed
2. **Super Admins**: Keep to minimum (2-3 people)
3. **Org Admin per Tenant**: Each tenant should have at least 1-2 org_admins
4. **Audit Regularly**: Review high-privilege assignments quarterly
5. **Use Groups** (if available): For easier bulk management
6. **Document Decisions**: Record why users have elevated access
