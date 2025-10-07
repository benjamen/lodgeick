# Lodgeick - One-Click Integration Platform

**Lodgeick** is a modern SaaS integration platform that provides simple, one-click integrations between popular business applications. Built on Frappe Framework with a Vue.js frontend and n8n workflow orchestration.

## 🎯 Overview

Lodgeick eliminates the complexity of connecting your favorite business tools. Users select an app, choose a use case, authorize their accounts, and let the platform handle the rest.

### Key Features

- ✅ **One-Click Integration Setup** - No workflow building required
- 🔐 **Secure OAuth Authentication** - Enterprise-grade token management
- 📊 **Real-time Monitoring** - Track integration status and execution logs
- 🎨 **Beautiful Vue.js Frontend** - Modern, responsive UI with Tailwind CSS
- 🔄 **n8n Workflow Engine** - Powerful automation behind the scenes
- 🚀 **50+ App Catalog** - Popular business applications ready to connect

## 🏗️ Architecture

```
Vue Frontend → Frappe Backend → n8n Workflows
  (UI/UX)      (API/OAuth/DB)    (Orchestration)
```

### Tech Stack

- **Frontend**: Vue 3 + Vite + Tailwind CSS + frappe-ui
- **Backend**: Frappe Framework (Python)
- **Database**: MariaDB
- **Orchestration**: n8n

## 📦 Quick Start

### Install

```bash
# Get the app
bench get-app https://github.com/benjamen/lodgeick
bench --site lodgeick.com install-app lodgeick
```

### Development

```bash
cd apps/lodgeick/frontend
yarn install
yarn dev
```

## 📋 Core DocTypes

- **Integration Token** - Secure OAuth token storage
- **User Integration** - Active integration tracking
- **App Catalog** - Available apps and use cases
- **Integration Log** - Execution logs

## 🔌 API Endpoints

- `/api/method/lodgeick.api.oauth.*` - OAuth flows
- `/api/method/lodgeick.api.integrations.*` - Integration management
- `/api/method/lodgeick.api.catalog.*` - App catalog

## 📄 License

MIT