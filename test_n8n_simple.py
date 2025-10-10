"""
Simple N8N Integration Test
Run with: bench --site lodgeick.com console < test_n8n_simple.py
"""

import frappe
import json
from lodgeick.services.n8n_client import get_n8n_client
from lodgeick.services.n8n_sync import get_n8n_sync_service

print("\n" + "="*70)
print(" N8N INTEGRATION TEST")
print("="*70)

# Test 1: Connection
print("\n[1/6] Testing n8n connection...")
try:
	client = get_n8n_client()
	workflows = client.list_workflows()
	print(f"✅ Connected to n8n successfully")
	print(f"   Found {len(workflows)} existing workflows")
except Exception as e:
	print(f"❌ Connection failed: {str(e)}")
	exit()

# Test 2: Create Integration
print("\n[2/6] Creating test integration...")
try:
	integration = frappe.get_doc({
		"doctype": "User Integration",
		"user": "Administrator",
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

	print(f"✅ Integration created: {integration.name}")
	print(f"   Flow: {integration.flow_name}")
	print(f"   Workflow ID: {integration.workflow_id}")

	test_integration_id = integration.name
	test_workflow_id = integration.workflow_id

except Exception as e:
	print(f"❌ Creation failed: {str(e)}")
	frappe.log_error(f"Test failed: {str(e)}", "N8N Test")
	exit()

# Test 3: Verify in n8n
print("\n[3/6] Verifying workflow in n8n...")
if test_workflow_id:
	try:
		workflow = client.get_workflow(test_workflow_id)
		print(f"✅ Workflow found in n8n")
		print(f"   Name: {workflow.get('name')}")
		print(f"   Active: {workflow.get('active')}")
		print(f"   Nodes: {len(workflow.get('nodes', []))}")
		for node in workflow.get('nodes', []):
			print(f"      • {node.get('name')} ({node.get('type')})")
	except Exception as e:
		print(f"❌ Verification failed: {str(e)}")
else:
	print("⚠️  No workflow_id to verify")

# Test 4: Update Integration
print("\n[4/6] Updating integration...")
try:
	integration = frappe.get_doc("User Integration", test_integration_id)
	config = json.loads(integration.config)
	config["source_settings"]["channel"] = "#updated-channel"
	integration.config = json.dumps(config)
	integration.save(ignore_permissions=True)
	frappe.db.commit()

	print(f"✅ Integration updated")
	print(f"   New channel: #updated-channel")
except Exception as e:
	print(f"❌ Update failed: {str(e)}")

# Test 5: Status Change
print("\n[5/6] Testing status change...")
try:
	integration = frappe.get_doc("User Integration", test_integration_id)
	integration.status = "Paused"
	integration.save(ignore_permissions=True)
	frappe.db.commit()

	print(f"✅ Status changed to: Paused")

	# Verify in n8n
	workflow = client.get_workflow(test_workflow_id)
	print(f"   N8N workflow active: {workflow.get('active')}")

except Exception as e:
	print(f"❌ Status change failed: {str(e)}")

# Test 6: List via API
print("\n[6/6] Testing list API...")
try:
	from lodgeick.api.n8n import list_user_integrations
	result = list_user_integrations()

	if result.get("success"):
		integrations = result.get("integrations", [])
		print(f"✅ API returned {len(integrations)} integrations")
		for i in integrations[-3:]:  # Show last 3
			print(f"   • {i.get('flow_name')} - {i.get('status')}")
	else:
		print(f"⚠️  API error: {result.get('error')}")
except Exception as e:
	print(f"❌ List API failed: {str(e)}")

print("\n" + "="*70)
print(" TEST RESULTS")
print("="*70)
print(f"Test integration ID: {test_integration_id}")
print(f"Test workflow ID: {test_workflow_id}")
print(f"\nView integration: http://localhost:8080/app/user-integration/{test_integration_id}")
print(f"View in n8n: https://flow.optified.nz/workflow/{test_workflow_id}")
print("\nTo delete test integration, run:")
print(f'frappe.delete_doc("User Integration", "{test_integration_id}", force=True)')
print("="*70)
