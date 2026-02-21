from datetime import datetime


def add_timeline(alert, stage):

    if "timeline" not in alert:
        alert["timeline"] = []

    alert["timeline"].append({
        "stage": stage,
        "time": datetime.utcnow().isoformat()
    })

    return alert
