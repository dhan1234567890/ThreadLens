import pandas as pd
import random
import uuid
from datetime import datetime, timedelta

def generate_firewall_logs(num_logs=100):
    ips = [f"192.168.1.{i}" for i in range(10, 20)]
    external_ips = [f"203.0.113.{i}" for i in range(1, 10)]
    actions = ["ALLOW", "DENY"]
    
    logs = []
    now = datetime.now()
    for _ in range(num_logs):
        logs.append({
            "timestamp": (now - timedelta(minutes=random.randint(1, 1000))).isoformat(),
            "source_ip": random.choice(ips),
            "destination_ip": random.choice(external_ips),
            "port": random.choice([80, 443, 22, 3389, 445]),
            "action": random.choice(actions)
        })
    return pd.DataFrame(logs)

def generate_ids_alerts(num_alerts=20):
    ips = [f"192.168.1.{i}" for i in range(10, 20)]
    external_ips = [f"203.0.113.{i}" for i in range(1, 10)]
    signatures = [
        {"name": "Suspicious SSH Brute Force", "cve": "CVE-2023-XXXX", "technique": "T1110"},
        {"name": "Malware Beaconing Detected", "cve": None, "technique": "T1071"},
        {"name": "SQL Injection Attempt", "cve": "CVE-2021-32694", "technique": "T1190"}
    ]
    
    alerts = []
    now = datetime.now()
    for _ in range(num_alerts):
        sig = random.choice(signatures)
        alerts.append({
            "timestamp": (now - timedelta(minutes=random.randint(1, 500))).isoformat(),
            "source_ip": random.choice(external_ips),
            "destination_ip": random.choice(ips),
            "alert_name": sig["name"],
            "cve": sig["cve"],
            "mitre_technique": sig["technique"],
            "severity": random.choice(["HIGH", "MEDIUM", "LOW"])
        })
    return pd.DataFrame(alerts)

if __name__ == "__main__":
    fw_logs = generate_firewall_logs()
    ids_alerts = generate_ids_alerts()
    
    fw_logs.to_csv("firewall_logs.csv", index=False)
    ids_alerts.to_csv("ids_alerts.csv", index=False)
    print("Mock data generated: firewall_logs.csv, ids_alerts.csv")
