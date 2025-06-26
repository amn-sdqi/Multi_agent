# summarize.py
from collections import Counter

def summarize_results(results):
    sentiments = [r["Sentiment"]["label"] for r in results]
    emotions = [r["Emotion"]["label"] for r in results]

    sentiment_counts = Counter(sentiments)
    emotion_counts = Counter(emotions)

    total = len(results)
    pos_pct = (sentiment_counts.get("POSITIVE", 0) / total) * 100
    neg_pct = (sentiment_counts.get("NEGATIVE", 0) / total) * 100
    top_emotion = emotion_counts.most_common(1)[0][0]

    return {
        "positive_percent": round(pos_pct, 2),
        "negative_percent": round(neg_pct, 2),
        "dominant_emotion": top_emotion,
    }
