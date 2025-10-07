"""
Integrations API for Lodgeick
Handles integration activation, status, and management
"""

import frappe
from frappe import _
import requests
import json


@frappe.whitelist()
def activate_integration(flow_name, source_app, target_app, config=None):
	"""
	Activate a new integration

	Args:
		flow_name: Name of the integration flow
		source_app: Source application (e.g., 'xero')
		target_app: Target application (e.g., 'google_sheets')
		config: JSON configuration for the integration

	Returns:
		dict: Integration details and status
	"""
	user = frappe.session.user

	# Verify user has tokens for both apps
	source_token = get_user_token(user, source_app)
	target_token = get_user_token(user, target_app)

	if not source_token:
		return {
			"success": False,
			"error": f"No authentication found for {source_app}. Please connect your account first."
		}

	if not target_token:
		return {
			"success": False,
			"error": f"No authentication found for {target_app}. Please connect your account first."
		}

	# Get workflow template ID from app catalog
	workflow_template_id = get_workflow_template(flow_name, source_app, target_app)

	if not workflow_template_id:
		return {
			"success": False,
			"error": "Workflow template not found for this integration"
		}

	# Create n8n workflow from template
	workflow_id = create_n8n_workflow(
		workflow_template_id,
		source_token,
		target_token,
		config
	)

	# Create User Integration record
	integration = frappe.get_doc({
		"doctype": "User Integration",
		"user": user,
		"flow_name": flow_name,
		"source_app": source_app,
		"target_app": target_app,
		"config": json.dumps(config) if config else None,
		"workflow_id": workflow_id,
		"status": "Active"
	})
	integration.insert()
	frappe.db.commit()

	# Create log entry
	from lodgeick.lodgeick.doctype.integration_log.integration_log import IntegrationLog
	IntegrationLog.create_log(
		integration.name,
		"Started",
		f"Integration {flow_name} activated successfully"
	)

	return {
		"success": True,
		"integration_id": integration.name,
		"message": "Integration activated successfully",
		"workflow_id": workflow_id
	}


@frappe.whitelist()
def get_integration_status(integration_id):
	"""
	Get status of an integration

	Args:
		integration_id: Integration document name

	Returns:
		dict: Integration status and details
	"""
	integration = frappe.get_doc("User Integration", integration_id)

	# Check permission
	if integration.user != frappe.session.user and not frappe.has_permission("User Integration", "read"):
		frappe.throw(_("Not permitted"))

	# Get recent logs
	logs = frappe.get_all(
		"Integration Log",
		filters={"integration": integration_id},
		fields=["status", "message", "timestamp"],
		order_by="timestamp desc",
		limit=10
	)

	return {
		"success": True,
		"integration": {
			"name": integration.name,
			"flow_name": integration.flow_name,
			"source_app": integration.source_app,
			"target_app": integration.target_app,
			"status": integration.status,
			"last_run": integration.last_run,
			"error_message": integration.error_message
		},
		"logs": logs
	}


@frappe.whitelist()
def list_user_integrations():
	"""
	List all integrations for current user

	Returns:
		dict: List of integrations
	"""
	user = frappe.session.user

	integrations = frappe.get_all(
		"User Integration",
		filters={"user": user},
		fields=[
			"name",
			"flow_name",
			"source_app",
			"target_app",
			"status",
			"last_run",
			"modified"
		],
		order_by="modified desc"
	)

	return {
		"success": True,
		"integrations": integrations
	}


@frappe.whitelist()
def pause_integration(integration_id):
	"""
	Pause an active integration

	Args:
		integration_id: Integration document name

	Returns:
		dict: Success status
	"""
	integration = frappe.get_doc("User Integration", integration_id)

	# Check permission
	if integration.user != frappe.session.user and not frappe.has_permission("User Integration", "write"):
		frappe.throw(_("Not permitted"))

	# Deactivate n8n workflow
	deactivate_n8n_workflow(integration.workflow_id)

	integration.status = "Paused"
	integration.save()
	frappe.db.commit()

	from lodgeick.lodgeick.doctype.integration_log.integration_log import IntegrationLog
	IntegrationLog.create_log(
		integration.name,
		"Warning",
		"Integration paused by user"
	)

	return {
		"success": True,
		"message": "Integration paused successfully"
	}


