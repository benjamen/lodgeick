# Frontend Deployment Guide

This guide explains how to deploy the Lodgeick Vue.js frontend to production so that lodgeick.com serves the frontend app instead of the Frappe backend.

## Architecture

The Lodgeick app uses a Vue.js SPA (Single Page Application) for the frontend, which is:
- Built with Vite
- Served via Frappe's routing system
- Integrated with Frappe's authentication and API

### Routing Strategy

- **Root path** (`/`) → Vue.js frontend (lodgeick.html)
- **Backend paths** (`/app`, `/desk`, `/api`) → Frappe backend (unchanged)
- **Assets** → Static files from `lodgeick/public/frontend/`

This is configured in `lodgeick/hooks.py:70-72`:
```python
website_route_rules = [
	{"from_route": "/", "to_route": "lodgeick"},
]
```

## Local Development

### Running Dev Server

```bash
# Inside devcontainer
cd /workspace/development/frappe-bench/apps/lodgeick/frontend
yarn dev
```

Access at: http://localhost:5173

The dev server proxies backend API calls to port 8090.

### Building for Production

```bash
# Inside devcontainer
cd /workspace/development/frappe-bench/apps/lodgeick/frontend
yarn build
```

This will:
1. Build the Vue.js app to `../lodgeick/public/frontend/`
2. Copy and transform `index.html` to `../lodgeick/www/lodgeick.html`
3. Fix asset paths to work with Frappe's `/assets/` serving

## Production Deployment

### Prerequisites

1. Frappe site configured and running
2. Lodgeick app installed
3. SSH access to production server

### Deployment Steps

#### Step 1: Build Frontend Locally

```bash
# On your local machine (or inside devcontainer)
cd /workspace/development/frappe-bench/apps/lodgeick/frontend
yarn build
```

#### Step 2: Commit and Push

```bash
cd /workspace/development/frappe-bench/apps/lodgeick
git add lodgeick/www/ lodgeick/public/frontend/
git commit -m "build: Update production frontend"
git push origin main
```

#### Step 3: Deploy to Production Server

```bash
# SSH into production server
ssh user@lodgeick.com

# Navigate to bench directory
cd ~/frappe-bench  # Or wherever your bench is located

# Pull latest code
cd apps/lodgeick
git pull origin main

# Go back to bench root
cd ../..

# Clear cache and build assets
bench --site lodgeick.com clear-cache
bench --site lodgeick.com clear-website-cache

# Restart services (choose one based on your setup)
# If using supervisor:
sudo supervisorctl restart all

# If using docker compose:
docker-compose restart backend frontend

# If using systemd:
sudo systemctl restart frappe-web@lodgeick.com frappe-worker@lodgeick.com
```

#### Step 4: Verify Deployment

1. Visit https://lodgeick.com - should show Vue.js frontend
2. Visit https://lodgeick.com/desk - should show Frappe backend
3. Check browser console for any errors

### Alternative: Direct Build on Server

If you prefer to build directly on the production server:

```bash
# SSH into server
ssh user@lodgeick.com

# Navigate to app
cd ~/frappe-bench/apps/lodgeick/frontend

# Install dependencies (if not already installed)
yarn install

# Build
yarn build

# Clear cache
cd ~/frappe-bench
bench --site lodgeick.com clear-cache
bench --site lodgeick.com clear-website-cache

# Restart services
sudo supervisorctl restart all
```

## Docker Deployment

If you're using the Docker setup from frappe_docker:

### Step 1: Build Frontend

```bash
# Inside the frappe devcontainer
docker exec frappe_docker_devcontainer-frappe-1 bash -c \
  "cd /workspace/development/frappe-bench/apps/lodgeick/frontend && yarn build"
```

### Step 2: Commit Changes

```bash
cd /home/ben/frappe_docker/development/frappe-bench/apps/lodgeick
git add lodgeick/www/ lodgeick/public/frontend/
git commit -m "build: Update production frontend"
git push origin main
```

### Step 3: Deploy to Server

```bash
# On production server with docker setup
cd ~/frappe_docker
git pull

# Restart containers
docker-compose restart backend frontend
```

