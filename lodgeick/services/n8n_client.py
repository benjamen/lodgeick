"""
N8N API Client for Lodgeick
Manages workflows and credentials in n8n automation platform
"""

import frappe
import requests
import json
from typing import Dict, List, Optional, Any
from frappe import _


class N8NClient:
	"""Client for interacting with n8n REST API"""

	def __init__(self):
		"""Initialize n8n client with configuration from site config"""
		self.base_url = frappe.conf.get("n8n_base_url", "http://localhost:5678")
		self.api_key = frappe.conf.get("n8n_api_key")

		if not self.api_key:
			frappe.log_error("n8n API key not configured in site config", "N8N Client Error")

		self.headers = {
			"X-N8N-API-KEY": self.api_key,
			"Content-Type": "application/json",
			"Accept": "application/json"
		}

	def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict:
		"""
		Make HTTP request to n8n API

		Args:
			method: HTTP method (GET, POST, PUT, DELETE)
			endpoint: API endpoint (e.g., '/workflows')
			data: Request payload

		Returns:
			Response data as dictionary

		Raises:
			Exception: If request fails
		"""
		url = f"{self.base_url}/api/v1{endpoint}"

		try:
			if method == "GET":
				response = requests.get(url, headers=self.headers, timeout=30)
			elif method == "POST":
				response = requests.post(url, headers=self.headers, json=data, timeout=30)
			elif method == "PUT":
				response = requests.put(url, headers=self.headers, json=data, timeout=30)
			elif method == "DELETE":
				response = requests.delete(url, headers=self.headers, timeout=30)
			else:
				raise ValueError(f"Unsupported HTTP method: {method}")

			response.raise_for_status()

			# n8n returns empty body for DELETE
			if method == "DELETE":
				return {"success": True}

			return response.json()

		except requests.exceptions.RequestException as e:
			error_msg = f"n8n API request failed: {str(e)}"
			# Try to get response body for more details
			if hasattr(e, 'response') and e.response is not None:
				try:
					error_detail = e.response.json()
					error_msg += f"\nResponse: {json.dumps(error_detail, indent=2)}"
				except:
					error_msg += f"\nResponse text: {e.response.text[:500]}"
			frappe.log_error(error_msg, "N8N API Error")
			raise Exception(error_msg)

	# ==================== Workflow Methods ====================

	def create_workflow(self, workflow_data: Dict) -> Dict:
		"""
		Create a new workflow in n8n

		Args:
			workflow_data: Workflow configuration

		Returns:
			Created workflow data with ID
		"""
		return self._make_request("POST", "/workflows", workflow_data)

	def get_workflow(self, workflow_id: str) -> Dict:
		"""
		Get workflow details by ID

		Args:
			workflow_id: n8n workflow ID

		Returns:
			Workflow data
		"""
		return self._make_request("GET", f"/workflows/{workflow_id}")

	def update_workflow(self, workflow_id: str, workflow_data: Dict) -> Dict:
		"""
		Update existing workflow

		Args:
			workflow_id: n8n workflow ID
			workflow_data: Updated workflow configuration

		Returns:
			Updated workflow data
		"""
		return self._make_request("PUT", f"/workflows/{workflow_id}", workflow_data)

	def delete_workflow(self, workflow_id: str) -> Dict:
		"""
		Delete workflow from n8n

		Args:
			workflow_id: n8n workflow ID

		Returns:
			Success status
		"""
		return self._make_request("DELETE", f"/workflows/{workflow_id}")

	def activate_workflow(self, workflow_id: str) -> Dict:
		"""
		Activate a workflow

		Args:
			workflow_id: n8n workflow ID

		Returns:
			Updated workflow data
		"""
		workflow = self.get_workflow(workflow_id)
		workflow["active"] = True
		return self.update_workflow(workflow_id, workflow)

	def deactivate_workflow(self, workflow_id: str) -> Dict:
		"""
		Deactivate a workflow

		Args:
			workflow_id: n8n workflow ID

		Returns:
			Updated workflow data
		"""
		workflow = self.get_workflow(workflow_id)
		workflow["active"] = False
		return self.update_workflow(workflow_id, workflow)

	def list_workflows(self) -> List[Dict]:
		"""
		List all workflows

		Returns:
			List of workflows
		"""
		response = self._make_request("GET", "/workflows")
		return response.get("data", [])

	# ==================== Credential Methods ====================

	def create_credential(self, credential_data: Dict) -> Dict:
		"""
		Create a new credential in n8n

		Args:
			credential_data: Credential configuration

		Returns:
			Created credential data with ID
		"""
		return self._make_request("POST", "/credentials", credential_data)

	def get_credential(self, credential_id: str) -> Dict:
		"""
		Get credential details by ID

		Args:
			credential_id: n8n credential ID

		Returns:
			Credential data
		"""
		return self._make_request("GET", f"/credentials/{credential_id}")

	def update_credential(self, credential_id: str, credential_data: Dict) -> Dict:
		"""
		Update existing credential

		Args:
			credential_id: n8n credential ID
			credential_data: Updated credential configuration

		Returns:
			Updated credential data
		"""
		return self._make_request("PUT", f"/credentials/{credential_id}", credential_data)

	def delete_credential(self, credential_id: str) -> Dict:
		"""
		Delete credential from n8n

		Args:
			credential_id: n8n credential ID

		Returns:
			Success status
		"""
		return self._make_request("DELETE", f"/credentials/{credential_id}")

	def list_credentials(self) -> List[Dict]:
		"""
		List all credentials

		Returns:
			List of credentials
		"""
		response = self._make_request("GET", "/credentials")
		return response.get("data", [])

	# ==================== Execution Methods ====================

	def execute_workflow(self, workflow_id: str, data: Optional[Dict] = None) -> Dict:
		"""
		Execute a workflow manually

		Args:
			workflow_id: n8n workflow ID
			data: Optional input data for workflow

		Returns:
			Execution result
		"""
		endpoint = f"/workflows/{workflow_id}/execute"
		return self._make_request("POST", endpoint, data or {})

	def get_execution(self, execution_id: str) -> Dict:
		"""
		Get execution details

		Args:
			execution_id: n8n execution ID

		Returns:
			Execution data
		"""
		return self._make_request("GET", f"/executions/{execution_id}")

	def list_executions(self, workflow_id: Optional[str] = None) -> List[Dict]:
		"""
		List workflow executions

		Args:
			workflow_id: Optional workflow ID to filter by

		Returns:
			List of executions
		"""
		endpoint = "/executions"
		if workflow_id:
			endpoint += f"?workflowId={workflow_id}"
		response = self._make_request("GET", endpoint)
		return response.get("data", [])


def get_n8n_client() -> N8NClient:
	"""
	Get singleton instance of N8N client

	Returns:
		N8NClient instance
	"""
	if not hasattr(frappe.local, "n8n_client"):
		frappe.local.n8n_client = N8NClient()
	return frappe.local.n8n_client
