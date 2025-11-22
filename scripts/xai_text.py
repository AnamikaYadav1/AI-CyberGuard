import numpy as np

def top_text_tokens(tfidf, model, text, top_n=8):
    """
    Return top influential tokens in a text sample based on model weights.
    Works best with linear models like Logistic Regression.
    """
    try:
        # Transform the text input using TF-IDF
        X = tfidf.transform([text])
        features = tfidf.get_feature_names_out()

        # Get model coefficients (feature weights)
        if hasattr(model, "coef_"):
            weights = model.coef_[0]
        else:
            return [("Model does not support feature importance", 0)]

        # Multiply each word's TF-IDF score by its model weight
        scores = X.toarray()[0] * weights

        # Sort by highest influence
        idx = np.argsort(scores)[::-1][:top_n]
        results = [(features[i], float(scores[i])) for i in idx if scores[i] != 0]

        return results if results else [("No influential words found", 0)]

    except Exception as e:
        print(f"[ERROR] Error in text explainability: {e}")
        return [("Explainability error", 0)]
"""# Example usage
if __name__ == "__main__":
    # Load model and vectorizer
    base_path = os.path.dirname(os.path.abspath(__file__))
    model = joblib.load(os.path.join(base_path, '..', 'models', 'text_model.joblib'))
    tfidf = joblib.load(os.path.join(base_path, '..', 'models', 'tfidf_vectorizer.joblib'))

    # Sample text for explanation
    sample_text = "You are such a loser and nobody likes you."

    explanations = top_text_tokens(tfidf, model, sample_text)
    print(f"Top influential tokens for the sample text:\n")
    for token, value in explanations:
        print(f"{token}: {value}")
"""
