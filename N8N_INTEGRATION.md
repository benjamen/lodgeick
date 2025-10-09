# N8N Integration Documentation

## Overview

Lodgeick automatically synchronizes integrations with n8n to enable powerful automation workflows. When you create, update, or delete an integration in Lodgeick, the changes are automatically reflected in n8n.

## Architecture

```
┌─────────────────┐         ┌──────────────────┐         ┌─────────────┐
│  Lodgeick UI    │────────▶│  Lodgeick API    │────────▶│    n8n      │
│  (Frontend)     │         │  (Python/Frappe) │         │  (Workflows)│
└─────────────────┘         └──────────────────┘         └─────────────┘
                                      │
                                      ▼
                            ┌──────────────────┐
                            │  Integration DB  │
                            │  (User           │
                            │   Integration)   │
                            └──────────────────┘
```

## Configuration

### 1. Site Configuration

Add the following to your `site_config.json`:

```json
{
  "n8n_base_url": "http://localhost:5678",
  "n8n_api_key": "your-n8n-api-key-here",
  "n8n_auto_sync": true
}
```

**Configuration Options:**
- `n8n_base_url`: Base URL of your n8n instance (default: `http://localhost:5678`)
- `n8n_api_key`: n8n API key for authentication (required)
- `n8n_auto_sync`: Enable/disable automatic synchronization (default: `true`)

### 2. Get n8n API Key

1. Log in to your n8n instance
2. Go to **Settings** → **API**
3. Generate a new API key
4. Copy the key and add it to your site configuration

## Features

### Automatic Synchronization

#### Create Integration
When you create an integration in Lodgeick:
1. A new n8n workflow is automatically created
2. Workflow includes:
   - Webhook trigger node
   - Source app node (configured with your settings)
   - Target app node (configured with your settings)
3. Workflow ID is stored in the integration record

#### Update Integration
When you update an integration:
1. The corresponding n8n workflow is updated
2. Node configurations are synced
3. Status changes (Active/Paused) are reflected in n8n

#### Delete Integration
When you delete an integration:
1. The corresponding n8n workflow is deleted
2. All associated data is cleaned up

### Manual Operations

#### Execute Workflow
```python
integration = frappe.get_doc("User Integration", integration_id)
result = integration.execute_workflow({"key": "value"})
```

#### Get Execution History
```python
integration = frappe.get_doc("User Integration", integration_id)
executions = integration.get_execution_history(limit=10)
```

## API Endpoints

### Create Integration
```
POST /api/method/lodgeick.api.n8n.create_integration
```

**Parameters:**
- `flow_name`: Name of the integration
- `source_app`: Source application (e.g., "slack")
- `target_app`: Target application (e.g., "google_sheets")
- `config`: JSON configuration

**Example:**
```javascript
await call('lodgeick.api.n8n.create_integration', {
  flow_name: "Slack to Google Sheets",
  source_app: "slack",
  target_app: "google_sheets",
  config: {
    source_settings: {
      channel: "#general"
    },
    target_settings: {
      spreadsheet_id: "1234567890",
      range: "Sheet1!A:Z"
    }
  }
})
```

### Update Integration
```
POST /api/method/lodgeick.api.n8n.update_integration
```

**Parameters:**
- `integration_id`: Integration document name
- `config`: Updated configuration (optional)
- `status`: Updated status (optional)

### Delete Integration
```
POST /api/method/lodgeick.api.n8n.delete_integration
```

**Parameters:**
- `integration_id`: Integration document name

### Execute Integration
```
POST /api/method/lodgeick.api.n8n.execute_integration
```

**Parameters:**
- `integration_id`: Integration document name
- `input_data`: Input data for workflow (optional)

### Get Integration Status
```
POST /api/method/lodgeick.api.n8n.get_integration_status
```

**Parameters:**
- `integration_id`: Integration document name

### Get Execution History
```
POST /api/method/lodgeick.api.n8n.get_execution_history
```

**Parameters:**
- `integration_id`: Integration document name
- `limit`: Maximum number of executions (default: 10)

### List User Integrations
```
POST /api/method/lodgeick.api.n8n.list_user_integrations
```

