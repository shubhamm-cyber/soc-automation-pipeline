import json
import os
from datetime import datetime

def create_case(data):

    case_id = datetime.now().strftime("CASE-%Y%m%d-%H%M%S")
    data["case_id"] = case_id

    os.makedirs("cases", exist_ok=True)

    filepath = os.path.join("cases", f"{case_id}.json")

    with open(filepath, "w") as f:
        json.dump(data, f, indent=4)

    print(f"[+] Case stored: {filepath}")
