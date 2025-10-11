import frappe
from lodgeick.services.n8n_client import get_n8n_client

def check():
	client = get_n8n_client()
	workflows = client.list_workflows()
	lodgeick_workflows = [w for w in workflows if 'Lodgeick' in w.get('name', '')]

	print(f'Total n8n workflows: {len(workflows)}')
	print(f'Lodgeick workflows: {len(lodgeick_workflows)}')
	for w in lodgeick_workflows:
		print(f"  - {w.get('name')} (ID: {w.get('id')}, Active: {w.get('active')})")
