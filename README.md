# End-to-End Phishing Investigation & Response Automation

**Python + Splunk | SOC Automation Project**

---

## 1️⃣ Executive Summary

Modern Security Operations Centers (SOCs) process large volumes of alerts that often require manual validation and correlation before analysts can determine whether activity represents a real security incident. This project simulates how an enterprise SOC can automate phishing investigations while preserving analyst visibility and decision control.

The Automated Phishing Detection & Incident Response Platform integrates **Splunk Enterprise** with a custom Python-based SOAR workflow to detect phishing activity, reconstruct attacker behavior, calculate dynamic risk scores, and generate structured incident response recommendations.

Instead of treating alerts independently, the system correlates related events, builds an investigation narrative, maps behaviors to MITRE ATT&CK techniques, and indexes investigation results back into Splunk dashboards for analyst review.

**Outcome**

* Automated investigation lifecycle from detection to incident reporting
* Centralized SOC visibility through Splunk dashboards
* Consistent and repeatable phishing incident triage workflow

📸 **SOC Dashboard Overview**


<img width="2233" height="2113" alt="Phishing Detection   Automated Incident Response Dashboard" src="https://github.com/user-attachments/assets/0640c961-e6b7-4974-b615-df5cc0f1fe49" />


*Splunk dashboard displaying incident outcome, attack timeline reconstruction, activity visualization, severity evolution, MITRE ATT&CK mapping, and targeted user analysis.*

---

## 2️⃣ Problem Statement

SOC teams commonly encounter operational challenges during phishing investigations:

**Alert Fatigue**
Multiple alerts generated from related activity require repeated manual analysis.

**Manual Investigation Overhead**
Analysts must correlate logs, identify affected users, and reconstruct timelines manually.

**Limited Context Awareness**
Traditional alerts identify indicators but fail to explain attacker progression.

These challenges increase investigation time and risk of missed threats during high alert volume.

---

## 3️⃣ Solution Architecture

The platform follows a structured SOC lifecycle where Splunk performs detection and visualization while Python automation performs investigation orchestration.

**Component Responsibilities**

* **Splunk Enterprise** — detection rules and dashboards
* **Flask Webhook** — secure alert ingestion
* **Python Automation Engine** — correlation and analysis
* **Splunk HTTP Event Collector (HEC)** — incident indexing
* **Dashboards** — analyst investigation visibility

📸 **Architecture Diagram**

<img width="1536" height="1024" alt="Flowchart" src="https://github.com/user-attachments/assets/d67ee921-4637-4b0d-b74f-5b73bf320ac4" />

---


## 4️⃣ Detection & Automation Workflow

Detection begins within Splunk using a phishing detection rule designed to identify suspicious credential harvesting behavior.

Workflow:

1. Splunk detection rule triggers
2. Webhook sends alert payload
3. Flask listener receives alert data
4. Python automation initiates investigation

The alert payload contains:

* alert name
* affected users
* suspicious domain information
* timestamps
* detection metadata

📸 **Splunk Detection Rule**

<img width="900" src="https://github.com/user-attachments/assets/cbf67c43-1257-4564-b7d6-b1d64521cfc6" />

<img width="900" src="https://github.com/user-attachments/assets/3273ee6b-4d92-410f-bdd4-8c7fe98b2b84" />

---

## 5️⃣ Investigation Process

After receiving the webhook alert, the Python automation engine performs automated analysis and generates a structured incident investigation report.

The generated output consolidates investigation evidence into an analyst-readable summary containing:

* **Primary affected user**
* **Affected user count**
* **Suspicious phishing domain and URL**
* **Calculated risk score**
* **Severity classification**
* **Automated decision outcome**
* **Recommended remediation actions**

This removes the need for manual log correlation and provides analysts with immediate investigation context.

📸 **Automated Incident Analysis Output**

<img width="650" src="https://github.com/user-attachments/assets/5622d389-146f-4b7d-9f13-82db3714c4c7" />

<img width="650" src="https://github.com/user-attachments/assets/d3d51c3c-c4af-4e7d-a212-ad23453d7ac6" />

---

## 6️⃣ Attack Timeline Reconstruction

