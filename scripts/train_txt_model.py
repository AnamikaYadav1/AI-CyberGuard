import pandas as pd
import joblib
import nltk
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score
import os

# Download NLTK stopwords
nltk.download('stopwords')

print("✅ Step 1: Loading dataset...")

base_path = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(base_path, '..', 'data', 'cyberbullying.csv')

df = pd.read_csv(data_path)
print("Columns:", df.columns.tolist())
print("Dataset shape:", df.shape)

# keep relevant columns
df = df[['tweet_text', 'cyberbullying_type']].dropna()
df['cyberbullying_type'] = df['cyberbullying_type'].replace(
    {'not_cyberbullying': 'Safe'}
)

print("✅ Step 2: Cleaning and preparing data...")

X_train, X_test, y_train, y_test = train_test_split(
    df['tweet_text'], df['cyberbullying_type'],
    test_size=0.2, stratify=df['cyberbullying_type'], random_state=42
)

print("✅ Step 3: Vectorizing text...")
tfidf = TfidfVectorizer(max_features=5000, stop_words='english')
X_train_tfidf = tfidf.fit_transform(X_train)
X_test_tfidf = tfidf.transform(X_test)

print("✅ Step 4: Training Logistic Regression model...")
model = LogisticRegression(max_iter=500)
model.fit(X_train_tfidf, y_train)

print("✅ Step 5: Evaluating model...")
preds = model.predict(X_test_tfidf)
print(classification_report(y_test, preds))
print("Accuracy:", accuracy_score(y_test, preds))

print("✅ Step 6: Saving model and vectorizer...")
joblib.dump(model, os.path.join(base_path, '..', 'models', 'text_model.joblib'))
joblib.dump(tfidf, os.path.join(base_path, '..', 'models', 'tfidf_vectorizer.joblib'))

print("✅ Model training complete and saved in /models folder.")
