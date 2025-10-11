"""
Google Cloud API client for automated project and OAuth setup
Handles project creation, API enablement, and OAuth credential generation
"""

import frappe
from frappe import _
import json
import time
from typing import Dict, List, Optional
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class GoogleCloudClient:
    """Client for interacting with Google Cloud APIs"""

    def __init__(self):
        """Initialize Google Cloud client with service account credentials"""
        # Get service account credentials from site config
        service_account_info = frappe.conf.get("google_cloud_service_account")

        if not service_account_info:
            frappe.throw(
                "Google Cloud service account not configured. "
                "Add 'google_cloud_service_account' to site_config.json with service account JSON"
            )

        # Parse if string, otherwise use dict directly
        if isinstance(service_account_info, str):
            try:
                service_account_info = json.loads(service_account_info)
            except json.JSONDecodeError:
                # Try loading from file path
                try:
                    with open(service_account_info, 'r') as f:
                        service_account_info = json.load(f)
                except Exception as e:
                    frappe.throw(f"Failed to load service account credentials: {str(e)}")

        # Create credentials
        self.credentials = service_account.Credentials.from_service_account_info(
            service_account_info,
            scopes=[
                'https://www.googleapis.com/auth/cloud-platform',
                'https://www.googleapis.com/auth/cloudplatformprojects'
            ]
        )

        # Initialize API clients (lazy loaded)
        self._cloudresourcemanager = None
        self._serviceusage = None
        self._iam = None

    @property
    def cloudresourcemanager(self):
        """Lazy load Cloud Resource Manager API client"""
        if not self._cloudresourcemanager:
            self._cloudresourcemanager = build(
                'cloudresourcemanager',
                'v1',
                credentials=self.credentials
            )
        return self._cloudresourcemanager

    @property
    def serviceusage(self):
        """Lazy load Service Usage API client"""
        if not self._serviceusage:
            self._serviceusage = build(
                'serviceusage',
                'v1',
                credentials=self.credentials
            )
        return self._serviceusage

    @property
    def iam(self):
        """Lazy load IAM API client"""
        if not self._iam:
            self._iam = build(
                'iam',
                'v1',
                credentials=self.credentials
            )
        return self._iam

    def create_project(self, project_id: str, project_name: str, parent_org: Optional[str] = None) -> Dict:
        """
        Create a new Google Cloud project

        Args:
            project_id: Unique project ID (lowercase, hyphens allowed)
            project_name: Display name for the project
            parent_org: Optional parent organization ID

        Returns:
            Created project details
        """
        try:
            project_body = {
                'projectId': project_id,
                'name': project_name
            }

            if parent_org:
                project_body['parent'] = {
                    'type': 'organization',
                    'id': parent_org
                }

            request = self.cloudresourcemanager.projects().create(body=project_body)
            operation = request.execute()

            # Wait for operation to complete
            project = self._wait_for_operation(operation)

            frappe.logger().info(f"Created Google Cloud project: {project_id}")
            return project

        except HttpError as e:
            error_detail = json.loads(e.content.decode('utf-8'))
            error_msg = error_detail.get('error', {}).get('message', str(e))
            frappe.log_error(f"Failed to create project {project_id}: {error_msg}", "Google Cloud API Error")
            frappe.throw(_(f"Failed to create Google Cloud project: {error_msg}"))

    def enable_apis(self, project_id: str, api_names: List[str]) -> Dict:
        """
        Enable multiple APIs on a Google Cloud project

        Args:
            project_id: Project ID where APIs should be enabled
            api_names: List of API names (e.g., ['gmail.googleapis.com', 'drive.googleapis.com'])

        Returns:
            Status of API enablement
        """
        enabled_apis = []
        failed_apis = []

        for api_name in api_names:
            try:
                service_name = f"projects/{project_id}/services/{api_name}"

                # Check if already enabled
                try:
                    service = self.serviceusage.services().get(name=service_name).execute()
                    if service.get('state') == 'ENABLED':
                        frappe.logger().info(f"API {api_name} already enabled on {project_id}")
                        enabled_apis.append(api_name)
                        continue
                except HttpError:
                    pass  # API not enabled yet, continue to enable it

                # Enable the API
                request = self.serviceusage.services().enable(name=service_name, body={})
                operation = request.execute()

                # Service enablement is usually fast, but wait briefly
                time.sleep(2)

                enabled_apis.append(api_name)
                frappe.logger().info(f"Enabled API {api_name} on project {project_id}")

            except HttpError as e:
                error_detail = json.loads(e.content.decode('utf-8'))
                error_msg = error_detail.get('error', {}).get('message', str(e))
                failed_apis.append({'api': api_name, 'error': error_msg})
                frappe.log_error(
                    f"Failed to enable {api_name} on {project_id}: {error_msg}",
                    "Google Cloud API Error"
                )

        return {
            'enabled': enabled_apis,
            'failed': failed_apis,
            'success': len(failed_apis) == 0
        }

    def create_oauth_client(
        self,
        project_id: str,
        client_name: str,
        redirect_uris: List[str],
        app_name: str = "Lodgeick"
    ) -> Dict:
        """
        Create OAuth 2.0 client credentials

        Note: This requires manual OAuth consent screen setup first.
        The full automation of OAuth client creation via API is limited.

        Args:
            project_id: Google Cloud project ID
            client_name: Name for the OAuth client
            redirect_uris: List of authorized redirect URIs
            app_name: Application name for consent screen

        Returns:
            OAuth client credentials
        """
        # Note: Full OAuth client creation via API requires OAuth consent screen
        # to be configured manually first. This is a Google Cloud limitation.
        #
        # For now, we'll return instructions for manual setup.
        # Future enhancement: Use internal Google APIs if service account has proper permissions.

        frappe.throw(_(
            "OAuth client creation requires manual setup in Google Cloud Console. "
            "Please follow the OAuth Setup Wizard to create credentials manually."
        ))

    def check_billing_enabled(self, project_id: str) -> bool:
        """
        Check if billing is enabled for a project

        Args:
            project_id: Google Cloud project ID

        Returns:
            True if billing is enabled
        """
        try:
            # This requires Cloud Billing API to be enabled
            billing_service = build('cloudbilling', 'v1', credentials=self.credentials)
            project_name = f"projects/{project_id}"
            billing_info = billing_service.projects().getBillingInfo(name=project_name).execute()

            return billing_info.get('billingEnabled', False)

        except HttpError as e:
            frappe.log_error(f"Failed to check billing status for {project_id}: {str(e)}")
            return False

    def _wait_for_operation(self, operation: Dict, timeout: int = 60) -> Dict:
        """
        Wait for a long-running operation to complete

        Args:
            operation: Operation object from Google Cloud API
            timeout: Maximum seconds to wait

        Returns:
            Operation result
        """
        start_time = time.time()

        while time.time() - start_time < timeout:
            if operation.get('done'):
                if 'error' in operation:
                    error = operation['error']
                    raise Exception(f"Operation failed: {error.get('message', error)}")
                return operation.get('response', operation)

            time.sleep(2)

            # Get operation status (if operation has a name)
            if 'name' in operation:
                try:
                    op_request = self.cloudresourcemanager.operations().get(name=operation['name'])
                    operation = op_request.execute()
                except HttpError:
                    # Some operations don't support status checking
                    break

        # If we've waited long enough, return what we have
        return operation.get('response', operation)


def get_google_cloud_client() -> GoogleCloudClient:
    """
    Get singleton instance of Google Cloud client

    Returns:
        GoogleCloudClient instance
    """
    if not hasattr(frappe.local, "google_cloud_client"):
        frappe.local.google_cloud_client = GoogleCloudClient()
    return frappe.local.google_cloud_client


@frappe.whitelist()
def test_google_cloud_connection():
    """
    Test endpoint to verify Google Cloud API access

    Returns:
        Connection status
    """
    try:
        client = get_google_cloud_client()
        # Try to list projects to verify credentials work
        projects = client.cloudresourcemanager.projects().list().execute()

        return {
            'success': True,
            'message': 'Successfully connected to Google Cloud APIs',
            'project_count': len(projects.get('projects', []))
        }

    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }
