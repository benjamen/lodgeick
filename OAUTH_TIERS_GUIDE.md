# OAuth Three-Tier Setup System

## Overview

Lodgeick provides three flexible options for OAuth integration setup, balancing ease-of-use with control and scalability:

1. **Quick Start (Default Tier)** - Use Lodgeick's shared OAuth app
2. **AI-Powered Setup (AI Tier)** - Create your own project with AI guidance
3. **Manual Setup (Manual Tier)** - Full control over your OAuth configuration

## Tier Comparison

| Feature | Quick Start | AI-Powered | Manual |
|---------|------------|------------|--------|
| **Setup Time** | Instant | ~2 minutes | ~10 minutes |
| **Technical Knowledge** | None | Basic | Advanced |
| **Rate Limits** | Shared limits | Unlimited | Unlimited |
| **Billing APIs** | Not available | Available | Available |
| **Best For** | Testing, personal use | Most users | Businesses, developers |

---

## Tier 1: Quick Start (Default/Shared App)

### Overview
Use Lodgeick's pre-configured OAuth application. No setup required - just click and connect.

### Supported Providers
- ✅ Google (Gmail, Sheets, Drive, Calendar)
- ✅ Slack
- ✅ Xero
- ✅ Microsoft 365
- ✅ HubSpot

### Rate Limits

#### Google
- Gmail: 100 emails/day, 5 requests/minute
- Sheets: 500 requests/day, 50 requests/minute
- Drive: 1,000 operations/day, 100 requests/minute
- Calendar: 500 requests/day, 50 requests/minute

#### Slack
- 20 requests/minute
- 10,000 requests/day

#### Xero
- 60 requests/minute
- 5,000 requests/day

#### Microsoft 365
- Outlook: 100 emails/day, 10 requests/minute
- OneDrive: 1,000 operations/day, 100 requests/minute
- Teams: 500 requests/day, 50 requests/minute

#### HubSpot
- 100 requests/10 seconds
- 250,000 requests/day (shared across all users)

### Limitations
- **Shared Quotas**: Rate limits are shared among all Lodgeick users using the default tier
- **No Billing APIs**: Maps, Vision AI, and other paid Google APIs are not available
- **Limited Scopes**: Only essential OAuth scopes are included
- **Branding**: API calls may show "via Lodgeick" in audit logs

### When to Use
- ✅ Testing integrations before production
- ✅ Personal projects with low API usage
- ✅ Quick proof-of-concept demos
- ✅ Non-billing-required workflows

### When NOT to Use
- ❌ Production business-critical workflows
- ❌ High-volume API usage (>100 requests/day)
- ❌ Billing-required APIs (Maps, Vision, Translation, etc.)
- ❌ Full inbox access (Gmail read access not included)

---

## Tier 2: AI-Powered Setup (Recommended)

### Overview
Describe what you want in plain English, and AI creates a custom Google Cloud project for you with the exact APIs and scopes needed.

### Supported Providers
- ✅ Google (full AI-powered setup)

### Features
- **Natural Language Input**: "I want to send emails from Gmail and create spreadsheets"
- **Smart API Detection**: AI automatically selects the right Google APIs
- **Billing Warnings**: Warns before enabling billing-required APIs
- **Project Creation**: Optionally creates a new Google Cloud project for you
- **Scope Optimization**: Requests only the minimum OAuth scopes needed

### Setup Process
1. Open the integration setup wizard
2. Choose "AI-Powered Setup"
3. Describe your use case in plain English
4. Review detected APIs and scopes
5. Decide: Create new project OR use existing
6. Complete OAuth credentials setup
7. Done!

### Rate Limits
**None** - You get Google's full API quotas for your project:
- Gmail API: 1 billion quota units/day
- Sheets API: 300 requests/minute per user
- Drive API: 1,000 requests/100 seconds per user
- Calendar API: 1,000,000 queries/day

### When to Use
- ✅ **Recommended for most users**
- ✅ You need more than the default tier's limits
- ✅ You want access to billing-required APIs
- ✅ You want dedicated quotas
- ✅ Production workflows

### Requirements
- Google account (free)
- ~2 minutes for setup
- Credit card for billing APIs (optional)

---