Correlated phishing events are visualized within Splunk as an ordered investigation timeline.

The timeline panel displays:

* **Event timestamps**
* **Affected user identity**
* **Phishing domain interaction**
* **Observed attacker actions**
* **Requested URI paths**

This enables analysts to understand attacker progression from initial interaction through credential compromise and subsequent activity.

📸 **Attack Progression Timeline**

<img width="1200" src="https://github.com/user-attachments/assets/a085bf42-f720-4bcf-bfc8-43c532b69835" />

---

## 7️⃣ MITRE ATT&CK Integration

Detected behaviors are automatically mapped to MITRE ATT&CK techniques and visualized inside Splunk.

The visualization displays:

* **Technique ID**
* **Technique name**
* **Occurrence count during investigation**

This provides standardized threat context and helps analysts quickly identify adversary tactics.

Examples observed:

* **T1566 — Phishing**
* **T1056 — Input Capture**
* **T1539 — Data from Web Session**

📸 **MITRE ATT&CK Technique Mapping**

<img width="900" src="https://github.com/user-attachments/assets/de61bb85-b65d-466e-8000-4d2bb475984b" />

---

## 8️⃣ Automated Response Logic

Following investigation, a decision engine evaluates findings using behavioral indicators and calculated risk scoring.

The automation generates a Slack notification containing:

* **Alert name**
* **Severity level**
* **Affected user information**
* **Investigation decision**
* **Incident summary**

This ensures SOC analysts receive actionable context immediately.

📸 **Slack SOC Notification**

<img width="600" src="https://github.com/user-attachments/assets/ab3ecdfd-8f8c-4399-aa0a-1686cee9ca2a" />

---

## 9️⃣ SOC Dashboard Design

The dashboard was developed in **Splunk Enterprise** to provide centralized analyst visibility into automated investigations.

<div align="center">

<img width="2233" height="2113" alt="Phishing Detection   Automated Incident Response Dashboard" src="https://github.com/user-attachments/assets/0640c961-e6b7-4974-b615-df5cc0f1fe49" />

</div>

### Incident Outcome

Displays case information including affected user, phishing domain, calculated risk score, severity level, and automated response decision.

### Attack Progression Timeline

Shows timestamp, user, domain interaction, action performed, and accessed URI for correlated events.

### Attack Activity Over Time

Visualizes event frequency across timestamps to illustrate behavioral progression.

### Severity Evolution

Shows how incident severity changes during investigation.

### MITRE ATT&CK Coverage

Displays mapped techniques with occurrence counts derived from analysis.

### Targeted Users

Lists impacted accounts identified during investigation.

---

## 🔟 Incident Outcome Example

The investigation concludes with an automatically generated incident record indexed into Splunk.

The final summary includes:

* **Case ID**
* **Primary compromised user**
* **Affected user count**
* **Detected phishing domain**
* **Calculated risk score**
* **Severity classification (Critical)**
* **Automated decision**
* **Recommended containment actions**

📸 **Incident Summary**

<img width="750" src="https://github.com/user-attachments/assets/03b4c7e3-d134-4bb7-857e-be0e6f43da6d" />

<img width="750" src="https://github.com/user-attachments/assets/3d0b4d6e-3d10-4134-819a-3e9fd86cfdbe" />

---

## 1️⃣1️⃣ Skills Demonstrated

### Detection Engineering

* SPL detection development
* Behavioral phishing analytics

### SOC Investigation

* Timeline reconstruction
* Threat behavior correlation

### Automation Development

* Python SOAR workflows
* Flask webhook integration

### SIEM Engineering

* Splunk alert configuration
* HTTP Event Collector integration
* Dashboard development

### Incident Response

* Risk scoring and severity classification
* Automated response workflows

---

## 1️⃣2️⃣ Conclusion

This project demonstrates how detection engineering and automation can improve SOC investigation efficiency. By integrating Splunk detection with a custom Python SOAR workflow, isolated alerts are transformed into structured investigations supported by behavioral analysis, risk scoring, and standardized threat mapping.

Automation accelerates investigation while dashboards maintain analyst visibility and control, reflecting real-world SOC operational practices.

---

