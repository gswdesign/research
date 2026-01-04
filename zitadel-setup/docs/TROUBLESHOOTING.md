# Troubleshooting Guide

Common issues and solutions for ZITADEL setup.

## ZITADEL Server Issues

### ZITADEL container won't start

**Symptoms**: Container exits immediately or restart loop

**Check logs**:
```bash
docker compose logs zitadel
```

**Common causes**:

1. **Invalid MASTERKEY**
   - Must be exactly 32 bytes base64 encoded
   - Generate with: `openssl rand -base64 32`
   - Error: "invalid master key"

2. **PostgreSQL not ready**
   - Wait for PostgreSQL healthcheck
   - Error: "connection refused" or "database does not exist"
   - Solution: `docker compose up postgres -d` first, wait, then start ZITADEL

3. **Port already in use**
   - Error: "bind: address already in use"
   - Solution: Change `ZITADEL_PORT` or stop conflicting service

### Can't access ZITADEL Console

**Check**:
1. Container is running: `docker compose ps`
2. Correct URL: `http://localhost:8080/ui/console`
3. No firewall blocking port 8080

### Login fails with "invalid credentials"

**For initial admin**:
- Username: `admin@zitadel.localhost` (default)
- Password: `Password1!` (default)
- Or check your `.env` for `ZITADEL_ADMIN_*` values

### "Certificate verify failed" errors

**Cause**: TLS configuration mismatch

**Solution**:
- Local dev: `ZITADEL_EXTERNALSECURE=false`
- Production: `ZITADEL_EXTERNALSECURE=true`
- Ensure domain matches `ZITADEL_EXTERNALDOMAIN`

## Database Issues

### "relation does not exist"

**Cause**: Migrations didn't run

**Solution**:
```bash
# Restart ZITADEL - it runs migrations on startup
docker compose restart zitadel

# Or check migration logs
docker compose logs zitadel | grep -i migration
```

### "too many connections"

**Cause**: Connection pool exhausted

**Solution**:
- Increase PostgreSQL max_connections
- Reduce ZITADEL instances
- Check for connection leaks

### Data lost after restart

**Cause**: Volume not persisted

**Solution**: Ensure docker-compose.yml has:
```yaml
volumes:
  postgres_data:
    driver: local
```

## Login UI Issues

### "OIDC configuration error"

**Check**:
1. `VITE_ZITADEL_AUTHORITY` matches ZITADEL URL
2. `VITE_ZITADEL_CLIENT_ID` is correct
3. Client exists in ZITADEL Console

### "redirect_uri_mismatch"

**Cause**: Redirect URI not registered

**Solution**:
1. Go to ZITADEL Console → Project → Application
2. Add exact redirect URI (including trailing slash if any)
3. URIs are case-sensitive

### Google login not appearing

**Check**:
1. Google IdP configured in ZITADEL
2. IdP is enabled (toggle on)
3. Scopes configured correctly

### Callback page spinning forever

**Cause**: Token exchange failing

**Check browser console for**:
- CORS errors
- Network failures
- JWT parsing errors

**Solutions**:
1. Verify ZITADEL is accessible from browser
2. Check OIDC configuration
3. Clear browser cache/cookies

## Google SSO Issues

### "Access blocked: This app's request is invalid"

**Cause**: Redirect URI mismatch in Google Console

**Solution**:
1. Copy exact URI from error
2. Add to Google Console → Credentials → OAuth Client → Authorized redirect URIs
3. Wait 5 minutes for propagation

### "Error 400: redirect_uri_mismatch"

**Same as above** - exact URI matching required

### "User info not returned"

**Check**:
1. Scopes include `openid email profile`
2. "User Info inside ID Token" enabled in ZITADEL app settings

### Google login works but no roles

**Cause**: Roles not assigned after IdP login

**Solutions**:
1. Enable auto-assignment with ZITADEL Actions
2. Use ZITADEL Console to assign roles manually
3. Configure default roles for new users

## Multi-Tenant Issues

### Users see wrong organization's data

**Cause**: Missing tenant isolation in queries

**Solution**:
```typescript
// Always filter by organization
const data = await db.query(
  'SELECT * FROM resources WHERE org_id = $1',
  [auth.organizationId]
)
```

### Can't switch organizations

**Check**: User has grants in multiple organizations

### "Forbidden" when accessing resources

**Check**:
1. User has correct role
2. Role is in the right project
3. Project is granted to the organization

## Cloudflare Worker Issues

### "Token validation failed"

**Check**:
1. `ZITADEL_ISSUER` is correct (full URL with https)
2. JWKS endpoint is accessible from Worker
3. Token hasn't expired

### CORS errors

**Solution**: Configure CORS in Worker:
```typescript
app.use('*', cors({
  origin: ['https://your-app.com'],
  credentials: true,
}))
```

### "Missing Authorization header"

**Check**: Frontend is sending token:
```typescript
fetch(url, {
  headers: {
    'Authorization': `Bearer ${token}`
  }
})
```

## Railway Deployment Issues

### Deployment fails

**Check**:
1. Dockerfile is in root of service folder
2. Build args are set in Railway dashboard
3. Check build logs in Railway

### Custom domain not working

**Steps**:
1. Add domain in Railway dashboard
2. Copy CNAME record
3. Add to your DNS
4. Wait for SSL provisioning (can take 10-30 min)

### Environment variables not applied

**Check**:
1. Variables are set in Railway service settings (not project level)
2. Service was redeployed after changing variables
3. Variable names match exactly (case-sensitive)

## Performance Issues

### Slow login

**Check**:
1. Database performance
2. Network latency to ZITADEL
3. JWKS caching in Workers

### High memory usage

**Solutions**:
1. Limit ZITADEL cache sizes
2. Configure appropriate Postgres memory
3. Use connection pooling

## Getting Help

1. **ZITADEL Discord**: https://zitadel.com/discord
2. **GitHub Issues**: https://github.com/zitadel/zitadel/issues
3. **Documentation**: https://zitadel.com/docs

When reporting issues, include:
- ZITADEL version
- Docker/Railway setup
- Relevant logs (redact secrets!)
- Steps to reproduce
