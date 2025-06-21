import streamlit as st
from openai import OpenAI

# --- Setup ---
st.set_page_config(page_title="Stride AI", layout="centered")
st.title("🧓 Stride AI: Personalized Longevity Builder")
st.markdown("Answer a few quick questions to get your custom daily micro-habit workout plan!")

# --- Initialize session state ---
if "responses" not in st.session_state:
    st.session_state.responses = {}
    st.session_state.q_index = 0
    st.session_state.survey_complete = False

# --- Questions Configuration ---
questions = [
    {"key": "balance", "text": "Do you have difficulty balancing while standing?", "type": "checkbox"},
    {"key": "joint_pain", "text": "Do you experience joint pain when walking or standing?", "type": "checkbox"},
    {"key": "stairs", "text": "Can you comfortably climb stairs without stopping?", "type": "checkbox"},
    {"key": "goal", "text": "What's your primary goal with Stride?", "type": "select", "options": ["Improve Balance", "Get Stronger", "Prevent Falls", "Move More Daily", "Feel Better"]},
    {"key": "walk_time", "text": "How many minutes do you walk daily?", "type": "slider", "min": 0, "max": 120, "default": 15},
    {"key": "mobility_input", "text": "Tell us briefly about your mobility or past injuries (optional):", "type": "text"},
]

# --- Survey Logic ---
if not st.session_state.survey_complete:
    idx = st.session_state.q_index

    if idx < len(questions):
        q = questions[idx]
        st.subheader(f"{idx + 1}. {q['text']}")

        input_key = f"input_{idx}"
        response = None

        if q['type'] == 'checkbox':
            response = st.checkbox("Yes", key=input_key)
        elif q['type'] == 'slider':
            response = st.slider(q['text'], q['min'], q['max'], q['default'], key=input_key)
        elif q['type'] == 'select':
            response = st.selectbox(q['text'], q['options'], key=input_key)
        elif q['type'] == 'text':
            response = st.text_area(q['text'], key=input_key)

        if st.button("Next"):
            st.session_state.responses[q['key']] = response
            st.session_state.q_index += 1
            st.experimental_rerun()
    else:
        if st.button("Submit Survey"):
            st.session_state.survey_complete = True
            st.experimental_rerun()

# --- Recommendation Display ---
else:
    st.subheader("🧠 Your Personalized Longevity Plan")
    responses = st.session_state.responses

    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    # --- Simple Recommendation Logic (Demo) ---
    exercises = []

    if responses.get("balance"):
        exercises.append(("Chair Marches", "Improves coordination and balance.", "https://youtu.be/6oL2sy-il6Y"))
    if responses.get("joint_pain"):
        exercises.append(("Wall Push-Ups", "Low-impact upper-body strength.", "https://youtu.be/0KNAwCGGzIE"))
    if responses.get("walk_time", 0) < 15:
        exercises.append(("Toe Taps", "Boosts circulation and activity.", "https://youtu.be/UvVZHLi4Gz0"))
    if "stronger" in responses.get("goal", "").lower():
        exercises.append(("Sit-to-Stand", "Trains leg strength and control.", "https://youtu.be/o1ZLcg9Y_Do"))
    if "fall" in responses.get("goal", "").lower():
        exercises.append(("Balance Hold", "Improves control and reduces fall risk.", "https://youtu.be/nq0N_j2XMQw"))

    selected = exercises[:5]

    for name, desc, yt in selected:
        st.markdown(f"### 🏋️ {name}")
        st.caption(desc)
        st.video(yt)

        prompt = f"An elderly person doing {name}, safe home setting, daylight, gentle pose"
        try:
            img = client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                n=1,
                size="512x512"
            )
            st.image(img.data[0].url, caption=f"{name} Illustration")
        except Exception as e:
            st.warning(f"Image failed: {e}")

    st.success("Want to redo your quiz? Refresh the page.")
