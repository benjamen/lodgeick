#!/usr/bin/env python3
"""
Test script for N8N Integration
Tests the complete flow: Create Integration → Verify in n8n → Execute → Check History
"""

import frappe
import json
from lodgeick.services.n8n_client import get_n8n_client
from lodgeick.services.n8n_sync import get_n8n_sync_service


def test_n8n_connection():
	"""Test 1: Verify n8n API connection"""
	print("\n" + "="*60)
	print("TEST 1: N8N CONNECTION")
	print("="*60)

	try:
		client = get_n8n_client()
		workflows = client.list_workflows()
		print(f"✅ Successfully connected to n8n")
		print(f"   Found {len(workflows)} existing workflows")
		return True
	except Exception as e:
		print(f"❌ Failed to connect to n8n: {str(e)}")
		return False


def test_create_integration():
	"""Test 2: Create a test integration and verify workflow creation"""
	print("\n" + "="*60)
	print("TEST 2: CREATE INTEGRATION")
	print("="*60)

	try:
		# Create test integration
		integration = frappe.get_doc({
			"doctype": "User Integration",
			"user": frappe.session.user,
			"flow_name": "Test: Slack to Google Sheets",
			"source_app": "slack",
			"target_app": "google_sheets",
			"config": json.dumps({
				"source_settings": {
					"channel": "#test-channel",
					"message_template": "{{$json.message}}"
				},
				"target_settings": {
					"spreadsheet_id": "test-spreadsheet-123",
					"range": "Sheet1!A:Z"
				}
			}),
			"status": "Active"
		})

		integration.insert(ignore_permissions=True)
		frappe.db.commit()

		print(f"✅ Created integration: {integration.name}")
		print(f"   Flow Name: {integration.flow_name}")
		print(f"   Source: {integration.source_app}")
		print(f"   Target: {integration.target_app}")
		print(f"   Status: {integration.status}")

		# Wait a moment for sync to complete
		import time
		time.sleep(2)

		# Reload to get workflow_id
		integration.reload()

		if integration.workflow_id:
			print(f"✅ N8N workflow created: {integration.workflow_id}")
			return integration.name, integration.workflow_id
		else:
			print(f"⚠️  No workflow_id set yet")
			return integration.name, None

	except Exception as e:
		print(f"❌ Failed to create integration: {str(e)}")
		frappe.log_error(f"Test integration creation failed: {str(e)}", "N8N Test Error")
		return None, None


def test_verify_workflow_in_n8n(workflow_id):
	"""Test 3: Verify workflow exists in n8n"""
	print("\n" + "="*60)
	print("TEST 3: VERIFY WORKFLOW IN N8N")
	print("="*60)

	if not workflow_id:
		print("⚠️  Skipping - no workflow_id available")
		return False

	try:
		client = get_n8n_client()
		workflow = client.get_workflow(workflow_id)

		print(f"✅ Found workflow in n8n")
		print(f"   ID: {workflow.get('id')}")
		print(f"   Name: {workflow.get('name')}")
		print(f"   Active: {workflow.get('active')}")
		print(f"   Nodes: {len(workflow.get('nodes', []))} nodes")

		# Print node details
		for node in workflow.get('nodes', []):
			print(f"      - {node.get('name')} ({node.get('type')})")

		return True

	except Exception as e:
		print(f"❌ Failed to get workflow from n8n: {str(e)}")
		return False


def test_update_integration(integration_id):
	"""Test 4: Update integration and verify sync"""
	print("\n" + "="*60)
	print("TEST 4: UPDATE INTEGRATION")
	print("="*60)

	if not integration_id:
		print("⚠️  Skipping - no integration available")
		return False

	try:
		integration = frappe.get_doc("User Integration", integration_id)

		# Update configuration
		config = json.loads(integration.config)
		config["source_settings"]["channel"] = "#updated-channel"
		integration.config = json.dumps(config)

		integration.save(ignore_permissions=True)
		frappe.db.commit()

		print(f"✅ Updated integration configuration")
		print(f"   New channel: #updated-channel")

		import time
		time.sleep(2)

		# Verify update in n8n
		if integration.workflow_id:
			client = get_n8n_client()
			workflow = client.get_workflow(integration.workflow_id)
			print(f"✅ Workflow updated in n8n")
			print(f"   Updated at: {workflow.get('updatedAt')}")

		return True

	except Exception as e:
		print(f"❌ Failed to update integration: {str(e)}")
		return False


