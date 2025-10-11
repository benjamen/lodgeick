"""
OAuth Usage Log DocType
Tracks API usage for rate limiting on shared OAuth apps
"""

import frappe
from frappe.model.document import Document
from datetime import datetime, timedelta
from lodgeick.config.oauth_tiers import get_rate_limit


class OAuthUsageLog(Document):
	"""Track OAuth API usage for rate limiting"""

	def before_save(self):
		"""Reset counters if time periods have elapsed"""
		now = datetime.now()

		# Reset daily counter if a day has passed
		if self.last_reset_daily:
			last_reset = frappe.utils.get_datetime(self.last_reset_daily)
			if (now - last_reset).total_seconds() > 86400:  # 24 hours
				self.requests_today = 0
				self.last_reset_daily = now
				self.warning_sent = 0

		# Reset minute counter if a minute has passed
		if self.last_reset_minute:
			last_reset = frappe.utils.get_datetime(self.last_reset_minute)
			if (now - last_reset).total_seconds() > 60:  # 1 minute
				self.requests_this_minute = 0
				self.last_reset_minute = now

		# Update status based on limits
		self.update_status()

	def update_status(self):
		"""Update status based on current usage"""
		if self.daily_limit and self.requests_today >= self.daily_limit:
			self.status = "Limit Reached"
		elif self.minute_limit and self.requests_this_minute >= self.minute_limit:
			self.status = "Limit Reached"
		elif self.daily_limit and self.requests_today >= (self.daily_limit * 0.8):
			self.status = "Warning"
		else:
			self.status = "Active"


@frappe.whitelist()
def check_rate_limit(user: str, provider: str, tier: str, api_name: str = None) -> dict:
	"""
	Check if user has exceeded rate limits

	Args:
		user: User email
		provider: OAuth provider (google, slack, etc.)
		tier: OAuth tier (default, ai, manual)
		api_name: Optional specific API name

	Returns:
		{
			"allowed": bool,
			"remaining_today": int,
			"remaining_minute": int,
			"message": str
		}
	"""
	# AI and manual tiers have no rate limits
	if tier in ["ai", "manual"]:
		return {
			"allowed": True,
			"remaining_today": None,
			"remaining_minute": None,
			"message": "Unlimited"
		}

	# Get rate limit configuration
	rate_config = get_rate_limit(provider, tier, api_name)
	if not rate_config:
		return {
			"allowed": True,
			"remaining_today": None,
			"remaining_minute": None,
			"message": "No limits configured"
		}

	# Find or create usage log
	usage_key = f"{user}-{provider}-{tier}"
	if api_name:
		usage_key += f"-{api_name}"

	usage_log = frappe.db.get_value(
		"OAuth Usage Log",
		{
			"user": user,
			"provider": provider,
			"tier": tier,
			"api_name": api_name or ""
		},
		["name", "requests_today", "requests_this_minute", "daily_limit", "minute_limit", "status"],
		as_dict=True
	)

	if not usage_log:
		# Create new usage log
		daily_limit = rate_config.get("requests_per_day")
		minute_limit = rate_config.get("requests_per_minute")

		usage_log = frappe.get_doc({
			"doctype": "OAuth Usage Log",
			"user": user,
			"provider": provider,
			"tier": tier,
			"api_name": api_name or "",
			"requests_today": 0,
			"requests_this_minute": 0,
			"daily_limit": daily_limit,
			"minute_limit": minute_limit,
			"last_reset_daily": datetime.now(),
			"last_reset_minute": datetime.now(),
			"status": "Active"
		})
		usage_log.insert(ignore_permissions=True)
		frappe.db.commit()

		return {
			"allowed": True,
			"remaining_today": daily_limit,
			"remaining_minute": minute_limit,
			"message": "New usage tracker created"
		}

	# Check limits
	if usage_log.status == "Limit Reached":
		remaining_daily = usage_log.daily_limit - usage_log.requests_today if usage_log.daily_limit else None
		remaining_minute = usage_log.minute_limit - usage_log.requests_this_minute if usage_log.minute_limit else None

		return {
			"allowed": False,
			"remaining_today": max(0, remaining_daily) if remaining_daily is not None else None,
			"remaining_minute": max(0, remaining_minute) if remaining_minute is not None else None,
			"message": "Rate limit exceeded. Please upgrade to AI or Manual setup for unlimited access."
		}

	remaining_daily = usage_log.daily_limit - usage_log.requests_today if usage_log.daily_limit else None
	remaining_minute = usage_log.minute_limit - usage_log.requests_this_minute if usage_log.minute_limit else None

	return {
		"allowed": True,
		"remaining_today": remaining_daily,
		"remaining_minute": remaining_minute,
		"message": "OK"
	}


@frappe.whitelist()
def record_api_request(user: str, provider: str, tier: str, api_name: str = None):
	"""
	Record an API request for rate limiting

	Args:
		user: User email
		provider: OAuth provider
		tier: OAuth tier
		api_name: Optional API name
	"""
	# Skip tracking for ai/manual tiers
	if tier in ["ai", "manual"]:
		return

	# Find usage log
	usage_log = frappe.db.get_value(
		"OAuth Usage Log",
		{
			"user": user,
			"provider": provider,
			"tier": tier,
			"api_name": api_name or ""
		},
		"name"
	)

	if usage_log:
		doc = frappe.get_doc("OAuth Usage Log", usage_log)
		doc.requests_today = (doc.requests_today or 0) + 1
		doc.requests_this_minute = (doc.requests_this_minute or 0) + 1
		doc.last_request_time = datetime.now()
		doc.save(ignore_permissions=True)
		frappe.db.commit()


@frappe.whitelist()
def get_usage_stats(user: str, provider: str = None) -> list:
	"""
	Get usage statistics for a user

	Args:
		user: User email
		provider: Optional filter by provider

	Returns:
		List of usage statistics
	"""
	filters = {"user": user}
	if provider:
		filters["provider"] = provider

	usage_logs = frappe.get_all(
		"OAuth Usage Log",
		filters=filters,
		fields=[
			"provider",
			"tier",
			"api_name",
			"requests_today",
			"daily_limit",
			"requests_this_minute",
			"minute_limit",
			"status",
			"last_request_time"
		]
	)

	return usage_logs
