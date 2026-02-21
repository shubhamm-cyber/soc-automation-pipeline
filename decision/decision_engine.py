# decision/decision_engine.py

# ---------------------------------------------------
# Response Playbook Mapping
# ---------------------------------------------------

RESPONSE_PLAYBOOK = {
    "CRITICAL": [
        "Disable affected user account",
        "Force password reset immediately",
        "Revoke active authentication sessions",
        "Block phishing domain and related IOCs",
        "Investigate data access activity",
        "Notify SOC team and incident response lead"
    ],

    "HIGH": [
        "Escalate incident to SOC analyst",
        "Validate suspicious login activity",
        "Check geo-location anomalies",
        "Prepare containment actions if needed"
    ],

    "MEDIUM": [
        "Review phishing URL reputation",
        "Monitor user session activity",
        "Correlate with recent alerts"
    ],

    "LOW": [
        "Log activity for monitoring",
        "Track recurrence trends"
    ]
}


# ---------------------------------------------------
# Decision Engine
# Determines SOC decision + recommended actions
# ---------------------------------------------------

def make_decision(alert):

    severity = alert.get("severity", "LOW").upper()

    # --- Decision Logic ---
    if severity == "CRITICAL":
        decision = "Initiate containment and incident response"

    elif severity == "HIGH":
        decision = "Escalate to SOC analyst immediately"

    elif severity == "MEDIUM":
        decision = "Send to analyst review queue"

    else:
        decision = "Log for monitoring"

    # --- Recommended Actions ---
    recommended_actions = RESPONSE_PLAYBOOK.get(severity, [])

    # --- Attach results to alert object ---
    alert["decision"] = decision
    alert["recommended_actions"] = recommended_actions

    return alert