## Tier 3: Manual Setup (Advanced)

### Overview
Step-by-step instructions to configure OAuth with full control. Use your existing Google Cloud project or other provider accounts.

### Supported Providers
- ✅ **Google**: Create OAuth 2.0 credentials in Google Cloud Console
- ✅ **Slack**: Create a Slack app in your workspace
- ✅ **Xero**: Create a Xero app in developer portal
- ✅ **Microsoft 365**: Register an Azure AD application
- ✅ **HubSpot**: Create a HubSpot private app
- ✅ **Salesforce**: Create a Salesforce Connected App
- ✅ **Stripe**: Use API keys (not OAuth-based)

### When to Use
- ✅ You have an existing Google Cloud project
- ✅ You need enterprise-specific OAuth configurations
- ✅ You want custom scopes not covered by AI
- ✅ You're integrating with organization-wide resources
- ✅ Compliance requires specific OAuth apps

### Setup Process
The wizard provides step-by-step instructions with screenshots for:
1. Creating cloud/developer accounts
2. Enabling required APIs
3. Configuring OAuth consent screens
4. Creating OAuth 2.0 credentials
5. Copying credentials to Lodgeick

---

## Configuration for Administrators

### Enabling Default Tier

To offer the "Quick Start" option, add OAuth credentials to `site_config.json`:

```json
{
  "google_client_id": "123456789-abc123.apps.googleusercontent.com",
  "google_client_secret": "GOCSPX-your-client-secret",

  "slack_client_id": "123456789.987654321",
  "slack_client_secret": "your-slack-secret",

  "xero_client_id": "your-xero-client-id",
  "xero_client_secret": "your-xero-client-secret",

  "microsoft_client_id": "azure-app-client-id",
  "microsoft_client_secret": "azure-client-secret",

  "hubspot_client_id": "hubspot-app-id",
  "hubspot_client_secret": "hubspot-secret"
}
```

### Security Considerations

#### For Default Tier:
1. **API Key Rotation**: Rotate OAuth credentials quarterly
2. **Scope Minimization**: Only include essential scopes
3. **Usage Monitoring**: Track API usage per user
4. **Rate Limit Enforcement**: Implemented automatically
5. **Audit Logging**: All OAuth connections are logged

#### Recommended Default Tier Scopes:

**Google (Non-Billing Only)**:
```
https://www.googleapis.com/auth/gmail.send
https://www.googleapis.com/auth/spreadsheets
https://www.googleapis.com/auth/drive.file
https://www.googleapis.com/auth/calendar
```

**Slack**:
```
channels:read
channels:write
chat:write
users:read
```

**Xero**:
```
accounting.transactions
accounting.contacts
offline_access
```

---

## Usage Tracking & Rate Limiting

### How It Works
1. Users select a tier during OAuth setup
2. For "default" tier, usage is tracked in the `OAuth Usage Log` DocType
3. Rate limits are enforced before API calls
4. Users are notified when approaching limits (80% threshold)
5. Automatic daily/minute counter resets

### Checking Usage
```python
from lodgeick.lodgeick.doctype.oauth_usage_log.oauth_usage_log import get_usage_stats

# Get user's usage across all providers
stats = get_usage_stats(user="user@example.com")

# Get usage for specific provider
google_stats = get_usage_stats(user="user@example.com", provider="google")
```

### Monitoring Rate Limits
```python
from lodgeick.lodgeick.doctype.oauth_usage_log.oauth_usage_log import check_rate_limit

# Check if user can make more API calls
limit_check = check_rate_limit(
    user="user@example.com",
    provider="google",
    tier="default",
    api_name="gmail.googleapis.com"
)

if limit_check["allowed"]:
    print(f"Remaining today: {limit_check['remaining_today']}")
    print(f"Remaining this minute: {limit_check['remaining_minute']}")
else:
    print(f"Rate limit exceeded: {limit_check['message']}")
```

---

## API Reference

### Frontend

#### Get Tier Configuration
```javascript
import { call } from 'frappe-ui'

const config = await call('lodgeick.api.oauth_tiers.get_tier_config', {
  provider: 'google'
})

console.log(config.tiers.default.rate_limits)
```

