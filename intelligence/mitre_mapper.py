def map_mitre(alert):

    techniques = []

    action_map = {
        "email_link_clicked": ("T1566", "Phishing"),
        "page_visit": ("T1595", "Active Scanning"),
        "credential_submission": ("T1056", "Input Capture"),
        "mfa_bypass_attempt": ("T1621", "Multi-Factor Authentication Request Generation"),
        "session_activity": ("T1078", "Valid Accounts"),
        "password_change_attempt": ("T1098", "Account Manipulation"),
        "data_access": ("T1539", "Data from Web Session")
    }

    timeline = alert.get("attack_timeline", [])

    for event in timeline:
        action = event.get("action")

        if action in action_map:
            technique_id, name = action_map[action]

            techniques.append({
                "technique_id": technique_id,
                "name": name
            })

    # Remove duplicates
    unique = {t["technique_id"]: t for t in techniques}

    alert["mitre_attack"] = list(unique.values())
    alert["mitre_ids"] = list(unique.keys())

    return alert
