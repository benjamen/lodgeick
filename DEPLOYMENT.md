# Lodgeick Deployment Guide

## Overview
This guide covers deploying the new onboarding flow to production (lodgeick.com).

## Changes Summary

### New Features
1. **Modern 4-Step Onboarding Flow**
   - `/auth` - Authentication with login/register tabs
   - `/connect` - App connection with integration cards
   - `/integrate` - One-click integration with progress animation
   - `/configure` - Field mapping configuration (optional)
   - `/dashboard` - Post-onboarding dashboard

2. **Backend Integration**
   - Connected to `lodgeick.api.catalog.get_app_catalog` API
   - Dynamic app loading from Frappe backend
   - Loading states and error handling

3. **UX Improvements**
   - Back to Dashboard navigation in Settings
   - Loading skeletons for better perceived performance
   - Mobile-responsive design throughout

### Bug Fixes
- Fixed ScriptManager error by removing duplicate frappe shim
- Proper minimal frappe object initialization
- Added Pinia for state management

## Deployment Steps

### 1. Pull Latest Code on Production Server

```bash
ssh root@tendercle.com
cd ~/frappe_docker
git pull
```

### 2. Update Lodgeick App

```bash
# Enter the Frappe container
docker exec -it frappe_docker_devcontainer-frappe-1 bash

# Navigate to bench directory
cd /workspace/development/frappe-bench

# Pull latest lodgeick code
cd apps/lodgeick
git pull origin main
cd ../..

# Install any new dependencies (if needed)
bench --site lodgeick.com migrate

# Build assets
bench build --app lodgeick

# Restart bench
bench restart
```

### 3. Verify Deployment

1. Visit https://lodgeick.com/
2. Test unauthenticated flow:
   - Should redirect to marketing page or auth
3. Test authenticated flow:
   - Login should redirect to `/connect` (if first time) or `/dashboard`
   - Test app connection flow
   - Test integration setup
   - Test field configuration (skip option)
   - Verify dashboard loads correctly

### 4. Test Critical Paths

- [ ] Guest user sees landing page
- [ ] Can sign up successfully
- [ ] Redirected to `/connect` after signup
- [ ] Apps load from backend API
- [ ] Can connect/disconnect apps
- [ ] Continue button enables after connecting at least one app
- [ ] Integration process shows progress animation
- [ ] Field configuration is optional (can skip)
- [ ] Dashboard shows connected apps count
- [ ] Settings has "Back to Dashboard" link
- [ ] No ScriptManager errors in console

## Rollback Plan

If issues occur, rollback to previous version:

```bash
cd ~/frappe_docker/apps/lodgeick
git log  # Find previous commit hash
git checkout <previous-commit-hash>
cd ../../
bench build --app lodgeick
bench restart
```

## Monitoring

### Key Metrics to Watch
- Page load times for onboarding steps
- API response times for `get_app_catalog`
- User completion rate of onboarding flow
- Error rates in browser console

### Common Issues

**Issue: ScriptManager error still appears**
- **Cause**: Production has old lodgeick.html with duplicate shim
- **Fix**: Ensure `bench build --app lodgeick` ran successfully
- **Verify**: Check `/assets/lodgeick/frontend/` has latest files

**Issue: Apps don't load in ConnectAppsView**
- **Cause**: API endpoint not accessible or no apps in catalog
- **Fix**: Check App Catalog doctype has active apps
- **Verify**: Run `bench --site lodgeick.com console` and test API

**Issue: Pinia store not working**
- **Cause**: main.js not updated with createPinia()
- **Fix**: Verify frontend/src/main.js includes Pinia setup
- **Verify**: Check browser console for Pinia errors

## Post-Deployment Tasks

1. **Monitor Error Logs**
   ```bash
   tail -f ~/frappe_docker/logs/frappe-bench.log
   ```

2. **Check Browser Console** on production for:
   - JavaScript errors
   - Failed API requests
   - Vue warnings

3. **Test User Flow** with a test account:
   - Complete full onboarding
   - Verify data persistence
   - Test logout/login cycle

## Architecture Notes

### State Management
- **Pinia Store**: `src/stores/onboarding.js`
- Manages: connected apps, integrations, field mappings, progress
- Persists: Uses Pinia's default in-memory state (consider localStorage for persistence)

### API Integration
- **Endpoint**: `lodgeick.api.catalog.get_app_catalog`
- **Response**: `{ success: boolean, apps: Array }`
- **Error Handling**: Try/catch with fallback UI

### Route Protection
- Public routes: `/`, `/auth`, `/login`, `/signup`
- Protected routes: `/connect`, `/integrate`, `/configure`, `/dashboard`, `/account/*`
- Redirect logic: `router.beforeEach` in `src/router.js`

## Performance Optimizations Applied

1. **Code Splitting**: Lazy-loaded routes with dynamic imports
2. **Conditional Loading**: Apps loaded once and cached
3. **Loading States**: Skeleton UI during data fetch
4. **Optimized Re-renders**: Computed properties in Pinia store

## Security Considerations

- ✅ All API endpoints require authentication except guest-allowed routes
- ✅ CSRF token validation on all mutations
- ✅ No sensitive data in client-side state
- ✅ OAuth credentials never exposed to frontend

## Support

For issues or questions:
- GitHub Issues: https://github.com/benjamen/lodgeick/issues
- Contact: development team

---

**Last Updated**: 2025-10-09
**Version**: 1.0.0
**Author**: Claude Code
