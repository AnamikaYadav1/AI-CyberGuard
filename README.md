🛡️ AI CyberGuard — Unified Cybersecurity Detection Suite

AI CyberGuard is an advanced, multi-module cybersecurity system that integrates AI-powered threat detection, URL scanning, malware analysis, cyberbullying detection, QR scanning, fake profile detection, analytics dashboards, and database-backed threat logging — all in one platform.

This system acts as a mini SIEM (Security Information & Event Management) tool with ML-based detection, explainability, and real-time analytics.

🚀 Features Overview
✅ 1. Malicious URL Detection (ML-Based)

Trained ML model to classify URLs as Safe or Malicious

Feature extraction (length, entropy, digits, suspicious patterns)

Explainable AI showing why URL was flagged

Database logging for each scan

Confidence score with colored result indicator

💬 2. Cyberbullying / Text Abuse Detection

ML model to classify comments as:

Toxic

Threat

Harassment

Safe

TF-IDF feature extraction

Explainable AI with top contributing words

Logs are stored in SQLite database

🔍 3. File Hash Malware Scanner (Basic + Extendable)

Upload any file

SHA-256 hashing

Lookup from local JSON malware signatures

Expandable to VIRUSTOTAL API integration

Logged into analytics dashboard

🧾 4. QR Code Scanner

Extract text/URL from QR images

Auto-send extracted URLs to malicious URL checker

Supports PNG, JPG, JPEG

🕵️ 5. Fake Profile Detection (Heuristic Analysis)

Detects suspicious social media accounts using:

Account age

Followers/following ratio

Profile image missing

Username anomalies

Frequent numbers in username

Fake-likelihood scoring with progress bar

📊 6. Threat Analytics Dashboard (Mini SIEM)

Displays real-time analytics of all scans:

Total scans

Safe vs. Malicious breakdown

Scan type distribution

Time-based event histogram

Fake profile and URL trends

Network attack simulation charts

Top IP addresses (for network logs)

🗄️ 7. Local Threat Database (SQLite)

Every scan is stored:

Type (URL/Text/File/QR/Profile)

Input data

Result

Confidence

Timestamp

Used for dashboards & SOC-style logs.

🧠 Tech Stack
Frontend / UI

Streamlit

Backend

Python

SQLite

Custom ML models

Machine Learning Libraries

Scikit-Learn

Joblib

Pandas

TF-IDF Vectorizer

Cybersecurity Libraries

PyZbar (QR scanning)

Hashlib (file hashing)

🏗️ Project Structure
ai_cyber_guard/
│
├── app.py
├── models/
│   ├── url_model.joblib
│   ├── text_model.joblib
│   ├── tfidf_vectorizer.joblib
│
├── scripts/
│   ├── url_features.py
│   ├── xai_url.py
│   ├── xai_text.py
│   ├── file_scanner.py
│   ├── qr_reader.py
│   ├── fake_profile.py
│   ├── db_logger.py
│   ├── analytics.py
│
└── data/
    └── scan_logs.db

⚡ Installation
1️⃣ Clone the repo
git clone https://github.com/yourusername/ai-cyber-guard.git
cd ai-cyber-guard

2️⃣ Create Virtual Environment
python -m venv venv
venv\Scripts\activate

3️⃣ Install Requirements
pip install -r requirements.txt

4️⃣ Run App
streamlit run app.py

🧪 Usage
🟦 URL Scanner

Enter any URL → Get classification + explanation

🟪 Text Analyzer

Paste message → Detect toxic/harmful content

🟧 File Scanner

Upload file → Detect known malicious signatures

🟩 QR Scanner

Upload QR → Auto-detect embedded text/URLs

🟨 Fake Profile Detector

Enter social media info → Suspiciousness score

🟥 Analytics Dashboard

View threat insights, event logs, charts, heatmaps

🛠️ Future Enhancements (Advanced Cybersecurity Roadmap)

We will add:

🔥 1. Intrusion Detection System (IDS)

Port Scan Detection

Brute-force login detection

Suspicious traffic alerts

Scapy packet monitoring

🔥 2. Phishing Email Analyzer

Spoofed sender detection

Header parsing

Phishing ML classifier

Domain age lookup

🔥 3. Threat Intelligence Integration

VirusTotal

AbuseIPDB

Shodan

GreyNoise

🔥 4. YARA-based Malware Analysis

Static malware signature scanning

Obfuscation detection

🔥 5. Authentication + Admin Role Panel

Secure login

API keys

Protected dashboards

⭐ Author

👩‍💻 Anamika Yadav
CSE Student | Cybersecurity & AI Enthusiast
