"""
attack_timeline.py

Builds chronological attacker activity timeline
from aggregated Splunk alert results.

"""

def build_attack_timeline(alert, results):

    timeline = []
    seen_events = set()

    # --------------------------------------------------
    # Splunk sends results as a LIST
    # --------------------------------------------------

    if isinstance(results, list) and len(results) > 0:
        results = results[0]

    # Safety fallback
    if not isinstance(results, dict):
        alert["attack_timeline"] = timeline
        alert["all_users"] = []
        alert["primary_compromised_user"] = None
        alert["affected_user_count"] = 0
        return alert

    # --------------------------------------------------
    # Stage severity mapping
    # --------------------------------------------------

    action_severity = {
        "email_link_clicked": "LOW",
        "page_visit": "LOW",
        "credential_submission": "MEDIUM",
        "mfa_bypass_attempt": "MEDIUM",
        "session_activity": "MEDIUM",
        "password_change_attempt": "HIGH",
        "data_access": "HIGH"
    }

    times = results.get("times", [])
    users = results.get("users", [])
    domains = results.get("domains", [])
    actions = results.get("actions", [])
    uris = results.get("uris", [])
    ips = results.get("ips", [])

    # --------------------------------------------------
    # Build timeline events (DEDUPLICATED)
    # --------------------------------------------------

    for i in range(len(times)):

        event = {
            "time": int(times[i]),
            "user": users[i],
            "domain": domains[i],
            "action": actions[i],
            "uri": uris[i],
            "ip": ips[i],
            "stage_severity": action_severity.get(actions[i], "LOW")
        }

        # Stable fingerprint (prevents duplicates)
        fingerprint = (
            users[i],
            actions[i],
            uris[i],
            domains[i],
            ips[i]
        )

        if fingerprint not in seen_events:
            seen_events.add(fingerprint)
            timeline.append(event)

    # --------------------------------------------------
    # Ensure chronological order
    # --------------------------------------------------

    timeline.sort(key=lambda x: x["time"])

    # --------------------------------------------------
    # Extract unique users
    # --------------------------------------------------

    unique_users = []
    seen_users = set()

    for event in timeline:
        user = event.get("user")

        if user and user not in seen_users:
            seen_users.add(user)
            unique_users.append(user)

    # --------------------------------------------------
    # Identify Primary Compromised User
    # --------------------------------------------------

    severity_rank = {
        "LOW": 1,
        "MEDIUM": 2,
        "HIGH": 3
    }

    user_max_severity = {}

    for event in timeline:
        user = event.get("user")
        sev = event.get("stage_severity", "LOW")

        if user not in user_max_severity:
            user_max_severity[user] = sev
        else:
            if severity_rank[sev] > severity_rank[user_max_severity[user]]:
                user_max_severity[user] = sev

    primary_user = None
    highest = 0

    for user, sev in user_max_severity.items():
        if severity_rank[sev] > highest:
            highest = severity_rank[sev]
            primary_user = user

    # --------------------------------------------------
    # Attach results back to alert
    # --------------------------------------------------

    alert["attack_timeline"] = timeline
    alert["all_users"] = unique_users
    alert["primary_compromised_user"] = primary_user
    alert["affected_user_count"] = len(unique_users)

    return alert
