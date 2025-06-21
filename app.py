import streamlit as st
from openai import OpenAI

# --- CONFIG ---
questions = [
    {
        "text": "Do you have difficulty balancing while standing or walking?",
        "type": "checkbox",
        "label": "Balance Issues",
        "key": "balance"
    },
    {
        "text": "How much time do you spend walking daily?",
        "type": "slider",
        "label": "Minutes of walking",
        "min": 0,
        "max": 60,
        "default": 10,
        "key": "walk_time"
    },
    {
        "text": "How would you rate your general activity level?",
        "type": "select",
        "label": "Activity Level",
        "options": ["Low", "Moderate", "High"],
        "key": "activity"
    },
    {
        "text": "Do you experience any joint pain or stiffness?",
        "type": "checkbox",
        "label": "Joint Pain",
        "key": "joint_pain"
    },
    {
        "text": "What is your primary fitness goal?",
        "type": "text",
        "label": "Goal",
        "key": "goal"
    }
]

# --- SURVEY FUNCTION ---
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

# --- EXERCISE RECOMMENDER ---
def get_exercises(responses):
    recs = []
    if responses.get("balance"):
        recs.append({"name": "Chair Marches", "description": "Improves balance", "youtube": "https://youtu.be/6oL2sy-il6Y"})
    if responses.get("joint_pain"):
        recs.append({"name": "Wall Push-Ups", "description": "Low-impact strength", "youtube": "https://youtu.be/0KNAwCGGzIE"})
    if responses.get("walk_time", 0) < 15:
        recs.append({"name": "Seated Toe Taps", "description": "Light cardio", "youtube": "https://youtu.be/UvVZHLi4Gz0"})
    if responses.get("activity") == "Low":
        recs.append({"name": "Arm Circles", "description": "Boosts shoulder mobility", "youtube": "https://youtu.be/nq0N_j2XMQw"})
    if "goal" in responses and "strength" in responses["goal"].lower():
        recs.append({"name": "Sit-to-Stand", "description": "Leg strength & control", "youtube": "https://youtu.be/o1ZLcg9Y_Do"})
    return recs

# --- MAIN APP ---
st.set_page_config(page_title="Stride AI", layout="centered")
st.title("🧓 Stride AI: Personalized Exercises for Older Adults")
st.markdown("Answer personalized questions and get 5 research-backed exercises!")

if 'survey_complete' not in st.session_state:
    st.session_state.survey_complete = False

if not st.session_state.survey_complete:
    run_survey()
else:
    st.subheader("🧠 AI-Powered Exercise Plan")
    responses = st.session_state.responses
    exercises = get_exercises(responses)[:5]

    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    for ex in exercises:
        name, desc, yt_link = ex['name'], ex['description'], ex['youtube']
        st.markdown(f"### 🏋️ {name}")
        st.caption(desc)
        st.video(yt_link)

        try:
            response = client.images.generate(
                model="dall-e-3",
                prompt=f"An elderly person doing {name}, safe indoor setting",
                n=1,
                size="1024x1024"
            )
            url = response.data[0].url
            if url:
                st.image(url)
        except Exception as e:
            st.warning(f"Image error: {e}")
