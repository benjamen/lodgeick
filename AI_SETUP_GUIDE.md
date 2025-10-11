# AI-Powered Google API Setup Assistant

## Overview

The AI-Powered Google API Setup Assistant automates the process of setting up Google Cloud integrations for Lodgeick users. It uses Claude AI to interpret natural language requests and automatically configure the necessary Google APIs, OAuth credentials, and n8n workflows.

## Features

✅ **Natural Language Input**: Users describe what they want in plain English
✅ **AI-Powered Analysis**: Claude parses intent and determines required APIs + scopes
✅ **Billing Detection**: Only prompts for billing if APIs actually require it
✅ **Dual Setup Modes**: Automated (new project) or Manual (existing project)
✅ **Auto n8n Sync**: Credentials automatically registered in n8n
✅ **Smart Scope Selection**: AI suggests minimal necessary OAuth scopes

## Architecture

```
┌─────────────────┐
│   Vue Frontend  │  GoogleAISetupWizard.vue
│   (User Input)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Frappe API     │  google_ai_setup.py
│  (Orchestration)│
└────────┬────────┘
         │
    ┌────┴────┬──────────┬────────────┐
    │         │          │            │
    ▼         ▼          ▼            ▼
┌───────┐ ┌──────┐ ┌──────────┐ ┌─────────┐
│  AI   │ │Google│ │   n8n    │ │  Frappe │
│Parser │ │Cloud │ │  Client  │ │   DB    │
└───────┘ └──────┘ └──────────┘ └─────────┘
```

## Setup Instructions

### Prerequisites

1. **Anthropic API Key** (for Claude AI)
   ```json
   // Add to site_config.json
   {
     "anthropic_api_key": "sk-ant-api03-..."
   }
   ```

2. **Google Cloud Service Account** (for automated project creation)
   ```json
   // Add to site_config.json
   {
     "google_cloud_service_account": {
       "type": "service_account",
       "project_id": "your-project",
       "private_key_id": "...",
       "private_key": "-----BEGIN PRIVATE KEY-----\n...",
       "client_email": "...@....iam.gserviceaccount.com",
       "client_id": "...",
       "auth_uri": "https://accounts.google.com/o/oauth2/auth",
       "token_uri": "https://oauth2.googleapis.com/token"
     }
   }
   ```

   **Service Account Permissions Required:**
   - `roles/resourcemanager.projectCreator`
   - `roles/serviceusage.serviceUsageAdmin`
   - `roles/iam.serviceAccountUser`

3. **n8n Configuration** (already set up)
   ```json
   {
     "n8n_base_url": "http://localhost:5678",
     "n8n_api_key": "your-n8n-api-key"
   }
   ```

4. **Python Dependencies**
   ```bash
   pip install anthropic google-auth google-auth-oauthlib google-api-python-client
   ```

### Installation

1. **Create DocType**
   ```bash
   cd ~/frappe_docker/development/frappe-bench
   bench --site lodgeick.com migrate
   ```

2. **Build Frontend**
   ```bash
   cd apps/lodgeick/frontend
   yarn install
   yarn build
   ```

3. **Clear Cache**
   ```bash
   bench --site lodgeick.com clear-cache
   bench restart
   ```

## Usage

### For End Users

1. **Open Integration Wizard**
   - Navigate to Integrations page
   - Click "AI-Powered Setup" button

2. **Describe Your Intent**
   ```
   Example inputs:
   - "Connect to Google Sheets and Gmail"
   - "I need access to Google Drive and Calendar"
   - "Set up Google Maps and Vision API"
   ```

3. **Review AI Analysis**
   - AI shows required APIs and scopes
   - Billing warning if needed
   - Choose setup method (Auto or Manual)

4. **Complete Setup**
   - **Auto**: Enter project name → Lodgeick creates everything
   - **Manual**: Follow step-by-step guide for existing project

5. **Enter OAuth Credentials**
   - Create credentials in Google Cloud Console
   - Enter Client ID and Secret
   - Credentials auto-sync to n8n

### For Developers

#### API Endpoints

