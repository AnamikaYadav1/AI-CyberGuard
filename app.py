import streamlit as st
import joblib
import pandas as pd
import os
import plotly.express as px

# -----------------------------
# Import your modules
# -----------------------------
from scripts.url_features import extract_url_features
from scripts.xai_url import explain_url
from scripts.xai_text import top_text_tokens
from scripts.fake_profile import heuristic_profile_score
from scripts.db_logger import log_scan, fetch_logs
from scripts.analytics import fetch_all_scans, summarize_data
from scripts.ids_engine import generate_fake_attack   # NEW IDS ENGINE
from scripts.ip_reputation import check_ip_reputation

# ------------------------------------------------------
# STREAMLIT CONFIG (always keep first)
# ------------------------------------------------------
st.set_page_config(
    page_title="AI Cyber Threat & Abuse Detector",
    page_icon="🛡️",
    layout="wide"
)

# ------------------------------------------------------
# LOAD MODELS
# ------------------------------------------------------
base_path = os.path.dirname(os.path.abspath(__file__))
models_path = os.path.join(base_path, "models")

try:
    url_model = joblib.load(os.path.join(models_path, "url_model.joblib"))
    text_model = joblib.load(os.path.join(models_path, "text_model.joblib"))
    tfidf = joblib.load(os.path.join(models_path, "tfidf_vectorizer.joblib"))
    print("✅ Model loaded successfully.")
except Exception as e:
    st.error(f"❌ Error loading models: {e}")
    st.stop()

# ------------------------------------------------------
# PAGE HEADER
# ------------------------------------------------------
st.title("🧠 AI Cyber Threat & Abuse Detection System")
st.markdown("Detect **malicious URLs**, **cyberbullying content**, **fake profiles**, and monitor **network intrusions**.")

# ------------------------------------------------------
# TABS (MUST come before using tab1)
# ------------------------------------------------------
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🔗 URL Scanner",
    "💬 Text Analyzer",
    "📊 Analytics Dashboard",
    "🕵️ Fake Profile Detector",
    "🛡️ Network IDS Monitor",
    "🌐 IP Reputation Checker"
])


# =====================================================
# 🔗 URL SCANNER TAB
# =====================================================
with tab1:
    st.subheader("🔗 Malicious URL Detection")

    url = st.text_input("Enter a URL to scan:")

    if st.button("Scan URL"):
        if url.strip():
            feats = extract_url_features(url)
            df = pd.DataFrame([feats])

            prob = url_model.predict_proba(df)[0][1]
            label = "⚠️ Malicious" if prob > 0.5 else "✅ Safe"
            color = "red" if prob > 0.5 else "green"

            st.markdown(
                f"<h3 style='color:{color}'>{label} (Confidence: {prob:.2f})</h3>",
                unsafe_allow_html=True
            )

            log_scan(
                scan_type="URL",
                input_data=url,
                result=label,
                confidence=float(prob)
            )

            st.write("### 🔍 Why did the model predict this?")
            with st.spinner("Analyzing features..."):
                explanation = explain_url(url)
                for feature, value in explanation:
                    st.write(f"- **{feature}** → {value:.4f}")
        else:
            st.warning("Please enter a URL first.")

# =====================================================
# 💬 TEXT ANALYZER TAB
# =====================================================
with tab2:
    st.subheader("💬 Cyberbullying Detection")

    text = st.text_area("Enter a message to analyze:")

    if st.button("Analyze Text"):
        if text.strip():
            X = tfidf.transform([text])
            pred = text_model.predict(X)[0]

            if pred != "Safe":
                st.error(f"🚨 Cyberbullying Detected: **{pred}**")
            else:
                st.success("✅ No cyberbullying detected.")

            log_scan(
                scan_type="Text",
                input_data=text,
                result=pred,
                confidence=0.0
            )

            st.write("### 🧠 Top Contributing Words")
            with st.spinner("Calculating influence..."):
                tokens = top_text_tokens(tfidf, text_model, text)
                for word, val in tokens:
                    st.write(f"- {word} → {val:.4f}")
        else:
            st.warning("Please enter some text.")

