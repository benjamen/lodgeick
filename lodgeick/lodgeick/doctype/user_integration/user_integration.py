# Copyright (c) 2025, Lodgeick and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import json


class UserIntegration(Document):
	"""Manages user's active integrations"""

	def validate(self):
		"""Validate integration data"""
		if not self.flow_name:
			frappe.throw("Flow name is required")
		if not self.user:
			frappe.throw("User is required")

	def get_config_json(self):
		"""Get configuration as JSON"""
		if self.config:
			return json.loads(self.config)
		return {}

	def set_config_json(self, config_dict):
		"""Set configuration from dictionary"""
		self.config = json.dumps(config_dict)

	def mark_error(self, error_message):
		"""Mark integration as error"""
		self.status = "Error"
		self.error_message = error_message
		self.save()

	def mark_completed(self):
		"""Mark integration as completed"""
		self.status = "Completed"
		self.last_run = frappe.utils.now()
		self.error_message = None
		self.save()
