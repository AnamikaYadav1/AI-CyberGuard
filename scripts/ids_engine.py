import re
import random
from datetime import datetime

def detect_port_scan(log_line):
    ports = re.findall(r"PORT=(.*)", log_line)
    if ports:
        port_list = ports[0].split(",")
        if len(port_list) >= 5:
            return True, "PortScan"
    return False, None

def detect_brute_force(log_line):
    match = re.search(r"FAILED LOGIN.*count=(\d+)", log_line)
    if match and int(match.group(1)) >= 5:
        return True, "BruteForce"
    return False, None

def detect_sql_injection(log_line):
    payloads = ["' or 1=1 --", "' OR '1'='1", "UNION SELECT", "<script>", "DROP TABLE"]
    for p in payloads:
        if p.lower() in log_line.lower():
            return True, "SQLiAttempt"
    return False, None

def detect_malware_download(log_line):
    if "exe" in log_line.lower() or "malware" in log_line.lower():
        return True, "MalwareDownload"
    return False, None

def detect_failed_login(log_line):
    if "failed password" in log_line.lower():
        return True, "FailedLogin"
    return False, None

def generate_fake_attack():
    attacks = [
        ("10.0.0.5", "PortScan"),
        ("192.168.1.10", "SQLiAttempt"),
        ("172.16.2.9", "BruteForce"),
        ("8.8.8.8", "FailedLogin"),
        ("103.21.244.0", "MalwareDownload"),
    ]
    ip, attack = random.choice(attacks)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return {
        "source_ip": ip,
        "event": attack,
        "timestamp": timestamp
    }
"""# Example usage
if __name__ == "__main__":
    sample_logs = [
        "2024-06-01 12:00:00 PORT=22,23,80,443,8080",
        "2024-06-01 12:05:00 FAILED LOGIN user=admin count=7",
        "2024-06-01 12:10:00 SQL QUERY='SELECT * FROM users WHERE username='' OR '1'='1' --'",
        "2024-06-01 12:15:00 DOWNLOAD URL=http://malicious.com/malware.exe",
    ]

    for log in sample_logs:
        for detector in [detect_port_scan, detect_brute_force, detect_sql_injection,
                         detect_malware_download, detect_failed_login]:
            detected, attack_type = detector(log)
            if detected:
                print(f"Detected {attack_type} in log: {log}")

    fake_attack = generate_fake_attack()
    print("Generated Fake Attack:", fake_attack)