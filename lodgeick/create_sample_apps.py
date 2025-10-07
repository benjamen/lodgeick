#!/usr/bin/env python3
import frappe
from frappe.installer import install_app

def create_sample_apps():
    frappe.init(site='lodgeick.com')
    frappe.connect()

    apps_data = [
        {
            "app_name": "xero",
            "display_name": "Xero",
            "description": "Cloud accounting software for small businesses",
            "category": "Accounting",
            "oauth_provider": "xero",
            "is_active": 1,
            "use_cases": [
                {
                    "use_case_name": "Sync invoices to Google Sheets",
                    "description": "Automatically export Xero invoices to a Google Sheet",
                    "workflow_template_id": "xero_to_sheets_001"
                },
                {
                    "use_case_name": "Send invoice reminders via Slack",
                    "description": "Get Slack notifications for overdue invoices",
                    "workflow_template_id": "xero_slack_reminders"
                }
            ]
        },
        {
            "app_name": "google_sheets",
            "display_name": "Google Sheets",
            "description": "Collaborative spreadsheets for the modern workplace",
            "category": "Productivity",
            "oauth_provider": "google",
            "is_active": 1,
            "use_cases": [
                {
                    "use_case_name": "Import contacts to CRM",
                    "description": "Sync Google Sheets data to your CRM system",
                    "workflow_template_id": "sheets_to_crm_001"
                }
            ]
        },
        {
            "app_name": "slack",
            "display_name": "Slack",
            "description": "Team communication and collaboration platform",
            "category": "Communication",
            "oauth_provider": "slack",
            "is_active": 1,
            "use_cases": [
                {
                    "use_case_name": "New deal notifications",
                    "description": "Get Slack alerts when new deals are created",
                    "workflow_template_id": "crm_slack_deals"
                }
            ]
        },
        {
            "app_name": "gmail",
            "display_name": "Gmail",
            "description": "Email service from Google with smart features",
            "category": "Email",
            "oauth_provider": "google",
            "is_active": 1,
            "use_cases": [
                {
                    "use_case_name": "Save attachments to Drive",
                    "description": "Automatically save email attachments to Google Drive",
                    "workflow_template_id": "gmail_drive_attachments"
                }
            ]
        },
        {
            "app_name": "salesforce",
            "display_name": "Salesforce",
            "description": "World's #1 CRM platform for sales and service",
            "category": "CRM",
            "oauth_provider": "salesforce",
            "is_active": 1,
            "use_cases": [
                {
                    "use_case_name": "Sync leads to marketing automation",
                    "description": "Push Salesforce leads to your marketing platform",
                    "workflow_template_id": "sf_marketing_sync"
                }
            ]
        },
        {
            "app_name": "mailchimp",
            "display_name": "Mailchimp",
            "description": "Email marketing and automation platform",
            "category": "Marketing",
            "oauth_provider": "mailchimp",
            "is_active": 1,
            "use_cases": [
                {
                    "use_case_name": "Add CRM contacts to campaigns",
                    "description": "Sync new CRM contacts to Mailchimp campaigns",
                    "workflow_template_id": "crm_mailchimp_sync"
                }
            ]
        }
    ]

    for app_data in apps_data:
        doc = frappe.get_doc({
            "doctype": "App Catalog",
            **app_data
        })
        doc.insert()
        print(f"Created: {doc.display_name}")

    frappe.db.commit()
    print(f"\nSuccessfully created {len(apps_data)} sample apps!")

if __name__ == "__main__":
    create_sample_apps()
