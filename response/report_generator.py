def generate_report(alert):

    # ---------- SAFE FIELD ACCESS ----------
    case_id = alert.get("case_id", "CASE-PENDING")
    user = alert.get("user", "Unknown")
    url = alert.get("url", "N/A")
    domain = alert.get("iocs", {}).get("domain", "N/A")
    risk_score = alert.get("risk_score", 0)
    severity = alert.get("severity", "UNKNOWN")
    decision = alert.get("decision", "Pending analysis")

    # ---------- MITRE SECTION ----------
    mitre_section = ""
    mitre_ids = []

    if alert.get("mitre_attack"):
        mitre_lines = []
        for t in alert["mitre_attack"]:
            mitre_lines.append(f"{t['technique_id']} - {t['name']}")
            mitre_ids.append(t["technique_id"])

        mitre_section = "\nMITRE ATT&CK Techniques:\n" + "\n".join(mitre_lines)

    # ---------- RECOMMENDED ACTIONS SECTION ----------
    actions = alert.get("recommended_actions", [])
    actions_section = ""

    if actions:
        action_lines = [f"• {a}" for a in actions]
        actions_section = "\nRecommended Actions:\n" + "\n".join(action_lines)

    # ---------- ANALYST REPORT ----------
    report = f"""
===== Security Incident Analysis Report =====

Case ID: {case_id}
User: {user}
Primary Compromised User: {alert.get('primary_compromised_user', 'N/A')}
Affected Users: {alert.get('affected_user_count', 0)}

URL: {url}
Domain: {domain}

Risk Score: {risk_score}
Severity: {severity}

Reasons:
{chr(10).join(alert.get('analysis_reasons', []))}

Decision:
{decision}
{actions_section}
{mitre_section}
"""

    # ---------- MACHINE-READABLE FIELDS ----------
    alert["mitre_ids"] = mitre_ids
    alert["report"] = report
    alert["recommended_actions"] = actions

    print(report)

    return alert