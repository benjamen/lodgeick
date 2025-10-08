#!/usr/bin/env python3
import frappe

frappe.init(site='lodgeick.com')
frappe.connect()

# Create Xero App Catalog entry
xero = frappe.get_doc({
    "doctype": "App Catalog",
    "name": "xero",
    "app_name": "Xero",
    "app_description": "Cloud-based accounting software for small and medium businesses",
    "category": "Accounting",
    "logo_url": "https://www.xero.com/content/dam/xero/pilot-images/logos/xero-logo.svg",
    "oauth_provider": "xero",
    "is_active": 1
})
xero.insert(ignore_if_duplicate=True)

# Add use cases for Xero
xero.append("use_cases", {
    "use_case_name": "Sync invoices to Google Sheets",
    "use_case_description": "Automatically sync Xero invoices to a Google Sheets spreadsheet",
    "workflow_template_id": "xero_sheets_sync"
})
xero.save()

# Create Google Sheets App Catalog entry
sheets = frappe.get_doc({
    "doctype": "App Catalog",
    "name": "google_sheets",
    "app_name": "Google Sheets",
    "app_description": "Cloud-based spreadsheet application",
    "category": "Productivity",
    "logo_url": "https://www.gstatic.com/images/branding/product/2x/sheets_2020q4_48dp.png",
    "oauth_provider": "google",
    "is_active": 1
})
sheets.insert(ignore_if_duplicate=True)

# Create HubSpot App Catalog entry
hubspot = frappe.get_doc({
    "doctype": "App Catalog",
    "name": "hubspot",
    "app_name": "HubSpot",
    "app_description": "CRM and marketing automation platform",
    "category": "CRM",
    "logo_url": "https://a.slack-edge.com/80588/img/services/hubspot_512.png",
    "oauth_provider": "hubspot",
    "is_active": 1
})
hubspot.insert(ignore_if_duplicate=True)

# Add use cases for HubSpot
hubspot.append("use_cases", {
    "use_case_name": "Sync contacts to Google Sheets",
    "use_case_description": "Export HubSpot contacts to Google Sheets for reporting",
    "workflow_template_id": "hubspot_sheets_contacts"
})
hubspot.save()

# Create Slack App Catalog entry
slack = frappe.get_doc({
    "doctype": "App Catalog",
    "name": "slack",
    "app_name": "Slack",
    "app_description": "Team communication and collaboration platform",
    "category": "Communication",
    "logo_url": "https://a.slack-edge.com/80588/marketing/img/icons/icon_slack_hash_colored.png",
    "oauth_provider": "slack",
    "is_active": 1
})
slack.insert(ignore_if_duplicate=True)

# Add use cases for Slack
slack.append("use_cases", {
    "use_case_name": "Send invoice notifications",
    "use_case_description": "Send Slack notifications when new invoices are created in Xero",
    "workflow_template_id": "xero_slack_notifications"
})
slack.save()

frappe.db.commit()
print("✅ Created App Catalog entries for Xero, Google Sheets, HubSpot, and Slack")
print(f"Total apps: {len(frappe.get_all('App Catalog'))}")

frappe.destroy()
