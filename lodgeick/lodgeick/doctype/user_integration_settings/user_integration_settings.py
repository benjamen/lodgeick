# Copyright (c) 2025, Lodgeick and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime


class UserIntegrationSettings(Document):
	def before_insert(self):
		"""Set created_at timestamp"""
		self.created_at = datetime.now()
		self.modified_at = datetime.now()

	def before_save(self):
		"""Update modified_at timestamp"""
		self.modified_at = datetime.now()

	def validate(self):
		"""Validate user can only create settings for themselves"""
		if self.user != frappe.session.user and not frappe.has_permission("User Integration Settings", "write"):
			frappe.throw("You can only create settings for your own account")


@frappe.whitelist()
def get_user_settings(app_name):
	"""
	Get integration settings for current user and app

	Args:
		app_name: Name of the app from App Catalog

	Returns:
		dict: User settings or None
	"""
	user = frappe.session.user

	settings = frappe.db.get_value(
		"User Integration Settings",
		{"user": user, "app_name": app_name},
		["name", "is_active", "settings"],
		as_dict=True
	)

	return settings


@frappe.whitelist()
def update_user_settings(app_name, settings, is_active=True):
	"""
	Create or update integration settings for current user

	Args:
		app_name: Name of the app from App Catalog
		settings: JSON settings object
		is_active: Whether integration is active

	Returns:
		dict: Updated settings document
	"""
	import json

	user = frappe.session.user

	# Check if settings already exist
	existing = frappe.db.get_value(
		"User Integration Settings",
		{"user": user, "app_name": app_name},
		"name"
	)

	if existing:
		# Update existing
		doc = frappe.get_doc("User Integration Settings", existing)
		doc.settings = json.dumps(settings) if isinstance(settings, dict) else settings
		doc.is_active = is_active
		doc.save()
	else:
		# Create new
		doc = frappe.get_doc({
			"doctype": "User Integration Settings",
			"user": user,
			"app_name": app_name,
			"settings": json.dumps(settings) if isinstance(settings, dict) else settings,
			"is_active": is_active
		})
		doc.insert()

	frappe.db.commit()

	return doc.as_dict()


@frappe.whitelist()
def get_user_integrations():
	"""
	Get all active integrations for current user

	Returns:
		list: List of user integration settings
	"""
	user = frappe.session.user

	integrations = frappe.get_all(
		"User Integration Settings",
		filters={"user": user, "is_active": 1},
		fields=["name", "app_name", "settings", "created_at", "modified_at"]
	)

	return integrations
