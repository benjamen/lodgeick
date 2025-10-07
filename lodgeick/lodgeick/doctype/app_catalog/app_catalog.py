# Copyright (c) 2025, Lodgeick and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class AppCatalog(Document):
	"""Catalog of available SaaS apps for integration"""

	def validate(self):
		"""Validate app data"""
		if not self.app_name:
			frappe.throw("App name is required")
		if not self.display_name:
			frappe.throw("Display name is required")

	def get_use_cases_list(self):
		"""Get list of use cases"""
		return [uc.use_case_name for uc in self.use_cases]
