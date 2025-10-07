# Copyright (c) 2025, Lodgeick and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class IntegrationLog(Document):
	"""Log integration execution events"""

	def validate(self):
		"""Validate log data"""
		if not self.integration:
			frappe.throw("Integration is required")
		if not self.status:
			frappe.throw("Status is required")

	@staticmethod
	def create_log(integration_id, status, message, execution_time=None):
		"""Helper method to create a log entry"""
		log = frappe.get_doc({
			"doctype": "Integration Log",
			"integration": integration_id,
			"status": status,
			"message": message,
			"execution_time": execution_time
		})
		log.insert()
		frappe.db.commit()
		return log
