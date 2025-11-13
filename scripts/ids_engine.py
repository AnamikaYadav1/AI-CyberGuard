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
