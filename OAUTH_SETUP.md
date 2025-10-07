# OAuth Setup Guide for Lodgeick

## Google OAuth (Gmail) Setup

### 1. Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project or select an existing one
3. Note your Project ID

### 2. Enable APIs

1. Navigate to **APIs & Services > Library**
2. Enable the following APIs:
   - Gmail API
   - Google Sheets API (optional, for sheets integration)
   - Google Drive API (optional, for drive integration)

### 3. Create OAuth 2.0 Credentials

1. Go to **APIs & Services > Credentials**
2. Click **Create Credentials > OAuth 2.0 Client ID**
3. If prompted, configure the OAuth consent screen:
   - User Type: External
   - App name: Lodgeick
   - User support email: Your email
   - Developer contact: Your email
   - Add scopes:
     - `https://www.googleapis.com/auth/gmail.readonly`
     - `https://www.googleapis.com/auth/gmail.send`
     - `https://www.googleapis.com/auth/spreadsheets`
     - `https://www.googleapis.com/auth/drive.file`
4. Create OAuth Client ID:
   - Application type: **Web application**
   - Name: Lodgeick Local
   - Authorized redirect URIs:
     - `http://localhost:5173/frontend/oauth/callback`
     - `http://localhost:8000/frontend/oauth/callback`
     - `http://localhost:8001/frontend/oauth/callback`

### 4. Configure Credentials in Frappe

Add your credentials to the site config:

```bash
# Inside Docker container
bench --site lodgeick.com set-config google_client_id "YOUR_CLIENT_ID.apps.googleusercontent.com"
bench --site lodgeick.com set-config google_client_secret "YOUR_CLIENT_SECRET"
```

Or manually edit `/workspace/development/frappe-bench/sites/lodgeick.com/site_config.json`:

```json
{
  "google_client_id": "YOUR_CLIENT_ID.apps.googleusercontent.com",
  "google_client_secret": "YOUR_CLIENT_SECRET"
}
```

### 5. Test OAuth Flow

1. Open http://localhost:5173/frontend
2. Click on Gmail app card
3. Click "Connect App"
4. OAuth popup should open
5. Sign in with Google and authorize
6. Popup should close automatically after success

## Other OAuth Providers

### Xero Setup

1. Go to [Xero Developer Portal](https://developer.xero.com/myapps)
2. Create new app
3. Add redirect URI: `http://localhost:5173/frontend/oauth/callback`
4. Add credentials:
```bash
bench --site lodgeick.com set-config xero_client_id "YOUR_CLIENT_ID"
bench --site lodgeick.com set-config xero_client_secret "YOUR_CLIENT_SECRET"
```

### Slack Setup

1. Go to [Slack API](https://api.slack.com/apps)
2. Create new app
3. Add redirect URI: `http://localhost:5173/frontend/oauth/callback`
4. Add credentials:
```bash
bench --site lodgeick.com set-config slack_client_id "YOUR_CLIENT_ID"
bench --site lodgeick.com set-config slack_client_secret "YOUR_CLIENT_SECRET"
```

## Troubleshooting

### Error: "The OAuth client was not found"

- Check that `google_client_id` and `google_client_secret` are set in site_config.json
- Verify credentials in Google Cloud Console

### Error: "Redirect URI mismatch"

- Add the exact redirect URI to your OAuth app in Google Cloud Console
- URI must match exactly: `http://localhost:5173/frontend/oauth/callback`

### Error: "Access blocked: Lodgeick has not completed the Google verification process"

- Add your test email to test users in OAuth consent screen
- Or publish the app (requires verification for production)

## Security Notes

- Never commit OAuth credentials to git
- Use environment variables or site_config.json (gitignored)
- Rotate credentials if exposed
- Use different credentials for dev/staging/production
