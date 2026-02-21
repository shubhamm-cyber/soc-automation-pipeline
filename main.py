import json
from normalization.normalize_alert import normalize_alert
from extraction.ioc_extractor import extract_iocs
from scoring.risk_engine import calculate_risk
from decision.decision_engine import make_decision
from response.report_generator import generate_report
from case_management.case_manager import create_case


def load_alert():
    with open("config/sample_alert.json") as f:
        return json.load(f)


def main():
    print("\n[+] AURORA-Py Advanced Starting...\n")

    alert = load_alert()
    print("[1] Alert Loaded")

    normalized = normalize_alert(alert)
    print("[2] Alert Normalized")

    extracted = extract_iocs(normalized)
    print("[3] IOC Extraction Complete")

    scored = calculate_risk(extracted)
    print("[4] Risk Scoring Complete")

    decided = make_decision(scored)
    print("[5] Decision Engine Complete")

    report = generate_report(decided)
    print("[6] Report Generated")

    create_case(report)
    print("[7] Case Created Successfully")


if __name__ == "__main__":
    main()
