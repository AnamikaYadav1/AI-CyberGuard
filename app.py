import streamlit as st
import joblib
import pandas as pd
import os

# Import feature extractors and XAI functions
from scripts.url_features import extract_url_features
from scripts.xai_url import explain_url
from scripts.xai_text import top_text_tokens

# ----------------------------
# Load models safely
# ----------------------------
base_path = os.path.dirname(os.path.abspath(__file__))
models_path = os.path.join(base_path, "models")

try:
    url_model = joblib.load(os.path.join(models_path, "url_model.joblib"))
    text_model = joblib.load(os.path.join(models_path, "text_model.joblib"))
    tfidf = joblib.load(os.path.join(models_path, "tfidf_vectorizer.joblib"))
except Exception as e:
    st.error(f"❌ Error loading models: {e}")
    st.stop()

# ----------------------------
# Streamlit UI setup
# ----------------------------
st.set_page_config(page_title="AI Cyber Threat & Abuse Detector", page_icon="🛡️", layout="wide")
st.title("🧠 AI Cyber Threat & Abuse Detection System")
st.markdown("Detect **malicious URLs** and **cyberbullying content** with AI + Explainable Insights.")

# Tabs for two modules
tab1, tab2 = st.tabs(["🔗 URL Scanner", "💬 Text Analyzer"])

# ----------------------------
# URL SCANNER TAB
# ----------------------------
with tab1:
    st.subheader("🔗 Malicious URL Detection")
    url = st.text_input("Enter a URL to check:")

    if st.button("Scan URL"):
        if url.strip():
            feats = extract_url_features(url)
            df = pd.DataFrame([feats])
            prob = url_model.predict_proba(df)[0][1]
            label = "⚠️ Malicious" if prob > 0.5 else "✅ Safe"
            color = "red" if prob > 0.5 else "green"
            st.markdown(f"<h3 style='color:{color}'>{label} (Confidence: {prob:.2f})</h3>", unsafe_allow_html=True)

            # --- Explainability section ---
            st.write("### 🔍 Why this prediction?")
            with st.spinner("Analyzing model explanation..."):
                explanation = explain_url(url)
                for feature, value in explanation:
                    st.write(f"- **{feature}** → {value:.4f}")

        else:
            st.warning("Please enter a URL first.")

# ----------------------------
# TEXT ANALYZER TAB
# ----------------------------
with tab2:
    st.subheader("💬 Cyberbullying Detection")
    text = st.text_area("Enter a comment or message:")

    if st.button("Analyze Text"):
        if text.strip():
            X = tfidf.transform([text])
            pred = text_model.predict(X)[0]
            if pred != "Safe":
                st.error(f"🚨 Cyberbullying Detected: **{pred}**")
            else:
                st.success("✅ No cyberbullying detected.")

            # --- Explainability section ---
            st.write("### 🧠 Top influential words:")
            with st.spinner("Analyzing text influence..."):
                tokens = top_text_tokens(tfidf, text_model, text)
                for word, val in tokens:
                    st.write(f"- {word} → {val:.4f}")

        else:
            st.warning("Please enter some text first.")
