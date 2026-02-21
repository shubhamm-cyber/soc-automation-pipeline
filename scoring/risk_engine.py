"""
risk_engine.py

Purpose:
Calculates behavioral risk score and determines incident severity
based on attacker progression through the attack timeline.

"""

def calculate_risk(alert):

    # --------------------------------------------------
    # Initialization
    # --------------------------------------------------

    timeline = alert.get("attack_timeline", [])
    score = 0
    reasons = []

    # --------------------------------------------------
    # Behavioral Risk Scoring (Stage-Based + Ordered)
    # --------------------------------------------------

    action_scores = {
        "email_link_clicked": 5,
        "page_visit": 5,
        "credential_submission": 25,
        "mfa_bypass_attempt": 20,
        "session_activity": 10,
        "password_change_attempt": 15,
        "data_access": 25
    }

    # Maintain order while removing duplicates
    unique_actions = []
    seen_actions = set()

    for event in timeline:
        action = event.get("action")

        if action in action_scores and action not in seen_actions:
            unique_actions.append(action)   # preserves timeline order
            seen_actions.add(action)

    # Score once per attacker behavior
    for action in unique_actions:
        score += action_scores[action]
        reasons.append(f"Observed activity: {action}")

    # --------------------------------------------------
    # Base phishing context
    # --------------------------------------------------

    if alert.get("alert_type") == "phishing":
        score += 10
        reasons.append("Phishing alert category")

    # --------------------------------------------------
    # Incident Severity Determination
    # (based on highest attack stage reached)
    # --------------------------------------------------

    severity_order = ["LOW", "MEDIUM", "HIGH"]
    incident_severity = "LOW"

    for event in timeline:

        stage_severity = event.get("stage_severity", "LOW")

        if severity_order.index(stage_severity) > severity_order.index(incident_severity):
            incident_severity = stage_severity

    # --------------------------------------------------
    # Multi-Stage Attack Detection
    # --------------------------------------------------

    if len(unique_actions) >= 5:
        score += 15
        reasons.append("Multi-stage attack behavior detected")

    # --------------------------------------------------
    # Attach Results Back To Alert Object
    # --------------------------------------------------

    alert["risk_score"] = score
    alert["severity"] = incident_severity
    alert["analysis_reasons"] = reasons

    return alert