#### Save OAuth Setup
```javascript
// Default tier
await call('lodgeick.api.oauth.save_user_oauth_setup', {
  provider: 'google',
  tier: 'default',
  use_default: true
})

// Manual tier
await call('lodgeick.api.oauth.save_user_oauth_setup', {
  provider: 'google',
  tier: 'manual',
  client_id: 'your-client-id',
  client_secret: 'your-client-secret'
})
```

### Backend

#### Check API Allowance
```python
from lodgeick.config.oauth_tiers import is_tier_allowed_for_api

result = is_tier_allowed_for_api(
    provider="google",
    tier="default",
    api_name="maps.googleapis.com",
    scopes=["https://www.googleapis.com/auth/maps"]
)

if not result["allowed"]:
    print(f"Not allowed: {result['reason']}")
```

---

## User Flow Examples

### Example 1: Quick Start User
1. User clicks "Connect Google Sheets"
2. Sees three tier options
3. Selects "Quick Start (Lodgeick Shared App)"
4. Sees rate limits: "500 requests/day"
5. Clicks "Continue" → Immediately redirected to Google OAuth
6. Authorizes and is done ✅

### Example 2: AI-Powered User
1. User clicks "Connect Google"
2. Selects "AI-Powered Setup"
3. Types: "I want to read and send emails, and create spreadsheets"
4. AI shows:
   - Gmail API (read + send scopes)
   - Sheets API (write scope)
   - ✅ No billing required
5. Chooses "Create new project for me"
6. AI creates project, enables APIs
7. Follows simple instructions to get OAuth credentials
8. Pastes credentials → Done ✅

### Example 3: Enterprise Manual User
1. Admin clicks "Connect Microsoft 365"
2. Selects "Manual Setup (Advanced)"
3. Follows step-by-step guide to:
   - Register Azure AD app
   - Configure tenant-wide admin consent
   - Set up custom redirect URIs
   - Generate client secret
4. Enters credentials
5. Tests connection
6. Done ✅ with enterprise-grade control

---

## Troubleshooting

### "Rate limit exceeded" for Default Tier
**Solution**: Upgrade to AI or Manual tier for unlimited quotas.

### "Default OAuth app not configured"
**Solution**: Admin needs to add credentials to `site_config.json`.

### "Billing required for this API"
**Solution**: Use AI or Manual tier to enable billing-required APIs like Maps or Vision.

### User wants to upgrade from Default to AI/Manual
**Solution**: Disconnect the integration and reconnect with a different tier.

---

## Best Practices

### For End Users:
1. **Start with Default Tier** for testing
2. **Upgrade to AI Tier** when ready for production
3. **Monitor your usage** in the account settings
4. **Use Manual Tier** only if you need custom configurations

### For Administrators:
1. **Enable Default Tier** for popular providers (Google, Slack, Xero)
2. **Don't enable billing APIs** in default tier to control costs
3. **Monitor aggregate usage** to prevent abuse
4. **Rotate API keys** quarterly for security
5. **Document tier policies** for your organization

### For Developers:
1. **Check rate limits** before making API calls
2. **Record API requests** to track usage
3. **Handle rate limit errors** gracefully
4. **Show upgrade prompts** when users approach limits

---

## Migration Guide

### Existing Users → Three-Tier System

If you already have OAuth credentials configured, they will automatically be treated as "manual" tier with unlimited quotas. No action needed.

### Adding Default Tier Support

1. Create OAuth apps for each provider you want to support
2. Add credentials to `site_config.json`
3. Configure rate limits in `oauth_tiers.py` if needed
4. Restart Frappe to load new config
5. Users will now see "Quick Start" option

---

## Future Enhancements

- [ ] AI-powered setup for more providers (Slack, Xero, Microsoft)
- [ ] Cost estimation for billing-required APIs
- [ ] Usage analytics dashboard
- [ ] Automatic tier recommendations based on usage patterns
- [ ] Tier upgrade prompts when limits are approaching
- [ ] White-label OAuth apps for enterprise customers

---

## Support

For questions or issues with the three-tier OAuth system:
- Check this guide first
- Review rate limit documentation for your provider
- Contact your Lodgeick administrator
- Open a GitHub issue at https://github.com/benjamen/lodgeick/issues
