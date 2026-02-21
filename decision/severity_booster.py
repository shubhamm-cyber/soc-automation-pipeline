def boost_severity(alert):

    techniques = alert.get("mitre_attack", [])
    technique_count = len(techniques)

    current = alert.get("severity", "LOW")

    severity_order = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]

    if technique_count >= 2:
        try:
            index = severity_order.index(current)
            new_index = min(index + 1, len(severity_order) - 1)
            alert["severity"] = severity_order[new_index]
            alert["analysis_reasons"].append(
                "Severity boosted due to multiple MITRE ATT&CK techniques"
            )
        except ValueError:
            pass

    return alert