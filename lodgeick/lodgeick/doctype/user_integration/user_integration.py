# Copyright (c) 2025, Lodgeick and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import json


class UserIntegration(Document):
	"""Manages user's active integrations with n8n synchronization"""

	def validate(self):
		"""Validate integration data"""
		if not self.flow_name:
			frappe.throw("Flow name is required")
		if not self.user:
			frappe.throw("User is required")

	def after_insert(self):
		"""Create corresponding n8n workflow after integration is created"""
		if frappe.conf.get("n8n_auto_sync", True):
			try:
				from lodgeick.services.n8n_sync import get_n8n_sync_service
				sync_service = get_n8n_sync_service()
				sync_service.sync_integration_create(self)
			except Exception as e:
				frappe.log_error(f"Failed to create n8n workflow: {str(e)}", "N8N Sync Hook Error")
				# Don't prevent integration creation if n8n sync fails
				pass

	def on_update(self):
		"""Update corresponding n8n workflow when integration is updated"""
		if frappe.conf.get("n8n_auto_sync", True):
			# Check if this is a status change
			if self.has_value_changed("status"):
				self._sync_status_to_n8n()
			# Check if configuration changed
			elif self.has_value_changed("config") or self.has_value_changed("source_app") or self.has_value_changed("target_app"):
				self._sync_update_to_n8n()

	def on_trash(self):
		"""Delete corresponding n8n workflow when integration is deleted"""
		if frappe.conf.get("n8n_auto_sync", True):
			try:
				from lodgeick.services.n8n_sync import get_n8n_sync_service
				sync_service = get_n8n_sync_service()
				sync_service.sync_integration_delete(self)
			except Exception as e:
				frappe.log_error(f"Failed to delete n8n workflow: {str(e)}", "N8N Sync Hook Error")
				# Don't prevent integration deletion if n8n delete fails
				pass

	def _sync_update_to_n8n(self):
		"""Sync integration update to n8n"""
		try:
			from lodgeick.services.n8n_sync import get_n8n_sync_service
			sync_service = get_n8n_sync_service()
			sync_service.sync_integration_update(self)
		except Exception as e:
			frappe.log_error(f"Failed to update n8n workflow: {str(e)}", "N8N Sync Hook Error")

	def _sync_status_to_n8n(self):
		"""Sync status change to n8n (activate/deactivate workflow)"""
		try:
			from lodgeick.services.n8n_sync import get_n8n_sync_service
			sync_service = get_n8n_sync_service()
			sync_service.sync_integration_status(self, self.status)
		except Exception as e:
			frappe.log_error(f"Failed to sync status to n8n: {str(e)}", "N8N Sync Hook Error")

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

	def execute_workflow(self, input_data=None):
		"""
		Manually execute the n8n workflow

		Args:
			input_data: Optional input data for workflow

		Returns:
			Execution result from n8n
		"""
		if not self.workflow_id:
			frappe.throw("No n8n workflow associated with this integration")

		try:
			from lodgeick.services.n8n_client import get_n8n_client
			client = get_n8n_client()
			result = client.execute_workflow(self.workflow_id, input_data)

			self.last_run = frappe.utils.now()
			self.save(ignore_permissions=True)
			frappe.db.commit()

			return result
		except Exception as e:
			error_msg = f"Failed to execute workflow: {str(e)}"
			self.mark_error(error_msg)
			frappe.throw(error_msg)

	def get_execution_history(self, limit=10):
		"""
		Get execution history from n8n

		Args:
			limit: Maximum number of executions to return

		Returns:
			List of executions
		"""
		if not self.workflow_id:
			return []

		try:
			from lodgeick.services.n8n_client import get_n8n_client
			client = get_n8n_client()
			executions = client.list_executions(self.workflow_id)
			return executions[:limit]
		except Exception as e:
			frappe.log_error(f"Failed to get execution history: {str(e)}", "N8N Client Error")
			return []