# =====================================================
# 📊 ANALYTICS DASHBOARD TAB
# =====================================================
with tab3:
    st.subheader("📊 Threat Analytics Dashboard")

    df = fetch_all_scans()

    if df.empty:
        st.info("No logs found — run a scan first.")
    else:
        st.write("### 📝 Recent Logs")
        st.dataframe(df, height=300)

        summary = summarize_data(df)

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Scans", summary["total"])
        col2.metric("Malicious / Toxic", summary["malicious"])
        col3.metric("Safe", summary["safe"])

        # Bar chart: scan types
        st.write("### 📌 Scan Type Distribution")
        fig = px.bar(
            df["type"].value_counts(),
            title="Scans per Category",
            labels={"value": "Count", "index": "Scan Type"}
        )
        st.plotly_chart(fig)

        # Pie chart: Safe vs Malicious
        st.write("### 🥧 Result Breakdown")
        fig2 = px.pie(
            df,
            names="result",
            title="Safe vs Malicious"
        )
        st.plotly_chart(fig2)

# =====================================================
# 🕵️ FAKE PROFILE DETECTOR TAB
# =====================================================
with tab4:
    st.subheader("🕵️ Fake Profile Detector")

    username = st.text_input("Username")
    created_at = st.date_input("Account Created On")
    followers = st.number_input("Followers", min_value=0)
    following = st.number_input("Following", min_value=0)
    posts = st.number_input("Posts", min_value=0)
    profile_image_default = st.checkbox("Default Profile Picture?")
    bio = st.text_area("Bio (Optional)")

    if st.button("Analyze Profile"):
        profile = {
            "username": username,
            "created_at": str(created_at),
            "followers": followers,
            "following": following,
            "posts": posts,
            "profile_image_default": profile_image_default,
            "bio": bio
        }

        score = heuristic_profile_score(profile)

        st.write("### 🔎 Fake Profile Likelihood")
        st.progress(score)

        if score >= 0.7:
            st.error(f"🚨 High Risk (Score: {score:.2f})")
        elif score >= 0.4:
            st.warning(f"⚠️ Suspicious (Score: {score:.2f})")
        else:
            st.success(f"✅ Likely Genuine (Score: {score:.2f})")

# =====================================================
# 🛡 NETWORK IDS MONITOR TAB — NEW
# =====================================================
with tab5:
    st.subheader("🛡 Real-Time Network Intrusion Detection System (IDS)")

    st.markdown("Simulate network attacks like **Port Scans, SQL Injection, Brute Force, Malware Downloads**, and more.")

    if st.button("🔥 Simulate Random Attack"):
        attack = generate_fake_attack()

        st.error(f"🚨 {attack['event']} detected from IP: {attack['source_ip']}")
        st.write(f"Timestamp: {attack['timestamp']}")

        log_scan(
            scan_type="IDS",
            input_data=attack["source_ip"],
            result=attack["event"],
            confidence=0.0
        )

    st.info("Live packet sniffing mode (with Scapy) will be added in next upgrade.")
# =====================================================
# 🌐 IP REPUTATION CHECKER
# =====================================================
with tab6:
    st.subheader("🌐 IP Reputation Checker (AbuseIPDB)")

    ip = st.text_input("Enter IP Address")

    if st.button("Check IP Reputation"):
        if ip.strip():
            with st.spinner("Checking IP reputation..."):
                data, error = check_ip_reputation(ip)

            if error:
                st.error(f"❌ Error: {error}")
            else:
                score = data.get("abuseConfidenceScore", 0)
                total_reports = data.get("totalReports", 0)
                country = data.get("countryCode", "Unknown")
                last_report = data.get("lastReportedAt", "N/A")

                # Classification
                if score >= 70:
                    st.error(f"🟥 HIGH RISK — Abuse Score: {score}")
                    result = "High-Risk IP"
                elif score >= 30:
                    st.warning(f"🟧 Suspicious IP — Abuse Score: {score}")
                    result = "Suspicious IP"
                else:
                    st.success(f"🟩 Clean IP — Abuse Score: {score}")
                    result = "Clean IP"

                # Show details
                st.write("### 📊 Details")
                st.write(f"- **Country:** {country}")
                st.write(f"- **Total Reports:** {total_reports}")
                st.write(f"- **Last Reported:** {last_report}")

                # Log into DB
                log_scan(
                    scan_type="IP Reputation",
                    input_data=ip,
                    result=result,
                    confidence=score
                )

        else:
            st.warning("Please enter an IP address.")
