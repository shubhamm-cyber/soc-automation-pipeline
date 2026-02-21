from flask import Flask, request, jsonify
from datetime import datetime

# ---- Modules ----
from normalization.normalize_alert import normalize_alert
from extraction.ioc_extractor import extract_iocs
from scoring.risk_engine import calculate_risk
from decision.decision_engine import make_decision
from response.report_generator import generate_report
from case_management.case_manager import create_case
from intelligence.mitre_mapper import map_mitre
from intelligence.attack_timeline import build_attack_timeline
from response.slack_notifier import send_slack_alert
from decision.severity_booster import boost_severity
from response.splunk_sender import send_to_splunk
from utils.timeline import add_timeline


app = Flask(__name__)

# -------------------------------------------------
# Helpers
# -------------------------------------------------

def format_timestamp(epoch_time):
    """
    Convert epoch timestamp → SOC readable time
    """
    try:
        if not epoch_time:
            return ""

        epoch_time = int(epoch_time)

        return datetime.fromtimestamp(epoch_time).strftime(
            "%Y-%m-%d %H:%M:%S"
        )

    except Exception:
        return str(epoch_time)


def get_timestamp(result):
    """
    Extract timestamp safely from aggregated Splunk results
    """
    times = result.get("times", [])
    if times:
        return times[0]
    return ""


def get_primary_user(users):
    """
    Select most relevant user.
    (Last user usually = attacker progression)
    """
    if not users:
        return "unknown"

    return users[-1]   # last activity user


# -------------------------------------------------
# Webhook Endpoint
# -------------------------------------------------

@app.route("/splunk-alert", methods=["POST"])
def receive_alert():

    data = request.json

    print("\n[+] Alert received from Splunk")
    print(data)

    # -------------------------------------------------
    # Handle Splunk webhook formats
    # -------------------------------------------------

    results = []

    # Real-time alert
    if "result" in data:
        results = [data["result"]]

    # Scheduled alert (aggregated)
    elif "results" in data:
        results = data["results"]

    result = results[0] if results else {}

    # -------------------------------------------------
    # Extract Aggregated Fields
    # -------------------------------------------------

    users = result.get("users", [])
    domains = result.get("domains", [])

    primary_user = get_primary_user(users)

    timestamp_epoch = get_timestamp(result)

    # -------------------------------------------------
    # Base Alert Object
    # -------------------------------------------------

    alert = {
        "alert_name": data.get("search_name", "Splunk Alert"),
        "user": primary_user,
        "all_users": users,  # keep full victim list
        "url": domains[0] if domains else "unknown",
        "timestamp": format_timestamp(timestamp_epoch),
        "timestamp_epoch": timestamp_epoch
    }

    # -------------------------------------------------
    # 🔥 Build Attack Timeline
    # -------------------------------------------------

    alert = build_attack_timeline(alert, results)

    # -------------------------------------------------
    # AURORA Investigation Pipeline
    # -------------------------------------------------

    incident = add_timeline(alert, "alert_received")

    incident = normalize_alert(incident)
    incident = add_timeline(incident, "normalized")

    incident = extract_iocs(incident)
    incident = add_timeline(incident, "ioc_extracted")

    incident = calculate_risk(incident)
    incident = add_timeline(incident, "risk_scored")

    incident = map_mitre(incident)
    incident = add_timeline(incident, "mitre_mapped")

    incident = boost_severity(incident)
    incident = add_timeline(incident, "severity_boosted")

    incident = make_decision(incident)
    incident = add_timeline(incident, "decision_made")

    create_case(incident)
    incident = add_timeline(incident, "case_created")

    incident = generate_report(incident)
    incident = add_timeline(incident, "report_generated")

    # -------------------------------------------------
    # Response Actions
    # -------------------------------------------------

    send_slack_alert(incident)

    

    send_to_splunk(incident)

    return jsonify({"status": "processed"}), 200


# -------------------------------------------------
# Run Server
# -------------------------------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
