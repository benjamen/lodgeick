# OAuth Setup Guide for Lodgeick

## Quick Fix for Google OAuth Error

The error you're seeing means the redirect URI needs to be updated in your Google Cloud Console.

### Fix the Google OAuth Redirect URI:

1. Go to https://console.cloud.google.com/apis/credentials
2. Click on your OAuth 2.0 Client ID
3. Under "Authorized redirect URIs", add:
   ```
   https://lodgeick.com/api/method/lodgeick.api.oauth.oauth_callback
   ```
4. Remove the old one:  
   ~~`https://lodgeick.com/frontend`~~
5. Click **Save**

### The Correct Redirect URI Format:

**Production:**
```
https://lodgeick.com/api/method/lodgeick.api.oauth.oauth_callback
```

**Local Development:**
```
http://lodgeick.com:8000/api/method/lodgeick.api.oauth.oauth_callback
```

Once you update the redirect URI in Google Cloud Console, the OAuth flow will work correctly!