**1. Parse Intent**
```python
POST /api/method/lodgeick.api.google_ai_setup.parse_intent
{
  "intent": "I want to read and send emails from Gmail"
}

Response:
{
  "success": true,
  "apis": [
    {
      "name": "gmail.googleapis.com",
      "display_name": "Gmail API",
      "scopes": [
        "https://www.googleapis.com/auth/gmail.readonly",
        "https://www.googleapis.com/auth/gmail.send"
      ],
      "description": "Read and send emails"
    }
  ],
  "billing_required": false,
  "billing_apis": [],
  "reasoning": "Gmail API doesn't require billing",
  "next_step": "project_setup"
}
```

**2. Create Project**
```python
POST /api/method/lodgeick.api.google_ai_setup.create_project
{
  "project_name": "My Integration",
  "intent_data": "{...parsed intent data...}"
}

Response:
{
  "success": true,
  "project_id": "my-integration-20250111123456",
  "apis_enabled": ["gmail.googleapis.com"],
  "next_step": "oauth_setup"
}
```

**3. Setup OAuth**
```python
POST /api/method/lodgeick.api.google_ai_setup.setup_oauth_credentials
{
  "project_id": "my-integration-20250111123456",
  "client_id": "123...apps.googleusercontent.com",
  "client_secret": "GOCSPX-..."
}

Response:
{
  "success": true,
  "n8n_credential_id": "credential-uuid",
  "next_step": "complete"
}
```

## Billing-Required APIs

The following APIs automatically trigger billing warnings:

- **Maps APIs**
  - `maps.googleapis.com`
  - `maps-backend.googleapis.com`

- **AI/ML APIs**
  - `vision.googleapis.com`
  - `language.googleapis.com`
  - `translate.googleapis.com`
  - `speech.googleapis.com`
  - `texttospeech.googleapis.com`
  - `aiplatform.googleapis.com`
  - `vertexai.googleapis.com`

- **Infrastructure APIs**
  - `compute.googleapis.com`
  - `container.googleapis.com`
  - `run.googleapis.com`
  - `bigquery.googleapis.com`

## Common Use Cases

### Example 1: Gmail + Sheets Integration
```
User: "I want to save Gmail attachments to Google Sheets"

AI Response:
- Gmail API (read email, manage attachments)
- Google Sheets API (create and update spreadsheets)
- Google Drive API (file storage)

Billing: No
```

### Example 2: Maps-Based Application
```
User: "Build a location tracker using Google Maps"

AI Response:
- Maps JavaScript API (display maps)
- Geolocation API (get user location)

Billing: Yes (Maps API requires billing)
Warning: "Maps API requires an active billing account"
```

### Example 3: Calendar Automation
```
User: "Sync my Google Calendar with our CRM"

AI Response:
- Google Calendar API (read/write events)

Billing: No
```

## Troubleshooting

### Issue: "Anthropic API key not configured"
**Solution:** Add `anthropic_api_key` to `site_config.json`

### Issue: "Failed to create Google Cloud project"
**Solution:**
1. Check service account has correct permissions
2. Verify service account JSON is valid
3. Check quota limits in your Google Cloud org

### Issue: "APIs failed to enable"
**Solution:**
- Some APIs may require billing even in test projects
- Check API-specific restrictions
- Verify project has correct org policies

### Issue: "n8n credential sync failed"
**Solution:**
- Verify n8n is running and accessible
- Check n8n API key is valid
- Ensure n8n has proper CORS settings

## Security Considerations

1. **Service Account Security**
   - Store service account JSON securely
   - Use minimal required permissions
   - Rotate credentials regularly

2. **API Key Protection**
   - Never commit API keys to git
   - Use environment variables or secret managers
   - Restrict API key usage by IP

3. **OAuth Credentials**
   - Client secrets stored encrypted in Frappe
   - Never expose in frontend
   - Use secure password fields

4. **Rate Limiting**
   - Claude API has rate limits
   - Implement request throttling
   - Cache AI responses when possible

## Future Enhancements

- [ ] Support for other cloud providers (AWS, Azure)
- [ ] Automatic billing account creation
- [ ] Multi-project management
- [ ] Cost estimation before setup
- [ ] Workflow template suggestions
- [ ] Integration health monitoring

## Support

For issues or questions:
1. Check this documentation
2. Review error logs in Frappe
3. Test individual components
4. Contact Lodgeick support

## License

MIT License - see LICENSE file for details
