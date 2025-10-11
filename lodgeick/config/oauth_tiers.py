"""
OAuth Setup Tier Configuration
Defines three-tier setup options for different OAuth providers
"""

# Three-tier system:
# 1. Default (Lodgeick Shared App) - Quick start, non-billing only, rate limited
# 2. AI-Powered - User creates own project via AI wizard, unlimited
# 3. Manual - User provides existing credentials, unlimited

OAUTH_TIER_CONFIG = {
	"google": {
		"provider_name": "Google",
		"icon": "🔵",
		"has_ai_setup": True,
		"tiers": {
			"default": {
				"enabled": True,
				"label": "Quick Start (Lodgeick Shared App)",
				"description": "Use our shared OAuth app - no setup required",
				"setup_time": "Instant",
				"icon": "⚡",
				"advantages": [
					"No Google Cloud account needed",
					"Start using in seconds",
					"Perfect for testing and personal use"
				],
				"limitations": [
					"Shared rate limits with other users",
					"Gmail: 100 emails/day",
					"Sheets: 500 requests/day",
					"Drive: 1000 operations/day",
					"Not available for billing-required APIs"
				],
				"allowed_apis": [
					"sheets.googleapis.com",
					"drive.googleapis.com",
					"calendar.googleapis.com",
					"gmail.googleapis.com"  # Send only, not read
				],
				"disallowed_scopes": [
					"https://mail.google.com/",  # Full Gmail access
					"https://www.googleapis.com/auth/gmail.readonly",
					"https://www.googleapis.com/auth/gmail.modify"
				],
				"rate_limits": {
					"gmail.googleapis.com": {
						"requests_per_day": 100,
						"requests_per_minute": 5
					},
					"sheets.googleapis.com": {
						"requests_per_day": 500,
						"requests_per_minute": 50
					},
					"drive.googleapis.com": {
						"requests_per_day": 1000,
						"requests_per_minute": 100
					},
					"calendar.googleapis.com": {
						"requests_per_day": 500,
						"requests_per_minute": 50
					}
				},
				"requires": []
			},
			"ai": {
				"enabled": True,
				"label": "AI-Powered Setup (Recommended)",
				"description": "Create your own Google Cloud project in 2 minutes",
				"setup_time": "~2 minutes",
				"icon": "🤖",
				"advantages": [
					"Unlimited API quota",
					"Full control over your project",
					"Access to all APIs including Maps, Vision, etc.",
					"AI guides you through setup"
				],
				"limitations": [
					"Billing required for some APIs (Maps, Vision, etc.)"
				],
				"allowed_apis": "all",
				"rate_limits": None,
				"requires": ["Google account"]
			},
			"manual": {
				"enabled": True,
				"label": "Manual Setup (Advanced)",
				"description": "Use your existing Google Cloud project",
				"setup_time": "~10 minutes",
				"icon": "🔧",
				"advantages": [
					"Full control over configuration",
					"Use existing billing account",
					"Enterprise-grade setup"
				],
				"limitations": [],
				"allowed_apis": "all",
				"rate_limits": None,
				"requires": ["Existing Google Cloud project", "Technical knowledge"]
			}
		}
	},

	"slack": {
		"provider_name": "Slack",
		"icon": "💬",
		"has_ai_setup": False,
		"tiers": {
			"default": {
				"enabled": True,
				"label": "Quick Start (Lodgeick Shared App)",
				"description": "Use our shared Slack app",
				"setup_time": "Instant",
				"icon": "⚡",
				"advantages": [
					"No Slack app creation needed",
					"Start in seconds",
					"Perfect for personal workspaces"
				],
				"limitations": [
					"Shared rate limits (Tier 2: 20 req/min)",
					"Cannot customize app name/icon",
					"May show 'via Lodgeick' in messages"
				],
				"rate_limits": {
					"requests_per_minute": 20,
					"requests_per_day": 10000
				},
				"requires": []
			},
			"manual": {
				"enabled": True,
				"label": "Custom Slack App",
				"description": "Create your own Slack app",
				"setup_time": "~5 minutes",
				"icon": "🔧",
				"advantages": [
					"Higher rate limits (Tier 3: 50 req/min)",
					"Custom app name and icon",
					"Full control over permissions",
					"Better for business use"
				],
				"limitations": [],
				"rate_limits": None,
				"requires": ["Slack workspace admin access"]
			}
		}
	},

	"xero": {
		"provider_name": "Xero",
		"icon": "💰",
		"has_ai_setup": False,
		"tiers": {
			"default": {
				"enabled": True,
				"label": "Quick Start (Lodgeick Shared App)",
				"description": "Use our shared Xero app",
				"setup_time": "Instant",
				"icon": "⚡",
				"advantages": [
					"No Xero app creation needed",
					"Connect in seconds",
					"Perfect for single organization"
				],
				"limitations": [
					"Rate limits: 60 calls/minute",
					"Single organization connection",
					"Shows 'Lodgeick' in audit logs"
				],
				"rate_limits": {
					"requests_per_minute": 60,
					"requests_per_day": 5000
				},
				"requires": []
			},
			"manual": {
				"enabled": True,
				"label": "Custom Xero App",
				"description": "Create your own Xero app",
				"setup_time": "~5 minutes",
				"icon": "🔧",
				"advantages": [
					"Higher rate limits (10,000/day)",
					"Multiple organization support",
					"Custom app branding",
					"Better for accounting firms"
				],
				"limitations": [],
				"rate_limits": None,
				"requires": ["Xero developer account"]
			}
		}
	},

	"microsoft": {
		"provider_name": "Microsoft 365",
		"icon": "🪟",
		"has_ai_setup": False,
		"tiers": {
			"default": {
				"enabled": True,
				"label": "Quick Start (Lodgeick Shared App)",
				"description": "Use our shared Microsoft app",
				"setup_time": "Instant",
				"icon": "⚡",
				"advantages": [
					"No Azure AD setup needed",
					"Access Outlook, OneDrive, Teams",
					"Start immediately"
				],
				"limitations": [
					"Shared rate limits",
					"Outlook: 100 emails/day",
					"OneDrive: 1000 operations/day",
					"Cannot access organization-wide data"
				],
				"rate_limits": {
					"outlook": {
						"requests_per_day": 100,
						"requests_per_minute": 10
					},
					"onedrive": {
						"requests_per_day": 1000,
						"requests_per_minute": 100
					},
					"teams": {
						"requests_per_day": 500,
						"requests_per_minute": 50
					}
				},
				"requires": []
			},
			"manual": {
				"enabled": True,
				"label": "Custom Azure App",
				"description": "Register your own Azure AD app",
				"setup_time": "~10 minutes",
				"icon": "🔧",
				"advantages": [
					"Unlimited API quota",
					"Organization-wide access",
					"Admin consent for tenant",
					"Enterprise features"
				],
				"limitations": [],
				"rate_limits": None,
				"requires": ["Azure AD tenant", "Admin permissions"]
			}
		}
	},

	"hubspot": {
		"provider_name": "HubSpot",
		"icon": "🟠",
		"has_ai_setup": False,
		"tiers": {
			"default": {
				"enabled": True,
				"label": "Quick Start (Lodgeick Shared App)",
				"description": "Use our shared HubSpot app",
				"setup_time": "Instant",
				"icon": "⚡",
				"advantages": [
					"No HubSpot app setup needed",
					"Connect instantly",
					"Access contacts, deals, companies"
				],
				"limitations": [
					"Rate limits: 100 requests/10 seconds",
					"Shared daily limit: 250,000 calls",
					"Single portal connection"
				],
				"rate_limits": {
					"requests_per_10_seconds": 100,
					"requests_per_day": 250000
				},
				"requires": []
			},
			"manual": {
				"enabled": True,
				"label": "Private HubSpot App",
				"description": "Create your own HubSpot app",
				"setup_time": "~5 minutes",
				"icon": "🔧",
				"advantages": [
					"Higher rate limits (150 req/10s)",
					"Multiple portals",
					"Custom webhooks",
					"Better for agencies"
				],
				"limitations": [],
				"rate_limits": None,
				"requires": ["HubSpot developer account"]
			}
		}
	},

	"salesforce": {
		"provider_name": "Salesforce",
		"icon": "☁️",
		"has_ai_setup": False,
		"tiers": {
			"manual": {
				"enabled": True,
				"label": "Connected App Setup",
				"description": "Create Salesforce Connected App",
				"setup_time": "~10 minutes",
				"icon": "🔧",
				"advantages": [
					"Full Salesforce API access",
					"Organization-specific",
					"Secure OAuth 2.0"
				],
				"limitations": [
					"Requires Salesforce admin access",
					"More complex setup"
				],
				"rate_limits": None,
				"requires": ["Salesforce org", "Admin permissions"]
			}
		},
		"note": "Salesforce requires organization-specific Connected Apps. Shared apps are not recommended for security reasons."
	},

	"stripe": {
		"provider_name": "Stripe",
		"icon": "💳",
		"has_ai_setup": False,
		"tiers": {
			"manual": {
				"enabled": True,
				"label": "Connect Your Stripe Account",
				"description": "Use your Stripe API keys",
				"setup_time": "~2 minutes",
				"icon": "🔧",
				"advantages": [
					"Direct access to your payments",
					"Secure API key authentication",
					"Real-time webhooks"
				],
				"limitations": [],
				"rate_limits": None,
				"requires": ["Stripe account"]
			}
		},
		"note": "Stripe uses API keys instead of OAuth. Each user must connect their own account."
	}
}


