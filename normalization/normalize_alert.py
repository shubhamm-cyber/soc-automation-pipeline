def normalize_alert(alert):

    
    normalized = alert.copy()

    normalized["alert_type"] = "phishing"
    normalized["user"] = alert.get("user", "unknown")
    normalized["url"] = alert.get("url", "unknown")
    normalized["timestamp"] = alert.get("timestamp", "")
    normalized["iocs"] = alert.get("iocs", {})

    return normalized

