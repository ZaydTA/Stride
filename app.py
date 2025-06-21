import streamlit as st
from openai import OpenAI

# Set up page
st.set_page_config(page_title="Stride AI", layout="centered")
st.title("🧓 Stride AI: Personalized Exercise Plan")
st.markdown("Answer this personalized survey to receive 5 expert-recommended exercises, complete with videos and AI-generated images.")

# Initialize state
if "q_index" not in st.session_state:
    st.session_state.q_index = 0
if "responses" not in st.session_state:
    st.session_state.responses = {}
if "completed" not in st.session_state:
    st.session_state.completed = False

# OpenAI client setup
if "OPENAI_API_KEY" in st.secrets:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
else:
    st.error("No API key found. Add your OPENAI_API_KEY in Streamlit secrets.")

# Survey questions (grouped and labeled)
questions = [
    {"key": "balance", "text": "Do you have difficulty maintaining balance?", "type": "checkbox"},
    {"key": "joint_pain", "text": "Do you experience joint pain?", "type": "checkbox"},
    {"key": "mobility_level", "text": "How would you rate your mobility?", "type": "select", "options": ["Low", "Medium", "High"]},
    {"key": "fatigue", "text": "Do you feel tired after light activities?", "type": "checkbox"},
    {"key": "stairs", "text": "Can you comfortably climb stairs?", "type": "select", "options": ["Yes", "With effort", "No"]},
    {"key": "goal", "text": "What is your top health goal?", "type": "text"},
    {"key": "activity_minutes", "text": "How many minutes of activity do you get daily?", "type": "slider", "min": 0, "max": 120, "default": 30},
    {"key": "shoulder_pain", "text": "Do you experience shoulder stiffness or pain?", "type": "checkbox"},
    {"key": "previous_injuries", "text": "Do you have any past injuries?", "type": "text"},
    {"key": "energy_level", "text": "How is your energy during the day?", "type": "select", "options": ["Low", "Normal", "High"]},
]

# Render one question at a time
def render_question():
    i = st.session_state.q_index
    q = questions[i]
    st.markdown(f"**Question {i+1} of {len(questions)}**")

    if q["type"] == "checkbox":
        response = st.checkbox(q["text"], value=st.session_state.responses.get(q["key"], False))
    elif q["type"] == "slider":
        response = st.slider(q["text"], q["min"], q["max"], q["default"])
    elif q["type"] == "select":
        response = st.selectbox(q["text"], q["options"], index=q["options"].index(st.session_state.responses.get(q["key"], q["options"][0])))
    elif q["type"] == "text":
        response = st.text_input(q["text"], value=st.session_state.responses.get(q["key"], ""))

    st.session_state.responses[q["key"]] = response

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("⬅️ Back", disabled=i == 0):
            st.session_state.q_index -= 1
            st.experimental_rerun()
    with col2:
        if st.button("Next ➡️"):
            if i + 1 < len(questions):
                st.session_state.q_index += 1
                st.experimental_rerun()
            else:
                st.session_state.completed = True
                st.experimental_rerun()

# Recommendation logic
def recommend_exercises():
    data = st.session_state.responses
    recs = []

    if data.get("balance"):
        recs.append(("Chair Marches", "Improves coordination and balance", "https://youtu.be/6oL2sy-il6Y"))
    if data.get("joint_pain"):
        recs.append(("Wall Push-Ups", "Gentle strength-building for joints", "https://youtu.be/0KNAwCGGzIE"))
    if data.get("activity_minutes", 0) < 20:
        recs.append(("Seated Toe Taps", "Light cardio to stay active", "https://youtu.be/UvVZHLi4Gz0"))
    if "strength" in data.get("goal", "").lower():
        recs.append(("Sit-to-Stand", "Builds lower body strength", "https://youtu.be/o1ZLcg9Y_Do"))
    if data.get("shoulder_pain"):
        recs.append(("Arm Circles", "Improves shoulder mobility", "https://youtu.be/nq0N_j2XMQw"))

    return recs[:5]

# Display final result
def display_results():
    st.subheader("🎯 Your Personalized Exercise Plan")
    exercises = recommend_exercises()

    for name, desc, yt in exercises:
        st.markdown(f"### 🏋️ {name}")
        st.caption(desc)
        st.video(yt)

        with st.spinner("Generating image..."):
            try:
                result = client.images.generate(
                    model="dall-e-3",
                    prompt=f"An elderly person doing {name} indoors with good lighting",
                    n=1,
                    size="1024x1024"
                )
                st.image(result.data[0].url, caption=name)
            except Exception as e:
                st.warning(f"Could not generate image: {e}")

# Run the app flow
if not st.session_state.completed:
    render_question()
else:
    display_results()
