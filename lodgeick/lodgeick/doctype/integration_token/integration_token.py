# Copyright (c) 2025, Lodgeick and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class IntegrationToken(Document):
	"""Store OAuth tokens for external integrations"""

	def validate(self):
		"""Validate token data"""
		if not self.provider:
			frappe.throw("Provider is required")
		if not self.user:
			frappe.throw("User is required")

	def is_expired(self):
		"""Check if token is expired"""
		import frappe.utils
		if not self.expires_at:
			return False
		return frappe.utils.now_datetime() >= self.expires_at

	def get_token_data_json(self):
		"""Get token data as JSON"""
		import json
		if self.token_data:
			return json.loads(self.token_data)
		return {}
