import streamlit as st
import nltk
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt

nltk.download('vader_lexicon', quiet=True)
sia = SentimentIntensityAnalyzer()
st.markdown("""
    <style>
    .main {
        background-color: #f9f9f9;
    }
    .stTextArea textarea {
        font-size: 1rem;
        border-radius: 0.5rem;
    }
    .stButton button {
        background-color: #4CAF50;
        color: white;
        border-radius: 0.4rem;
        font-weight: bold;
    }
    .stButton button:hover {
        background-color: #45a049;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>💬 Real-Time Sentiment Analyzer</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #6c757d;'>Analyze the mood of your message using NLTK's VADER model.</p>", unsafe_allow_html=True)
tab1, tab2 = st.tabs(["✍️ Single Text", "📝 Batch Input"])
with tab1:
    st.markdown("### ✍️ Enter your text below:")
    user_input = st.text_area("", height=200, placeholder="Type something meaningful...")

    if st.button("🔍 Analyze Sentiment", key="single"):
        if not user_input.strip():
            st.warning("⚠️ Please enter some text to analyze.")
        else:
            score = sia.polarity_scores(user_input)
            compound = score['compound']

            if compound >= 0.05:
                sentiment = "Positive 😊"
                color = "green"
            elif compound <= -0.05:
                sentiment = "Negative 😞"
                color = "red"
            else:
                sentiment = "Neutral 😐"
                color = "gray"

            st.markdown(f"<h3 style='color: {color};'>Sentiment: {sentiment}</h3>", unsafe_allow_html=True)

            st.markdown("#### 📊 Confidence Scores:")
            labels = ['Positive', 'Neutral', 'Negative']
            values = [score['pos'], score['neu'], score['neg']]
            fig, ax = plt.subplots(figsize=(5, 1.8))
            ax.barh(labels, values, color=['green', 'gray', 'red'])
            ax.set_xlim(0, 1)
            ax.set_xlabel("Score")
            ax.set_title("VADER Sentiment Breakdown", fontsize=10)
            st.pyplot(fig)

            st.markdown("#### 🧪 Raw VADER Scores:")
            st.json(score)
with tab2:
    st.markdown("### 📝 Enter multiple lines of text (one review per line):")
    batch_input = st.text_area(
        "",
        height=200,
        placeholder="Example:\nI loved the movie!\nThe product was okay.\nTerrible service."
    )

    st.markdown("### 📂 Or upload a CSV or TXT file:")
    uploaded_file = st.file_uploader("Upload CSV or TXT file", type=['csv', 'txt'])

    reviews = []

    if uploaded_file:
        if uploaded_file.type == 'text/plain':
            content = uploaded_file.read().decode("utf-8")
            reviews = [line.strip() for line in content.split('\n') if line.strip()]
        elif uploaded_file.type == 'text/csv':
            df_uploaded = pd.read_csv(uploaded_file)
            if len(df_uploaded.columns) == 1:
                reviews = df_uploaded.iloc[:, 0].dropna().tolist()
            else:
                st.warning("⚠️ CSV should contain only one column with text data.")
    else:
        if batch_input.strip():
            reviews = [line.strip() for line in batch_input.split('\n') if line.strip()]

    if st.button("🔍 Analyze Batch Sentiments", key="batch"):
        if not reviews:
            st.warning("⚠️ Please enter or upload at least one line of text.")
        else:
            sentiments = []
            compounds = []
            pos_scores = []
            neu_scores = []
            neg_scores = []

            for text in reviews:
                score = sia.polarity_scores(text)
                compound = score['compound']

                if compound >= 0.05:
                    sentiment = "Positive 😊"
                elif compound <= -0.05:
                    sentiment = "Negative 😞"
                else:
                    sentiment = "Neutral 😐"

                sentiments.append(sentiment)
                compounds.append(compound)
                pos_scores.append(score['pos'])
                neu_scores.append(score['neu'])
                neg_scores.append(score['neg'])

            df = pd.DataFrame({
                "Text": reviews,
                "Sentiment": sentiments,
                "Compound Score": compounds,
                "Positive": pos_scores,
                "Neutral": neu_scores,
                "Negative": neg_scores
            })

            st.markdown("### 📝 Sentiment Analysis Results:")
            st.dataframe(df.style.applymap(
                lambda val: 'background-color: lightgreen' if 'Positive' in str(val)
                else 'background-color: salmon' if 'Negative' in str(val)
                else 'background-color: lightgray' if 'Neutral' in str(val)
                else '', subset=['Sentiment']
            ))
            st.download_button(
                label="💾 Download Results as CSV",
                data=df.to_csv(index=False),
                file_name="sentiment_results.csv",
                mime="text/csv"
            )

st.markdown("---")
st.markdown("<div style='text-align: center; color: #999;'>Made By Kishmala,Faiza,Aeshah</div>", unsafe_allow_html=True)