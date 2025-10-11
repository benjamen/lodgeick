# Copyright (c) 2025, Lodgeick and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class UserGoogleProject(Document):
	"""Stores Google Cloud projects created through AI setup assistant"""

	def validate(self):
		"""Validate project data"""
		if not self.user:
			self.user = frappe.session.user

	def before_insert(self):
		"""Set defaults before insert"""
		if not self.status:
			self.status = "Created"
