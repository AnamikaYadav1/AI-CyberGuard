import os
import tweepy
import pandas as pd
import joblib
from dotenv import load_dotenv

load_dotenv()  # Load API keys

# Load model + vectorizer
base_path = os.path.dirname(os.path.abspath(__file__))
models_path = os.path.join(base_path, "..", "models")

text_model = joblib.load(os.path.join(models_path, "text_model.joblib"))
tfidf = joblib.load(os.path.join(models_path, "tfidf_vectorizer.joblib"))

# Authenticate Twitter API
bearer_token = os.getenv("TWITTER_BEARER")
client = tweepy.Client(bearer_token=bearer_token)


def analyze_twitter_user(username, limit=20):
    """
    Fetch recent tweets and classify cyberbullying or safe content.
    """
    try:
        # Get user ID from username
        user = client.get_user(username=username)
        if not user.data:
            return None, "❌ User not found"

        tweets = client.get_users_tweets(
            id=user.data.id,
            max_results=limit
        )
    except Exception as e:
        return None, f"❌ Error: {e}"

    results = []
    if tweets.data:
        for t in tweets.data:
            text = t.text
            X = tfidf.transform([text])
            pred = text_model.predict(X)[0]

            results.append({
                "Tweet": text,
                "Prediction": pred
            })

        df = pd.DataFrame(results)
        return df, None

    return None, "❌ No tweets found"
