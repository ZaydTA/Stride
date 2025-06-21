import streamlit as st
import openai

# Set up your app
st.set_page_config(page_title="Stride AI", layout="centered")
st.title("🧓 Stride AI: Personalized Exercises for Older Adults")
st.markdown("Answer a few questions and get 5 custom exercises with AI-generated images!")

# Load your OpenAI API key from Streamlit secrets
if "OPENAI_API_KEY" not in st.secrets:
    st.error("API key not found in secrets. Please add OPENAI_API_KEY.")
else:
    openai.api_key = st.secrets["OPENAI_API_KEY"]

    # Survey Questions
    q1 = st.checkbox("Do you have difficulty balancing while standing?")
    q2 = st.checkbox("Do you experience joint pain?")
    q3 = st.checkbox("Do you feel short of breath after short walks?")
    q4 = st.checkbox("Can you stand from a chair without using your hands?")
    q5 = st.checkbox("Do you struggle with grip strength (e.g. opening jars)?")
    q6 = st.checkbox("Do you get tired easily?")
    q7 = st.checkbox("Do you experience stiffness in the morning?")
    q8 = st.checkbox("Can you lift your arms above your head comfortably?")
    q9 = st.checkbox("Do you have any previous injuries?")
    q10 = st.slider("How m