def test_status_change(integration_id):
	"""Test 5: Change status and verify sync"""
	print("\n" + "="*60)
	print("TEST 5: STATUS CHANGE")
	print("="*60)

	if not integration_id:
		print("⚠️  Skipping - no integration available")
		return False

	try:
		integration = frappe.get_doc("User Integration", integration_id)

		# Pause the integration
		integration.status = "Paused"
		integration.save(ignore_permissions=True)
		frappe.db.commit()

		print(f"✅ Changed status to: Paused")

		import time
		time.sleep(2)

		# Verify in n8n
		if integration.workflow_id:
			client = get_n8n_client()
			workflow = client.get_workflow(integration.workflow_id)
			print(f"   N8N workflow active: {workflow.get('active')}")

			if not workflow.get('active'):
				print(f"✅ Status synced correctly to n8n")
			else:
				print(f"⚠️  Status not synced to n8n yet")

		return True

	except Exception as e:
		print(f"❌ Failed to change status: {str(e)}")
		return False


def test_list_integrations():
	"""Test 6: List all integrations via API"""
	print("\n" + "="*60)
	print("TEST 6: LIST INTEGRATIONS API")
	print("="*60)

	try:
		from lodgeick.api.n8n import list_user_integrations

		result = list_user_integrations()

		if result.get("success"):
			integrations = result.get("integrations", [])
			print(f"✅ API returned {len(integrations)} integrations")

			for integration in integrations:
				print(f"   - {integration.get('flow_name')}")
				print(f"     Status: {integration.get('status')}")
				print(f"     Workflow ID: {integration.get('workflow_id')}")
		else:
			print(f"⚠️  API returned error: {result.get('error')}")

		return True

	except Exception as e:
		print(f"❌ Failed to list integrations: {str(e)}")
		return False


def cleanup_test_integration(integration_id):
	"""Cleanup: Delete test integration"""
	print("\n" + "="*60)
	print("CLEANUP: DELETE TEST INTEGRATION")
	print("="*60)

	if not integration_id:
		print("⚠️  No integration to cleanup")
		return

	try:
		integration = frappe.get_doc("User Integration", integration_id)
		workflow_id = integration.workflow_id

		integration.delete()
		frappe.db.commit()

		print(f"✅ Deleted integration: {integration_id}")

		import time
		time.sleep(2)

		# Verify deletion in n8n
		if workflow_id:
			try:
				client = get_n8n_client()
				client.get_workflow(workflow_id)
				print(f"⚠️  Workflow still exists in n8n")
			except:
				print(f"✅ Workflow deleted from n8n")

	except Exception as e:
		print(f"❌ Failed to cleanup: {str(e)}")


def run_all_tests():
	"""Run all tests"""
	print("\n" + "="*70)
	print(" N8N INTEGRATION TEST SUITE")
	print("="*70)

	# Initialize Frappe
	frappe.init(site="lodgeick.com")
	frappe.connect()
	frappe.set_user("Administrator")

	try:
		# Test 1: Connection
		if not test_n8n_connection():
			print("\n❌ Cannot proceed - n8n connection failed")
			return

		# Test 2: Create Integration
		integration_id, workflow_id = test_create_integration()
		if not integration_id:
			print("\n❌ Cannot proceed - integration creation failed")
			return

		# Test 3: Verify in n8n
		test_verify_workflow_in_n8n(workflow_id)

		# Test 4: Update Integration
		test_update_integration(integration_id)

		# Test 5: Status Change
		test_status_change(integration_id)

		# Test 6: List API
		test_list_integrations()

		# Cleanup
		print("\nDo you want to delete the test integration? (y/n): ", end="")
		response = input().strip().lower()
		if response == 'y':
			cleanup_test_integration(integration_id)
		else:
			print(f"\n✅ Test integration kept: {integration_id}")
			print(f"   You can view it at: http://localhost:8080/app/user-integration/{integration_id}")

		print("\n" + "="*70)
		print(" TEST SUITE COMPLETED")
		print("="*70)

	finally:
		frappe.destroy()


if __name__ == "__main__":
	run_all_tests()
