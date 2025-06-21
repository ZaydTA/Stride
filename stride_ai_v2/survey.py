import streamlit as st
from .config import questions

def run_survey():
    if 'responses' not in st.session_state:
        st.session_state.responses = {}
        st.session_state.q_index = 0

    q_idx = st.session_state.q_index

    if q_idx < len(questions):
        q = questions[q_idx]
        st.subheader(f"{q_idx+1}. {q['text']}")

        input_key = f"input_{q_idx}"
        response = None

        if q['type'] == 'slider':
            response = st.slider(q['label'], q['min'], q['max'], q['default'], key=input_key)
        elif q['type'] == 'checkbox':
            response = st.checkbox(q['label'], key=input_key)
        elif q['type'] == 'text':
            response = st.text_input(q['label'], key=input_key)
        elif q['type'] == 'select':
            response = st.selectbox(q['label'], q['options'], key=input_key)

        if st.button("Next"):
            st.session_state.responses[q['key']] = response
            st.session_state.q_index += 1
            st.experimental_rerun()
    else:
        if st.button("Submit Survey"):
            st.session_state.survey_complete = True
            st.experimental_rerun()
