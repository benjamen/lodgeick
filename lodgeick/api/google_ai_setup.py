"""
AI-Powered Google API Setup Assistant
Main orchestration endpoint for automated Google Cloud integration setup
"""

import frappe
from frappe import _
import json
import re
from typing import Dict, Optional
from datetime import datetime


@frappe.whitelist()
def parse_intent(intent: str) -> Dict:
    """
    Parse user's natural language intent to determine required Google APIs

    Args:
        intent: User's description of what they want to integrate

    Returns:
        {
            "success": bool,
            "apis": [{"name": str, "display_name": str, "scopes": [str], "description": str}],
            "billing_required": bool,
            "billing_apis": [str],
            "reasoning": str,
            "next_step": str
        }
    """
    try:
        from lodgeick.services.ai_parser import get_ai_parser

        parser = get_ai_parser()
        result = parser.parse_intent(intent)

        # Determine next step based on billing requirement
        if result.get('billing_required'):
            next_step = "billing_setup"
            message = f"The following APIs require billing to be enabled: {', '.join(result.get('billing_apis', []))}"
        else:
            next_step = "project_setup"
            message = "Ready to create Google Cloud project and enable APIs"

        return {
            "success": True,
            **result,
            "next_step": next_step,
            "message": message
        }

    except Exception as e:
        frappe.log_error(f"Failed to parse intent: {str(e)}", "AI Setup Error")
        return {
            "success": False,
            "error": str(e)
        }


@frappe.whitelist()
def create_project(project_name: str, intent_data: str) -> Dict:
    """
    Create Google Cloud project and enable required APIs

    Args:
        project_name: Desired name for the project
        intent_data: JSON string of parsed intent data from parse_intent

    Returns:
        {
            "success": bool,
            "project_id": str,
            "project_name": str,
            "apis_enabled": [str],
            "apis_failed": [dict],
            "next_step": str
        }
    """
    try:
        # Parse intent data
        if isinstance(intent_data, str):
            intent_data = json.loads(intent_data)

        # Generate project ID from name (must be lowercase, hyphens only)
        base_project_id = re.sub(r'[^a-z0-9-]', '-', project_name.lower())
        base_project_id = re.sub(r'-+', '-', base_project_id).strip('-')

        # Add timestamp to ensure uniqueness
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        project_id = f"{base_project_id}-{timestamp}"[:30]  # GCP project ID max length is 30

        # Get Google Cloud client
        from lodgeick.api.google_cloud import get_google_cloud_client
        client = get_google_cloud_client()

        # Create project
        frappe.logger().info(f"Creating Google Cloud project: {project_id}")
        project = client.create_project(project_id, project_name)

        # Extract API names from intent data
        api_names = [api['name'] for api in intent_data.get('apis', [])]

        # Enable APIs
        frappe.logger().info(f"Enabling APIs: {', '.join(api_names)}")
        enable_result = client.enable_apis(project_id, api_names)

        # Store project info for user
        _store_user_project(project_id, project_name, intent_data, enable_result)

        return {
            "success": True,
            "project_id": project_id,
            "project_name": project_name,
            "apis_enabled": enable_result.get('enabled', []),
            "apis_failed": enable_result.get('failed', []),
            "next_step": "oauth_setup",
            "message": f"Project '{project_name}' created successfully with {len(enable_result.get('enabled', []))} APIs enabled"
        }

    except Exception as e:
        frappe.log_error(f"Failed to create project: {str(e)}", "AI Setup Error")
        return {
            "success": False,
            "error": str(e)
        }


@frappe.whitelist()
def setup_oauth_credentials(project_id: str, client_id: str, client_secret: str) -> Dict:
    """
    Save OAuth credentials and sync with n8n

    Args:
        project_id: Google Cloud project ID
        client_id: OAuth client ID from Google Cloud Console
        client_secret: OAuth client secret

    Returns:
        {
            "success": bool,
            "n8n_credential_id": str,
            "message": str
        }
    """
    try:
        # Save credentials to Frappe
        from lodgeick.api.oauth import save_oauth_credentials

        save_result = save_oauth_credentials(
            provider='google',
            client_id=client_id,
            client_secret=client_secret
        )

        if not save_result.get('success'):
            return save_result

        # Sync with n8n
        n8n_result = _sync_credentials_to_n8n(
            project_id=project_id,
            client_id=client_id,
            client_secret=client_secret
        )

        return {
            "success": True,
            "n8n_credential_id": n8n_result.get('credential_id'),
            "message": "OAuth credentials saved and synced to n8n successfully",
            "next_step": "complete"
        }

    except Exception as e:
        frappe.log_error(f"Failed to setup OAuth credentials: {str(e)}", "AI Setup Error")
        return {
            "success": False,
            "error": str(e)
        }


