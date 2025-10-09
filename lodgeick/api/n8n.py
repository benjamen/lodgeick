"""
N8N Integration API
REST API endpoints for managing n8n integrations
"""

import frappe
from frappe import _
import json


@frappe.whitelist()
def create_integration(flow_name, source_app, target_app, config):
	"""
	Create a new integration and sync to n8n

	Args:
		flow_name: Name of the integration flow
		source_app: Source application
		target_app: Target application
		config: Configuration JSON string or dict

	Returns:
		Created integration document
	"""
	try:
		# Parse config if it's a string
		if isinstance(config, str):
			config = json.loads(config)

		# Create integration document
		integration = frappe.get_doc({
			"doctype": "User Integration",
			"user": frappe.session.user,
			"flow_name": flow_name,
			"source_app": source_app,
			"target_app": target_app,
			"config": json.dumps(config),
			"status": "Active"
		})

		integration.insert(ignore_permissions=True)
		frappe.db.commit()

		return {
			"success": True,
			"integration_id": integration.name,
			"workflow_id": integration.workflow_id,
			"message": "Integration created and synced to n8n"
		}

	except Exception as e:
		frappe.log_error(f"Failed to create integration: {str(e)}", "Integration API Error")
		return {
			"success": False,
			"error": str(e)
		}


@frappe.whitelist()
def update_integration(integration_id, config=None, status=None):
	"""
	Update an integration and sync to n8n

	Args:
		integration_id: Integration document name
		config: Updated configuration (optional)
		status: Updated status (optional)

	Returns:
		Success status
	"""
	try:
		integration = frappe.get_doc("User Integration", integration_id)

		# Check permissions
		if integration.user != frappe.session.user and not frappe.has_permission("User Integration", "write"):
			frappe.throw(_("You don't have permission to update this integration"))

		# Update config if provided
		if config:
			if isinstance(config, str):
				config = json.loads(config)
			integration.config = json.dumps(config)

		# Update status if provided
		if status:
			integration.status = status

		integration.save(ignore_permissions=True)
		frappe.db.commit()

		return {
			"success": True,
			"message": "Integration updated and synced to n8n"
		}

	except Exception as e:
		frappe.log_error(f"Failed to update integration: {str(e)}", "Integration API Error")
		return {
			"success": False,
			"error": str(e)
		}


@frappe.whitelist()
def delete_integration(integration_id):
	"""
	Delete an integration and remove from n8n

	Args:
		integration_id: Integration document name

	Returns:
		Success status
	"""
	try:
		integration = frappe.get_doc("User Integration", integration_id)

		# Check permissions
		if integration.user != frappe.session.user and not frappe.has_permission("User Integration", "delete"):
			frappe.throw(_("You don't have permission to delete this integration"))

		integration.delete()
		frappe.db.commit()

		return {
			"success": True,
			"message": "Integration deleted and removed from n8n"
		}

	except Exception as e:
		frappe.log_error(f"Failed to delete integration: {str(e)}", "Integration API Error")
		return {
			"success": False,
			"error": str(e)
		}


@frappe.whitelist()
def execute_integration(integration_id, input_data=None):
	"""
	Manually execute an integration workflow

	Args:
		integration_id: Integration document name
		input_data: Optional input data for workflow

	Returns:
		Execution result from n8n
	"""
	try:
		integration = frappe.get_doc("User Integration", integration_id)

		# Check permissions
		if integration.user != frappe.session.user and not frappe.has_permission("User Integration", "read"):
			frappe.throw(_("You don't have permission to execute this integration"))

		# Parse input data if string
		if input_data and isinstance(input_data, str):
			input_data = json.loads(input_data)

		result = integration.execute_workflow(input_data)

		return {
			"success": True,
			"execution_result": result
		}

	except Exception as e:
		frappe.log_error(f"Failed to execute integration: {str(e)}", "Integration API Error")
		return {
			"success": False,
			"error": str(e)
		}


@frappe.whitelist()
def get_integration_status(integration_id):
	"""
	Get integration status and n8n workflow info

	Args:
		integration_id: Integration document name

	Returns:
		Integration status and workflow info
	"""
	try:
		integration = frappe.get_doc("User Integration", integration_id)

		# Check permissions
		if integration.user != frappe.session.user and not frappe.has_permission("User Integration", "read"):
			frappe.throw(_("You don't have permission to view this integration"))

		# Get n8n workflow status if workflow exists
		workflow_info = None
		if integration.workflow_id:
			try:
				from lodgeick.services.n8n_client import get_n8n_client
				client = get_n8n_client()
				workflow = client.get_workflow(integration.workflow_id)
				workflow_info = {
					"id": workflow.get("id"),
					"name": workflow.get("name"),
					"active": workflow.get("active"),
					"createdAt": workflow.get("createdAt"),
					"updatedAt": workflow.get("updatedAt")
				}
			except Exception as e:
				frappe.log_error(f"Failed to get n8n workflow info: {str(e)}", "N8N Client Error")

		return {
			"success": True,
			"integration": {
				"id": integration.name,
				"flow_name": integration.flow_name,
				"source_app": integration.source_app,
				"target_app": integration.target_app,
				"status": integration.status,
				"workflow_id": integration.workflow_id,
				"last_run": integration.last_run,
				"error_message": integration.error_message
			},
			"workflow_info": workflow_info
		}

	except Exception as e:
		frappe.log_error(f"Failed to get integration status: {str(e)}", "Integration API Error")
		return {
			"success": False,
			"error": str(e)
		}


@frappe.whitelist()
def get_execution_history(integration_id, limit=10):
	"""
	Get execution history for an integration

	Args:
		integration_id: Integration document name
		limit: Maximum number of executions to return

	Returns:
		List of executions
	"""
	try:
		integration = frappe.get_doc("User Integration", integration_id)

		# Check permissions
		if integration.user != frappe.session.user and not frappe.has_permission("User Integration", "read"):
			frappe.throw(_("You don't have permission to view this integration"))

		executions = integration.get_execution_history(int(limit))

		return {
			"success": True,
			"executions": executions
		}

	except Exception as e:
		frappe.log_error(f"Failed to get execution history: {str(e)}", "Integration API Error")
		return {
			"success": False,
			"error": str(e)
		}


@frappe.whitelist()
def trigger_sync_job():
	"""
	Manually trigger n8n sync job

	Returns:
		Job enqueue status
	"""
	# Check if user has permission
	if not frappe.has_permission("User Integration", "write"):
		frappe.throw(_("You don't have permission to trigger sync jobs"))

	try:
		from lodgeick.tasks.n8n_sync_job import enqueue_sync_job
		enqueue_sync_job()

		return {
			"success": True,
			"message": "Sync job enqueued successfully"
		}

	except Exception as e:
		frappe.log_error(f"Failed to trigger sync job: {str(e)}", "Integration API Error")
		return {
			"success": False,
			"error": str(e)
		}


@frappe.whitelist()
def list_user_integrations(status=None):
	"""
	List all integrations for current user

	Args:
		status: Optional status filter

	Returns:
		List of integrations
	"""
	try:
		filters = {"user": frappe.session.user}
		if status:
			filters["status"] = status

		integrations = frappe.get_all(
			"User Integration",
			fields=["name", "flow_name", "source_app", "target_app", "status", "workflow_id", "last_run"],
			filters=filters,
			order_by="modified desc"
		)

		return {
			"success": True,
			"integrations": integrations
		}

	except Exception as e:
		frappe.log_error(f"Failed to list integrations: {str(e)}", "Integration API Error")
		return {
			"success": False,
			"error": str(e)
		}
