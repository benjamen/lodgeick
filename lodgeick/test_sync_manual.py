#!/usr/bin/env python
"""Manual test to debug n8n sync"""

import frappe
from lodgeick.services.n8n_sync import get_n8n_sync_service
from lodgeick.services.n8n_client import get_n8n_client


def test_sync():
	"""Test manual sync"""
	print("="*70)
	print("MANUAL SYNC TEST")
	print("="*70)

	# Get the test integration
	integration = frappe.get_doc("User Integration", "88bltpkada")
	print(f"\nIntegration: {integration.flow_name}")
	print(f"Source: {integration.source_app}")
	print(f"Target: {integration.target_app}")
	print(f"Current workflow_id: {integration.workflow_id}")

	# Test n8n connection
	print("\n1. Testing n8n connection...")
	try:
		client = get_n8n_client()
		workflows = client.list_workflows()
		print(f"✅ Connected to n8n - {len(workflows)} workflows found")
	except Exception as e:
		print(f"❌ Connection failed: {str(e)}")
		return

	# Try to manually sync
	print("\n2. Manually triggering sync_integration_create...")
	try:
		sync_service = get_n8n_sync_service()
		workflow_id = sync_service.sync_integration_create(integration)
		print(f"✅ Success! Workflow ID: {workflow_id}")

		# Reload and verify
		integration.reload()
		print(f"✅ Updated workflow_id in doc: {integration.workflow_id}")

		# Verify in n8n
		workflow = client.get_workflow(workflow_id)
		print(f"✅ Verified in n8n: {workflow.get('name')}")
		print(f"   Active: {workflow.get('active')}")
		print(f"   Nodes: {len(workflow.get('nodes', []))}")

	except Exception as e:
		print(f"❌ Error: {str(e)}")
		import traceback
		traceback.print_exc()

		# Check error logs
		print("\n3. Checking error logs...")
		errors = frappe.get_all("Error Log",
			fields=["name", "error"],
			order_by="creation desc",
			limit=1
		)
		if errors:
			print(f"Latest error log: {errors[0].name}")
			print(errors[0].error[:1000])

	print("\n" + "="*70)