@frappe.whitelist()
def get_setup_status(project_id: str) -> Dict:
    """
    Get current setup status for a project

    Args:
        project_id: Google Cloud project ID

    Returns:
        Project setup status
    """
    try:
        user = frappe.session.user

        # Get stored project info
        project_doc = frappe.get_doc("User Google Project", {
            "user": user,
            "project_id": project_id
        })

        return {
            "success": True,
            "project": {
                "id": project_doc.project_id,
                "name": project_doc.project_name,
                "status": project_doc.status,
                "apis_enabled": json.loads(project_doc.apis_enabled or "[]"),
                "created_at": project_doc.creation,
                "has_oauth": bool(project_doc.oauth_client_id)
            }
        }

    except frappe.DoesNotExistError:
        return {
            "success": False,
            "error": "Project not found"
        }
    except Exception as e:
        frappe.log_error(f"Failed to get setup status: {str(e)}", "AI Setup Error")
        return {
            "success": False,
            "error": str(e)
        }


def _store_user_project(project_id: str, project_name: str, intent_data: Dict, enable_result: Dict):
    """Store user's Google Cloud project information"""
    user = frappe.session.user

    # Check if project already exists
    if frappe.db.exists("User Google Project", {"user": user, "project_id": project_id}):
        doc = frappe.get_doc("User Google Project", {"user": user, "project_id": project_id})
    else:
        doc = frappe.new_doc("User Google Project")
        doc.user = user
        doc.project_id = project_id

    doc.project_name = project_name
    doc.status = "APIs Enabled"
    doc.intent = json.dumps(intent_data)
    doc.apis_enabled = json.dumps(enable_result.get('enabled', []))
    doc.apis_failed = json.dumps(enable_result.get('failed', []))

    doc.save(ignore_permissions=True)
    frappe.db.commit()


def _sync_credentials_to_n8n(project_id: str, client_id: str, client_secret: str) -> Dict:
    """Sync OAuth credentials to n8n"""
    try:
        from lodgeick.services.n8n_client import get_n8n_client

        client = get_n8n_client()
        user = frappe.session.user

        # Get redirect URI
        site_url = frappe.utils.get_url()
        redirect_uri = f"{site_url}/api/method/lodgeick.api.oauth.oauth_callback"

        # Create credential in n8n
        credential_data = {
            "name": f"Google OAuth - {user} - {project_id}",
            "type": "googleOAuth2Api",
            "data": {
                "clientId": client_id,
                "clientSecret": client_secret,
                "authUrl": "https://accounts.google.com/o/oauth2/v2/auth",
                "accessTokenUrl": "https://oauth2.googleapis.com/token",
                "redirectUri": redirect_uri
            }
        }

        result = client.create_credential(credential_data)

        # Update stored project with n8n credential ID
        project_doc = frappe.get_doc("User Google Project", {
            "user": user,
            "project_id": project_id
        })
        project_doc.oauth_client_id = client_id
        project_doc.n8n_credential_id = result.get('id')
        project_doc.status = "Complete"
        project_doc.save(ignore_permissions=True)
        frappe.db.commit()

        return {
            "success": True,
            "credential_id": result.get('id')
        }

    except Exception as e:
        frappe.log_error(f"Failed to sync credentials to n8n: {str(e)}", "N8N Sync Error")
        # Don't fail the whole setup if n8n sync fails
        return {
            "success": False,
            "error": str(e),
            "credential_id": None
        }


@frappe.whitelist()
def list_user_projects() -> Dict:
    """
    List all Google Cloud projects created by current user

    Returns:
        List of projects with their status
    """
    try:
        user = frappe.session.user

        projects = frappe.get_all(
            "User Google Project",
            fields=["project_id", "project_name", "status", "creation", "apis_enabled"],
            filters={"user": user},
            order_by="creation desc"
        )

        # Parse APIs enabled
        for project in projects:
            try:
                project['apis_enabled'] = json.loads(project.get('apis_enabled', '[]'))
            except:
                project['apis_enabled'] = []

        return {
            "success": True,
            "projects": projects
        }

    except Exception as e:
        frappe.log_error(f"Failed to list projects: {str(e)}", "AI Setup Error")
        return {
            "success": False,
            "error": str(e)
        }
