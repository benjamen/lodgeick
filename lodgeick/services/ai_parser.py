"""
AI-powered intent parser for Google API integration setup
Uses Claude AI to interpret natural language and map to Google APIs
"""

import frappe
import json
from typing import Dict, List, Optional
import anthropic


# Known billing-required APIs (canonical Google API identifiers)
BILLING_REQUIRED_APIS = [
    "maps-backend.googleapis.com",
    "maps.googleapis.com",
    "vision.googleapis.com",
    "language.googleapis.com",
    "translate.googleapis.com",
    "speech.googleapis.com",
    "texttospeech.googleapis.com",
    "videointelligence.googleapis.com",
    "ml.googleapis.com",
    "aiplatform.googleapis.com",
    "vertexai.googleapis.com",
    "bigquery.googleapis.com",
    "compute.googleapis.com",
    "container.googleapis.com",
    "run.googleapis.com",
    "cloudfunctions.googleapis.com",
    "cloudscheduler.googleapis.com",
    "pubsub.googleapis.com",
    "storage.googleapis.com",
]

# System prompt for Claude to structure its responses
SYSTEM_PROMPT = """You are the AI backend for Lodgeick's Integration Assistant.
Your job is to interpret natural-language integration requests and output structured configuration for Google Cloud setup.

You will:
1. Identify which Google APIs are needed based on user intent
2. Determine the correct OAuth scopes for each API
3. Check if any APIs require billing (based on the known list)
4. Return a JSON object describing what should be enabled and whether billing is required

IMPORTANT RULES:
- Never guess API names that don't exist
- Always use canonical *.googleapis.com identifiers
- Use the exact scope URLs from Google's official documentation
- Be conservative: only suggest APIs that are clearly needed
- If billing is required, explain which specific API(s) need it

Common Google APIs and their scopes:
- Gmail API (gmail.googleapis.com):
  - Read: https://www.googleapis.com/auth/gmail.readonly
  - Send: https://www.googleapis.com/auth/gmail.send
  - Full access: https://mail.google.com/

- Google Sheets API (sheets.googleapis.com):
  - Read/Write: https://www.googleapis.com/auth/spreadsheets
  - Read only: https://www.googleapis.com/auth/spreadsheets.readonly

- Google Drive API (drive.googleapis.com):
  - Full access: https://www.googleapis.com/auth/drive
  - File access: https://www.googleapis.com/auth/drive.file
  - Read only: https://www.googleapis.com/auth/drive.readonly

- Google Calendar API (calendar.googleapis.com):
  - Full access: https://www.googleapis.com/auth/calendar
  - Read only: https://www.googleapis.com/auth/calendar.readonly

- Google Contacts API (people.googleapis.com):
  - Read: https://www.googleapis.com/auth/contacts.readonly
  - Write: https://www.googleapis.com/auth/contacts

- Google Maps APIs (maps.googleapis.com, maps-backend.googleapis.com):
  - REQUIRES BILLING
  - Scope: https://www.googleapis.com/auth/maps

- Cloud Vision API (vision.googleapis.com):
  - REQUIRES BILLING
  - Scope: https://www.googleapis.com/auth/cloud-vision

- Cloud Natural Language API (language.googleapis.com):
  - REQUIRES BILLING
  - Scope: https://www.googleapis.com/auth/cloud-language

- YouTube Data API (youtube.googleapis.com):
  - Read only: https://www.googleapis.com/auth/youtube.readonly
  - Upload: https://www.googleapis.com/auth/youtube.upload

- Google Photos Library API (photoslibrary.googleapis.com):
  - Read only: https://www.googleapis.com/auth/photoslibrary.readonly
  - Append: https://www.googleapis.com/auth/photoslibrary.appendonly

Output Format (JSON only, no markdown):
{
  "apis": [
    {
      "name": "gmail.googleapis.com",
      "display_name": "Gmail API",
      "scopes": ["https://www.googleapis.com/auth/gmail.send"],
      "description": "Send emails on behalf of the user"
    }
  ],
  "billing_required": false,
  "billing_apis": [],
  "reasoning": "Brief explanation of why these APIs and scopes were chosen"
}"""


class AIIntentParser:
    """Parse user intent using Claude AI to determine required Google APIs and scopes"""

    def __init__(self):
        """Initialize Claude client"""
        self.api_key = frappe.conf.get("anthropic_api_key")
        if not self.api_key:
            frappe.throw("Anthropic API key not configured in site config. Add 'anthropic_api_key' to site_config.json")

        self.client = anthropic.Anthropic(api_key=self.api_key)

    def parse_intent(self, user_intent: str) -> Dict:
        """
        Parse user's natural language intent into structured Google API configuration

        Args:
            user_intent: Natural language description of what user wants to do

        Returns:
            Dict containing:
            {
                "apis": [{"name": str, "display_name": str, "scopes": [str], "description": str}],
                "billing_required": bool,
                "billing_apis": [str],
                "reasoning": str
            }
        """
        try:
            # Call Claude API
            message = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=2000,
                temperature=0.2,  # Low temperature for consistent, deterministic output
                system=SYSTEM_PROMPT,
                messages=[
                    {
                        "role": "user",
                        "content": f"Parse this integration request:\n\n{user_intent}"
                    }
                ]
            )

            # Extract the response
            response_text = message.content[0].text.strip()

            # Remove markdown code blocks if present
            if response_text.startswith("```json"):
                response_text = response_text[7:]  # Remove ```json
            if response_text.startswith("```"):
                response_text = response_text[3:]  # Remove ```
            if response_text.endswith("```"):
                response_text = response_text[:-3]  # Remove trailing ```

            response_text = response_text.strip()

            # Parse JSON response
            parsed = json.loads(response_text)

            # Validate billing detection
            detected_billing_apis = []
            for api in parsed.get("apis", []):
                api_name = api.get("name", "")
                if api_name in BILLING_REQUIRED_APIS:
                    detected_billing_apis.append(api_name)

            # Override billing_required based on our authoritative list
            if detected_billing_apis:
                parsed["billing_required"] = True
                parsed["billing_apis"] = detected_billing_apis
            else:
                parsed["billing_required"] = False
                parsed["billing_apis"] = []

            return parsed

        except json.JSONDecodeError as e:
            frappe.log_error(f"Failed to parse AI response as JSON: {response_text}", "AI Parser Error")
            frappe.throw(f"AI returned invalid JSON: {str(e)}")

        except anthropic.APIError as e:
            frappe.log_error(f"Anthropic API error: {str(e)}", "AI Parser Error")
            frappe.throw(f"AI service error: {str(e)}")

        except Exception as e:
            frappe.log_error(f"Unexpected error in AI parser: {str(e)}", "AI Parser Error")
            frappe.throw(f"Failed to parse intent: {str(e)}")


def get_ai_parser() -> AIIntentParser:
    """
    Get singleton instance of AI parser

    Returns:
        AIIntentParser instance
    """
    if not hasattr(frappe.local, "ai_parser"):
        frappe.local.ai_parser = AIIntentParser()
    return frappe.local.ai_parser


@frappe.whitelist()
def parse_integration_intent(intent: str) -> Dict:
    """
    Public API endpoint to parse user intent

    Args:
        intent: User's natural language integration request

    Returns:
        Parsed API configuration
    """
    parser = get_ai_parser()
    return parser.parse_intent(intent)
