from urllib.parse import urlparse

def extract_iocs(alert):
    url = alert["url"]
    domain = urlparse(f"http://{url}").netloc
    alert["iocs"]["domain"] = domain
    return alert
