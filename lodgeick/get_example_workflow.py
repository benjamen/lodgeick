#!/usr/bin/env python
"""Get an example workflow from n8n to see the correct format"""

import frappe
import json
from lodgeick.services.n8n_client import get_n8n_client


def get_example():
	"""Get example workflow"""
	client = get_n8n_client()
	workflows = client.list_workflows()

	if workflows:
		# Get the first workflow as an example
		workflow_id = workflows[0].get("id")
		print(f"Fetching example workflow: {workflows[0].get('name')} (ID: {workflow_id})")

		workflow = client.get_workflow(workflow_id)

		print("\n" + "="*70)
		print("EXAMPLE WORKFLOW STRUCTURE:")
		print("="*70)
		print(json.dumps(workflow, indent=2))

		print("\n" + "="*70)
		print("KEY FIELDS:")
		print("="*70)
		print(f"• name: {workflow.get('name')}")
		print(f"• active: {workflow.get('active')}")
		print(f"• nodes count: {len(workflow.get('nodes', []))}")
		print(f"• settings: {json.dumps(workflow.get('settings', {}), indent=2)}")
		print(f"• staticData: {workflow.get('staticData')}")
		print(f"• tags: {workflow.get('tags')}")
	else:
		print("No workflows found")
