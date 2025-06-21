import streamlit as st
from .survey import run_survey
from .recommend import generate_recommendations

st.set_page_config(page_title="Stride AI", layout="centered")
st.title("🧓 Stride AI: Personalized Exercises for Older Adults")
st.markdown("Answer personalized questions and get 5 research-backed exercises!")

if 'survey_complete' not in st.session_state:
    st.session_state.survey_complete = False

if not st.session_state.survey_complete:
    run_survey()
else:
    generate_recommendations()

