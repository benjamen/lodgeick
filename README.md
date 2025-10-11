# Lodgeick - One-Click Integration Platform

**Lodgeick** is a modern SaaS integration platform that provides simple, one-click integrations between popular business applications. Built on Frappe Framework with a Vue.js frontend and n8n workflow orchestration.

## 🎯 Overview

Lodgeick eliminates the complexity of connecting your favorite business tools. Users select an app, choose a use case, authorize their accounts, and let the platform handle the rest.

### Key Features

- ✅ **One-Click Integration Setup** - No workflow building required
- 🤖 **AI-Powered Google Setup** - Natural language to Google Cloud integration
- 🔐 **Secure OAuth Authentication** - Enterprise-grade token management
- 📊 **Real-time Monitoring** - Track integration status and execution logs
- 🎨 **Beautiful Vue.js Frontend** - Modern, responsive UI with Tailwind CSS
- 🔄 **n8n Workflow Engine** - Powerful automation behind the scenes
- 🚀 **50+ App Catalog** - Popular business applications ready to connect
- 💡 **Smart Billing Detection** - Only prompts for billing when actually required

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

# Install Python dependencies
pip install -r apps/lodgeick/requirements.txt
```

### Configuration

```json
// Add to site_config.json
{
  "anthropic_api_key": "sk-ant-api03-...",  // For AI-powered setup
  "google_cloud_service_account": {...},    // For automated project creation
  "n8n_base_url": "http://localhost:5678",
  "n8n_api_key": "your-api-key"
}
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
- **User Google Project** - AI-created Google Cloud projects
- **App Catalog** - Available apps and use cases
- **Integration Log** - Execution logs

## 🔌 API Endpoints

### OAuth & Authentication
- `/api/method/lodgeick.api.oauth.*` - OAuth flows
- `/api/method/lodgeick.api.integrations.*` - Integration management

### AI-Powered Setup
- `/api/method/lodgeick.api.google_ai_setup.parse_intent` - Parse natural language
- `/api/method/lodgeick.api.google_ai_setup.create_project` - Create GCP project
- `/api/method/lodgeick.api.google_ai_setup.setup_oauth_credentials` - Setup OAuth

### Catalog
- `/api/method/lodgeick.api.catalog.*` - App catalog

## 🤖 AI-Powered Google Setup

Lodgeick includes an intelligent setup wizard for Google Cloud integrations:

1. **Natural Language Input**: "I want to read emails from Gmail and create spreadsheets"
2. **AI Analysis**: Claude AI determines required APIs and scopes
3. **Smart Setup**: Choose automated (new project) or manual (existing project)
4. **Auto n8n Sync**: Credentials automatically available in workflows

See [AI_SETUP_GUIDE.md](./AI_SETUP_GUIDE.md) for detailed documentation.

## 📖 Additional Documentation

- [AI Setup Guide](./AI_SETUP_GUIDE.md) - AI-powered Google integration setup
- [OAuth Setup](./OAUTH_SETUP.md) - Manual OAuth configuration
- [N8N Integration](./N8N_INTEGRATION.md) - n8n workflow sync

## 📄 License

MIT