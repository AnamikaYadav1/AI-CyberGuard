import random, time, os, sqlite3
from faker import Faker
from datetime import datetime

fake = Faker()
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "scan_logs.db")

def create_fake_entry():
    types = ["PortScan","FailedLogin","SQLiAttempt","BruteForce","MalwareDownload"]
    t = random.choice(types)
    src_ip = fake.ipv4_public()
    desc = f"{t} from {src_ip}"
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return (t, src_ip, desc, 0.0, ts)

def insert_n(n=50):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    for _ in range(n):
        t, src, desc, conf, ts = create_fake_entry()
        c.execute("INSERT INTO scans (type, input, result, confidence, timestamp) VALUES (?, ?, ?, ?, ?)",
                  (t, src, desc, conf, ts))
    conn.commit()
    conn.close()
    print(f"Inserted {n} fake logs.")
if __name__ == '__main__':
    insert_n(100)