## Troubleshooting

### Frontend shows Frappe backend instead

**Problem**: Visiting lodgeick.com shows Frappe UI instead of Vue frontend

**Solutions**:
1. Check `lodgeick/www/lodgeick.html` exists
2. Verify `lodgeick/www/lodgeick.py` exists
3. Check hooks.py has `website_route_rules` configured
4. Clear cache: `bench --site lodgeick.com clear-website-cache`
5. Restart services

### Assets not loading (404 errors)

**Problem**: CSS/JS files return 404

**Solutions**:
1. Verify files exist in `lodgeick/public/frontend/assets/`
2. Run `bench build` to rebuild assets
3. Check nginx is serving `/assets/` correctly
4. Clear browser cache

### Blank page with console errors

**Problem**: Page loads but shows blank with JS errors

**Solutions**:
1. Check browser console for specific errors
2. Verify `copy-html.js` ran successfully during build
3. Ensure asset paths in lodgeick.html are correct
4. Check Frappe session/authentication is working

### Changes not reflected after deployment

**Problem**: Code changes don't appear on site

**Solutions**:
1. Clear Frappe cache: `bench --site lodgeick.com clear-cache`
2. Clear website cache: `bench --site lodgeick.com clear-website-cache`
3. Hard refresh browser (Ctrl+Shift+R / Cmd+Shift+R)
4. Check browser is not using cached version
5. Restart Frappe services

## File Structure

```
lodgeick/
├── frontend/                    # Vue.js source code
│   ├── src/
│   ├── package.json
│   ├── vite.config.js
│   └── copy-html.js            # Build script to copy HTML
│
├── lodgeick/
│   ├── public/
│   │   └── frontend/           # Built frontend assets (output)
│   │       ├── index.html
│   │       └── assets/         # CSS, JS, fonts
│   │
│   ├── www/
│   │   ├── lodgeick.html       # Production HTML (from copy-html.js)
│   │   └── lodgeick.py         # Frappe page controller
│   │
│   └── hooks.py                # Routing configuration
```

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Build and Deploy Frontend

on:
  push:
    branches: [main]
    paths:
      - 'frontend/**'

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'yarn'
          cache-dependency-path: frontend/yarn.lock

      - name: Install dependencies
        run: cd frontend && yarn install

      - name: Build frontend
        run: cd frontend && yarn build

      - name: Commit build
        run: |
          git config user.name "GitHub Actions"
          git config user.email "actions@github.com"
          git add lodgeick/www/ lodgeick/public/frontend/
          git commit -m "build: Auto-build frontend [skip ci]" || exit 0
          git push

      - name: Deploy to server
        run: |
          ssh ${{ secrets.SSH_USER }}@${{ secrets.SSH_HOST }} \
            "cd ~/frappe-bench/apps/lodgeick && \
             git pull && \
             cd ~/frappe-bench && \
             bench --site lodgeick.com clear-cache && \
             bench --site lodgeick.com clear-website-cache && \
             sudo supervisorctl restart all"
```

## Performance Optimization

### Enable Gzip Compression

Ensure nginx is configured to compress static assets (already configured in `frappe_docker/resources/nginx-template.conf`).

### CDN Integration

For better performance, consider serving static assets from a CDN:

1. Upload `lodgeick/public/frontend/assets/` to CDN
2. Update asset paths in `copy-html.js`
3. Configure CORS headers if needed

### Cache Busting

Asset filenames already include content hashes (e.g., `index-BXa9JWwl.js`), which enables long-term caching.

## Maintenance

### Regular Tasks

- **Weekly**: Check for dependency updates (`yarn outdated`)
- **After major changes**: Test build locally before deploying
- **Monthly**: Review and optimize bundle size

### Monitoring

Monitor these metrics:
- Frontend load time
- Asset download sizes
- JavaScript errors in browser console
- Server logs for routing issues

## Support

For issues or questions:
- Check the troubleshooting section above
- Review Frappe documentation: https://frappeframework.com
- Check Vite documentation: https://vitejs.dev
