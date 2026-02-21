import requests
import os

SLACK_WEBHOOK = os.getenv("SLACK_WEBHOOK_URL")


def send_slack_alert(alert):

    case_id = alert.get("case_id", "CASE-PENDING")
    severity = alert.get("severity", "UNKNOWN")
    decision = alert.get("decision", "Pending")
    domain = alert.get("iocs", {}).get("domain", "N/A")

    primary_user = alert.get("primary_compromised_user", "N/A")
    affected_users = alert.get("affected_user_count", 0)

    message_text = f"""
🚨 *SOC INCIDENT ALERT*

*Case ID:* {case_id}
*Severity:* {severity}

*Primary Compromised User:* {primary_user}
*Affected Users:* {affected_users}
*Domain:* {domain}

*Decision:* {decision}
"""

    payload = {
        "text": message_text
    }

    try:
        requests.post(SLACK_WEBHOOK, json=payload, timeout=5)
    except Exception as e:
        print(f"[WARNING] Slack notification failed: {e}")