**Parameters:**
- `status`: Optional status filter

## Supported Applications

Currently supported app types and their n8n node mappings:

| App Type | n8n Node Type | Parameters |
|----------|---------------|------------|
| Slack | `n8n-nodes-base.slack` | channel, text, attachments |
| Google Sheets | `n8n-nodes-base.googleSheets` | sheetId, range, valueInputOption |
| Gmail | `n8n-nodes-base.gmail` | to, subject, message |
| Jira | `n8n-nodes-base.jira` | project, issueType, summary |
| Hubspot | `n8n-nodes-base.hubspot` | resource, operation |
| Xero | `n8n-nodes-base.xero` | resource, operation |
| Notion | `n8n-nodes-base.notion` | resource, operation |
| Salesforce | `n8n-nodes-base.salesforce` | resource, operation |

## Periodic Sync Job

A background job runs every hour to:
1. Validate all integrations are in sync with n8n
2. Recreate missing workflows
3. Remove orphaned workflows
4. Fix status mismatches

### Manual Trigger
```
POST /api/method/lodgeick.api.n8n.trigger_sync_job
```

### Configure Schedule

Edit `hooks.py`:
```python
scheduler_events = {
    "hourly": [
        "lodgeick.tasks.n8n_sync_job.sync_all_integrations"
    ]
}
```

## Error Handling

### Integration Errors
If n8n synchronization fails:
1. Integration status is set to "Error"
2. Error message is stored in `error_message` field
3. Error is logged to Frappe error log
4. Integration remains usable in Lodgeick

### Graceful Degradation
- If n8n is unavailable, integrations still work in Lodgeick
- Sync will retry on next update or during periodic sync
- No data loss occurs

## Troubleshooting

### Check n8n Connection
```python
from lodgeick.services.n8n_client import get_n8n_client

client = get_n8n_client()
workflows = client.list_workflows()
print(workflows)
```

### View Sync Errors
1. Go to **Error Log** in Frappe
2. Filter by "N8N Sync" errors
3. Review stack trace and error message

### Re-sync Integration
```python
from lodgeick.services.n8n_sync import get_n8n_sync_service

integration = frappe.get_doc("User Integration", integration_id)
sync_service = get_n8n_sync_service()
sync_service.sync_integration_create(integration)
```

### Disable Auto-Sync
Set in `site_config.json`:
```json
{
  "n8n_auto_sync": false
}
```

## Development

### File Structure
```
lodgeick/
├── services/
│   ├── n8n_client.py          # n8n REST API client
│   └── n8n_sync.py             # Integration sync service
├── api/
│   └── n8n.py                  # REST API endpoints
├── tasks/
│   └── n8n_sync_job.py         # Periodic sync job
└── lodgeick/doctype/
    └── user_integration/
        └── user_integration.py  # DocType with hooks
```

### Adding New App Types

1. Add app to `node_type_map` in `n8n_sync.py`:
```python
node_type_map = {
    "your_app": "n8n-nodes-base.yourApp"
}
```

2. Add parameter mapping in `parameter_maps`:
```python
parameter_maps = {
    "your_app": {
        "param1": settings.get("param1"),
        "param2": settings.get("param2")
    }
}
```

## Testing

### Unit Tests
```bash
bench run-tests --app lodgeick --module "lodgeick.services.n8n_client"
bench run-tests --app lodgeick --module "lodgeick.services.n8n_sync"
```

### Integration Tests
```bash
bench run-tests --app lodgeick --module "lodgeick.api.n8n"
```

## Security

- n8n API key is stored in site config (encrypted)
- All API endpoints check user permissions
- Workflows are tagged with user information
- Each user's integrations are isolated

## Performance

- Synchronization is asynchronous (doesn't block UI)
- Background jobs use Frappe's job queue
- Connection pooling for API requests
- Retry logic for failed requests

## Roadmap

- [ ] Credential synchronization (OAuth tokens)
- [ ] Template workflows for common integrations
- [ ] Real-time webhook notifications from n8n
- [ ] Workflow versioning and rollback
- [ ] Multi-step workflow builder UI
- [ ] Execution analytics and monitoring
