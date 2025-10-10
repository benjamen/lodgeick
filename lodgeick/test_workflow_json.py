#!/usr/bin/env python
"""Test to inspect the workflow JSON being sent to n8n"""

import frappe
import json
from lodgeick.services.n8n_sync import get_n8n_sync_service


def test_workflow_json():
	"""Test workflow JSON generation"""
	print("="*70)
	print("WORKFLOW JSON INSPECTION")
	print("="*70)

	# Get the test integration
	integration = frappe.get_doc("User Integration", "88bltpkada")
	print(f"\nIntegration: {integration.flow_name}")
	print(f"Source: {integration.source_app}")
	print(f"Target: {integration.target_app}")
	print(f"Config: {integration.config}")

	# Build the workflow JSON
	sync_service = get_n8n_sync_service()
	workflow_data = sync_service._build_workflow_json(integration)

	print("\n" + "="*70)
	print("GENERATED WORKFLOW JSON:")
	print("="*70)
	print(json.dumps(workflow_data, indent=2))

	print("\n" + "="*70)
	print("VALIDATION:")
	print("="*70)
	print(f"✓ Name: {workflow_data.get('name')}")
	print(f"✓ Nodes: {len(workflow_data.get('nodes', []))}")
	print(f"✓ Active: {workflow_data.get('active')}")
	print(f"✓ Connections: {len(workflow_data.get('connections', {}))} nodes connected")

	print("\nNode details:")
	for i, node in enumerate(workflow_data.get('nodes', []), 1):
		print(f"  {i}. {node.get('name')} ({node.get('type')})")
		print(f"     Position: {node.get('position')}")
		print(f"     Parameters: {json.dumps(node.get('parameters', {}), indent=6)}")

	print("="*70)