@frappe.whitelist()
def delete_integration(integration_id):
	"""
	Delete an integration

	Args:
		integration_id: Integration document name

	Returns:
		dict: Success status
	"""
	integration = frappe.get_doc("User Integration", integration_id)

	# Check permission
	if integration.user != frappe.session.user and not frappe.has_permission("User Integration", "delete"):
		frappe.throw(_("Not permitted"))

	# Delete n8n workflow
	delete_n8n_workflow(integration.workflow_id)

	integration_name = integration.flow_name
	frappe.delete_doc("User Integration", integration_id)
	frappe.db.commit()

	return {
		"success": True,
		"message": f"Integration '{integration_name}' deleted successfully"
	}


# Helper functions

def get_user_token(user, provider):
	"""Get user's OAuth token for a provider"""
	try:
		token = frappe.get_doc("Integration Token", {
			"user": user,
			"provider": provider
		})
		return token
	except frappe.DoesNotExistError:
		return None


def get_workflow_template(flow_name, source_app, target_app):
	"""Get workflow template ID from App Catalog"""
	# Get source app
	try:
		app_catalog = frappe.get_doc("App Catalog", source_app)

		# Find matching use case
		for use_case in app_catalog.use_cases:
			if use_case.use_case_name == flow_name:
				return use_case.workflow_template_id

		return None
	except frappe.DoesNotExistError:
		return None


def create_n8n_workflow(template_id, source_token, target_token, config):
	"""
	Create and activate n8n workflow from template

	Args:
		template_id: n8n workflow template ID
		source_token: Source app token
		target_token: Target app token
		config: User configuration

	Returns:
		str: New workflow ID
	"""
	# TODO: Implement n8n API integration
	# This is a placeholder - actual implementation will:
	# 1. Clone workflow template via n8n API
	# 2. Inject credentials from tokens
	# 3. Apply user configuration
	# 4. Activate workflow
	# 5. Set up webhook callback to Frappe

	n8n_url = frappe.conf.get("n8n_api_url")
	n8n_api_key = frappe.conf.get("n8n_api_key")

	if not n8n_url or not n8n_api_key:
		frappe.log_error("n8n not configured", "Lodgeick Integration")
		return f"workflow_{frappe.generate_hash(length=16)}"  # Fallback for development

	# Placeholder: Return mock workflow ID
	return f"workflow_{frappe.generate_hash(length=16)}"


def deactivate_n8n_workflow(workflow_id):
	"""Deactivate n8n workflow"""
	# TODO: Implement n8n API call to deactivate workflow
	pass


def delete_n8n_workflow(workflow_id):
	"""Delete n8n workflow"""
	# TODO: Implement n8n API call to delete workflow
	pass


@frappe.whitelist(allow_guest=True)
def n8n_webhook_callback():
	"""
	Webhook endpoint for n8n to report execution status

	Expected payload:
	{
		"workflow_id": "...",
		"status": "success|error",
		"message": "...",
		"execution_time": 1.23
	}
	"""
	data = frappe.local.form_dict

	workflow_id = data.get("workflow_id")
	status = data.get("status")
	message = data.get("message")
	execution_time = data.get("execution_time")

	# Find integration by workflow ID
	integrations = frappe.get_all(
		"User Integration",
		filters={"workflow_id": workflow_id},
		fields=["name"]
	)

	if not integrations:
		return {"success": False, "error": "Integration not found"}

	integration_id = integrations[0].name
	integration = frappe.get_doc("User Integration", integration_id)

	# Update integration status
	if status == "success":
		integration.mark_completed()
		log_status = "Success"
	else:
		integration.mark_error(message)
		log_status = "Error"

	# Create log entry
	from lodgeick.lodgeick.doctype.integration_log.integration_log import IntegrationLog
	IntegrationLog.create_log(
		integration_id,
		log_status,
		message,
		execution_time
	)

	return {
		"success": True,
		"message": "Callback processed successfully"
	}
