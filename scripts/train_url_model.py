import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score
from url_features import extract_url_features

print("✅ Step 1: Starting script...")

# Load dataset
try:
    df = pd.read_csv('../data/urls.csv')

    print("✅ Step 2: Dataset loaded successfully.")
    print("Dataset shape:", df.shape)
    print("Columns:", df.columns.tolist())
except Exception as e:
    print("❌ Error loading dataset:", e)
    exit()

# Drop missing values and sample
try:
    df = df.dropna().sample(10000, random_state=42)
    print("✅ Step 3: Dataset cleaned and sampled.")
except Exception as e:
    print("❌ Error cleaning dataset:", e)
    exit()

# Feature extraction
try:
    features = pd.DataFrame([extract_url_features(u) for u in df['url']])
    labels = df['type'].map({
        'benign': 0,
        'defacement': 1,
        'phishing': 1,
        'malware': 1
    })
    print("✅ Step 4: Feature extraction complete.")
except Exception as e:
    print("❌ Error extracting features:", e)
    exit()

# Train-test split
try:
    X_train, X_test, y_train, y_test = train_test_split(
        features, labels, test_size=0.2, stratify=labels, random_state=42
    )
    print("✅ Step 5: Train-test split done.")
except Exception as e:
    print("❌ Error splitting data:", e)
    exit()

# Train model
try:
    clf = RandomForestClassifier(n_estimators=150, random_state=42)
    clf.fit(X_train, y_train)
    print("✅ Step 6: Model training complete.")
except Exception as e:
    print("❌ Error training model:", e)
    exit()

# Evaluate
try:
    y_pred = clf.predict(X_test)
    roc_auc = roc_auc_score(y_test, clf.predict_proba(X_test)[:, 1])
    print("✅ Step 7: Evaluation complete.")
    print(classification_report(y_test, y_pred))
    print("ROC-AUC:", roc_auc)
except Exception as e:
    print("❌ Error evaluating model:", e)
    exit()

# Save model
try:
    joblib.dump(clf, '../models/url_model.joblib')
    print("✅ Step 8: Model saved successfully as url_model.joblib")
except Exception as e:
    print("❌ Error saving model:", e)
