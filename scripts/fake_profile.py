import re
from datetime import datetime, timedelta

def heuristic_profile_score(profile):
    score = 0.0

    # very new account
    try:
        created = datetime.fromisoformat(profile.get("created_at"))
        if created > datetime.now() - timedelta(days=30):
            score += 0.3
    except:
        pass

    # few followers
    if profile.get("followers", 0) < 10:
        score += 0.2

    # following >> followers
    if profile.get("followers", 1) < profile.get("following", 0) / 5:
        score += 0.15

    # default image
    if profile.get("profile_image_default"):
        score += 0.2

    # suspicious username
    if re.search(r'\d{4,}', profile.get("username", "")):
        score += 0.15

    return min(score, 1.0)
