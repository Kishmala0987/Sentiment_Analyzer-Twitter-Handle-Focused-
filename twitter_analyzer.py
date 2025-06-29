import streamlit as st
import tweepy
import re
import matplotlib.pyplot as plt
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

st.title("Twitter Sentiment Analyzer")
st.write("Enter a Twitter handle to analyze sentiment and predict personality based on recent tweets (English only).")
username = st.text_input("Enter Twitter handle (without @):")

analyzer = SentimentIntensityAnalyzer()

def clean_text(text):
    text = re.sub(r"http\S+|@\S+|#\S+", "", text)
    text = re.sub(r"[^\w\s]", "", text)
    return text.strip()

def classify_sentiment(score):
    if score['compound'] >= 0.05:
        return 'positive'
    elif score['compound'] <= -0.05:
        return 'negative'
    else:
        return 'neutral'

client = tweepy.Client(bearer_token='AAAAAAAAAAAAAAAAAAAAAALG2AEAAAAA%2BsP7MbtBjuk%2Fy6Nu5SKw4XrFfFU%3D4SrNOUPW8mb9Q1lC4o3CEZn19cu5lvCIS0g9RMtvvLINiZxDjN')  # replace with your token
if username:
    try:
        user_data = client.get_user(username=username)
        user_id = user_data.data.id

        tweets_response = client.get_users_tweets(id=user_id, max_results=30)

        if not tweets_response.data:
            st.warning("No tweets found.")
        else:
            sentiment_counts = {"positive": 0, "neutral": 0, "negative": 0}

            for tweet in tweets_response.data:
                text = tweet.text
                cleaned = clean_text(text)
                if cleaned:
                    sentiment = analyzer.polarity_scores(cleaned)
                    sentiment_type = classify_sentiment(sentiment)
                    sentiment_counts[sentiment_type] += 1

            total = sum(sentiment_counts.values())
            st.subheader(f"Sentiment Analysis for @{username}")
            st.markdown(f"*Total Tweets Analyzed:* {total}")

            col1, col2, col3 = st.columns(3)
            col1.metric("😊 Positive", sentiment_counts["positive"])
            col2.metric("😐 Neutral", sentiment_counts["neutral"])
            col3.metric("😠 Negative", sentiment_counts["negative"])

            st.subheader("Sentiment Distribution")
            fig, ax = plt.subplots()
            labels = sentiment_counts.keys()
            sizes = sentiment_counts.values()
            colors = ['#66b3ff', '#ffcc99', '#ff9999']
            ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=colors)
            ax.axis('equal')
            st.pyplot(fig)

            pos = sentiment_counts['positive']
            neu = sentiment_counts['neutral']
            neg = sentiment_counts['negative']

            if pos > neg and pos > neu:
                personality = "Optimistic & Uplifting"
            elif neg > pos and neg > neu:
                personality = "Critical or Concerned"
            elif neu > pos and neu > neg:
                personality = "Reserved or Informative"
            else:
                personality = "Expressive or Emotional"

            st.subheader("Predicted Personality Type")
            st.success(f"🎭 {personality}")

    except tweepy.TweepyException as e:
        st.warning("Try again after 15 minutes, or use paid API")
    except Exception as e:
        st.error(f"General Error: {e}")
