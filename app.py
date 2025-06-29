import streamlit as st

# App config
st.set_page_config(page_title="Sentiment Analyzer", page_icon="🧠", layout="centered")

st.title("🧠 Sentiment Analyzer Dashboard")
st.markdown("Choose the mode of sentiment analysis:")

# Option selector
choice = st.radio("🔍 Select a Mode", ["Analyze Custom Text", "Analyze Twitter Handle"])

# Route to respective module
if choice == "Analyze Custom Text":
    st.markdown("### ✍️ You chose to analyze your own text.")
    # Run text analyzer script
    with open("text_analyzer.py", encoding="utf-8") as f:
        exec(f.read())

elif choice == "Analyze Twitter Handle":
    st.markdown("### 🐦 You chose to analyze a Twitter handle.")
    # Run Twitter analyzer script
    with open("twitter_analyzer.py", encoding="utf-8") as f:
        exec(f.read())