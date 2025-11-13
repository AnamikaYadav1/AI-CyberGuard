# scripts/generate_fake_scans.py

import random
from datetime import datetime, timedelta
from db_logger import log_scan, init_db

# Initialize DB (in case it wasn't created)
init_db()

fake_urls = [
    "https://google.com",
    "http://phishy-site-login.net",
    "https://secure-payments.co.in",
    "http://malicious-update.xyz",
    "https://youtube.com",
    "https://schoolportal.edu",
]

fake_texts = [
    "You’re amazing! Keep going.",
    "You are such a loser.",
    "Great job on your project!",
    "Everyone hates you.",
    "This is so cool, I love it!",
    "I will hack your account.",
]

def generate_fake_data():
    print("💾 Generating fake scan data...")
    for i in range(6):
        # Random URL scans
        url = fake_urls[i]
        confidence = round(random.uniform(0.3, 0.99), 2)
        result = "⚠️ Malicious" if "phish" in url or "malicious" in url else "✅ Safe"
        log_scan("URL", url, result, confidence)

        # Random text scans
        text = fake_texts[i]
        confidence = round(random.uniform(0.4, 0.95), 2)
        result = "🚨 Cyberbullying" if any(w in text.lower() for w in ["loser", "hate", "hack"]) else "✅ Safe"
        log_scan("Text", text, result, confidence)

    print("✅ Fake data inserted successfully!")

if __name__ == "__main__":
    generate_fake_data()