def get_available_tiers(provider: str) -> dict:
	"""
	Get available OAuth tiers for a provider

	Args:
		provider: Provider name (google, slack, xero, etc.)

	Returns:
		Tier configuration for the provider
	"""
	return OAUTH_TIER_CONFIG.get(provider, {})


def is_tier_allowed_for_api(provider: str, tier: str, api_name: str, scopes: list = None) -> dict:
	"""
	Check if a specific API/scope is allowed for a tier

	Args:
		provider: Provider name
		tier: Tier name (default, ai, manual)
		api_name: API name (e.g., gmail.googleapis.com)
		scopes: List of OAuth scopes

	Returns:
		{
			"allowed": bool,
			"reason": str (if not allowed)
		}
	"""
	provider_config = OAUTH_TIER_CONFIG.get(provider, {})
	tier_config = provider_config.get("tiers", {}).get(tier, {})

	if not tier_config:
		return {"allowed": False, "reason": "Invalid tier"}

	# Manual/AI tiers allow everything
	if tier in ["manual", "ai"]:
		return {"allowed": True}

	# Default tier - check restrictions
	allowed_apis = tier_config.get("allowed_apis", [])
	disallowed_scopes = tier_config.get("disallowed_scopes", [])

	# Check if API is allowed
	if allowed_apis != "all":
		if api_name not in allowed_apis:
			return {
				"allowed": False,
				"reason": f"{api_name} requires AI or Manual setup. Not available in Quick Start tier."
			}

	# Check if any scope is disallowed
	if scopes and disallowed_scopes:
		for scope in scopes:
			if scope in disallowed_scopes:
				return {
					"allowed": False,
					"reason": f"Full access scope requires AI or Manual setup for privacy/security."
				}

	return {"allowed": True}


def get_rate_limit(provider: str, tier: str, api_name: str = None) -> dict:
	"""
	Get rate limit configuration for a provider/tier/api

	Args:
		provider: Provider name
		tier: Tier name
		api_name: Optional specific API name

	Returns:
		Rate limit configuration or None
	"""
	provider_config = OAUTH_TIER_CONFIG.get(provider, {})
	tier_config = provider_config.get("tiers", {}).get(tier, {})
	rate_limits = tier_config.get("rate_limits")

	if not rate_limits:
		return None

	# If api_name specified and rate_limits is nested by API
	if api_name and isinstance(rate_limits, dict) and api_name in rate_limits:
		return rate_limits[api_name]

	return rate_limits
