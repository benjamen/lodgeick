"""
Periodic N8N Sync Job
Validates and syncs integrations between Lodgeick and n8n
"""

import frappe
from lodgeick.services.n8n_client import get_n8n_client
from lodgeick.services.n8n_sync import get_n8n_sync_service


def sync_all_integrations():
	"""
	Periodic job to validate and sync all integrations with n8n
	Fixes any mismatches between Lodgeick and n8n
	"""
	if not frappe.conf.get("n8n_auto_sync", True):
		frappe.logger().info("N8N auto-sync is disabled, skipping sync job")
		return

	frappe.logger().info("Starting n8n sync job...")

	try:
		client = get_n8n_client()
		sync_service = get_n8n_sync_service()

		# Get all n8n workflows
		n8n_workflows = client.list_workflows()
		n8n_workflow_ids = {wf.get("id"): wf for wf in n8n_workflows}

		# Get all Lodgeick integrations
		integrations = frappe.get_all(
			"User Integration",
			fields=["name", "workflow_id", "status", "flow_name"],
			filters={"workflow_id": ["!=", ""]}
		)

		synced_count = 0
		created_count = 0
		deleted_count = 0
		error_count = 0

		# Sync Lodgeick integrations to n8n
		for integration in integrations:
			try:
				integration_doc = frappe.get_doc("User Integration", integration.name)

				if integration.workflow_id:
					# Check if workflow exists in n8n
					if integration.workflow_id in n8n_workflow_ids:
						# Workflow exists, verify it's in sync
						n8n_workflow = n8n_workflow_ids[integration.workflow_id]

						# Check if status matches
						n8n_active = n8n_workflow.get("active", False)
						lodgeick_active = integration.status == "Active"

						if n8n_active != lodgeick_active:
							# Sync status
							sync_service.sync_integration_status(integration_doc, integration.status)
							synced_count += 1
							frappe.logger().info(f"Synced status for integration {integration.name}")

						# Remove from dict so we know it's accounted for
						del n8n_workflow_ids[integration.workflow_id]
					else:
						# Workflow doesn't exist in n8n, recreate it
						frappe.logger().warning(f"Workflow {integration.workflow_id} missing in n8n, recreating...")
						sync_service.sync_integration_create(integration_doc)
						created_count += 1
				else:
					# Integration has no workflow, create one
					sync_service.sync_integration_create(integration_doc)
					created_count += 1

			except Exception as e:
				error_count += 1
				frappe.log_error(
					f"Failed to sync integration {integration.name}: {str(e)}",
					"N8N Sync Job Error"
				)

		# Check for orphaned workflows in n8n (workflows that don't have corresponding integrations)
		if n8n_workflow_ids:
			for workflow_id, workflow in n8n_workflow_ids.items():
				workflow_name = workflow.get("name", "")

				# Only delete workflows created by Lodgeick
				if workflow_name.startswith("Lodgeick:"):
					try:
						frappe.logger().warning(f"Found orphaned n8n workflow {workflow_id}, deleting...")
						client.delete_workflow(workflow_id)
						deleted_count += 1
					except Exception as e:
						frappe.log_error(
							f"Failed to delete orphaned workflow {workflow_id}: {str(e)}",
							"N8N Sync Job Error"
						)

		summary = f"N8N sync job completed: {synced_count} synced, {created_count} created, {deleted_count} deleted, {error_count} errors"
		frappe.logger().info(summary)

		return {
			"success": True,
			"synced": synced_count,
			"created": created_count,
			"deleted": deleted_count,
			"errors": error_count
		}

	except Exception as e:
		error_msg = f"N8N sync job failed: {str(e)}"
		frappe.log_error(error_msg, "N8N Sync Job Error")
		return {
			"success": False,
			"error": str(e)
		}


def enqueue_sync_job():
	"""
	Enqueue sync job to run in background
	"""
	frappe.enqueue(
		"lodgeick.tasks.n8n_sync_job.sync_all_integrations",
		queue="default",
		timeout=600,
		is_async=True
	)


# Scheduler hooks (add to hooks.py)
# scheduler_events = {
#     "hourly": [
#         "lodgeick.tasks.n8n_sync_job.sync_all_integrations"
#     ]
# }
