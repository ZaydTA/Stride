import streamlit as st
from openai import OpenAI

# --- Config ---
st.set_page_config(page_title="Stride AI v4", layout="centered")
st.title("🧓 Stride AI v4 – Advanced Personalized Fitness Plan")

if "step" not in st.session_state:
    st.session_state.step = 0
if "responses" not in st.session_state:
    st.session_state.responses = {}
if "complete" not in st.session_state:
    st.session_state.complete = False
if "summary_ready" not in st.session_state:
    st.session_state.summary_ready = False

client = None
if "OPENAI_API_KEY" in st.secrets:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# --- Question List (30+ modular questions) ---
questions = [
    {"key": "balance_issues", "text": "Do you have difficulty balancing?", "type": "checkbox"},
    {"key": "joint_pain", "text": "Do you experience joint pain or arthritis?", "type": "checkbox"},
    {"key": "stairs", "text": "Can you comfortably walk up stairs?", "type": "select", "options": ["Yes", "With difficulty", "No"]},
    {"key": "fatigue", "text": "Do you get tired easily during the day?", "type": "checkbox"},
    {"key": "goal", "text": "What is your top health goal?", "type": "text"},
    {"key": "daily_activity", "text": "How many minutes of activity do you get daily?", "type": "slider", "min": 0, "max": 120, "default": 20},
    {"key": "shoulder_pain", "text": "Do you experience shoulder stiffness or pain?", "type": "checkbox"},
    {"key": "grip_strength", "text": "Do you struggle opening jars or holding items?", "type": "checkbox"},
    {"key": "age", "text": "What is your age?", "type": "slider", "min": 55, "max": 95, "default": 70},
    {"key": "energy_level", "text": "How is your energy level most days?", "type": "select", "options": ["Low", "Moderate", "High"]},
    {"key": "fall_history", "text": "Have you fallen in the past 6 months?", "type": "checkbox"},
    {"key": "back_pain", "text": "Do you experience back discomfort?", "type": "checkbox"},
    {"key": "flexibility", "text": "Can you touch your toes comfortably?", "type": "select", "options": ["Yes", "Somewhat", "No"]},
    {"key": "mobility_aid", "text": "Do you use a cane, walker, or aid?", "type": "checkbox"},
    {"key": "preferred_time", "text": "What time of day do you prefer to exercise?", "type": "select", "options": ["Morning", "Afternoon", "Evening"]},
    {"key": "stress", "text": "Do you feel mentally stressed?", "type": "checkbox"},
    {"key": "sleep_quality", "text": "How well do you sleep?", "type": "select", "options": ["Poorly", "Average", "Well"]},
    {"key": "injuries", "text": "List any past injuries or surgeries.", "type": "text"},
    {"key": "walk_time", "text": "How many minutes can you walk comfortably?", "type": "slider", "min": 0, "max": 60, "default": 15},
    {"key": "confidence", "text": "How confident do you feel exercising alone?", "type": "select", "options": ["Very confident", "Somewhat", "Not confident"]},
    {"key": "arm_raise", "text": "Can you lift your arms above your head?", "type": "checkbox"},
    {"key": "difficulty_bending", "text": "Do you struggle with bending down?", "type": "checkbox"},
    {"key": "motivation", "text": "What motivates you to stay active?", "type": "text"},
    {"key": "medical_conditions", "text": "Do you have any diagnosed medical conditions?", "type": "text"},
    {"key": "comfort_group", "text": "Do you prefer group or solo workouts?", "type": "select", "options": ["Group", "Solo", "Either"]},
    {"key": "leg_strength", "text": "Can you stand from a chair without using arms?", "type": "select", "options": ["Yes", "Sometimes", "No"]},
    {"key": "stairs_frequency", "text": "How often do you use stairs daily?", "type": "slider", "min": 0, "max": 20, "default": 5},
    {"key": "ankle_pain", "text": "Do you have ankle or foot discomfort?", "type": "checkbox"},
    {"key": "hearing_issues", "text": "Do you have difficulty hearing instructions clearly?", "type": "checkbox"},
    {"key": "vision_issues", "text": "Do you have impaired vision?", "type": "checkbox"},
]

# --- Survey Engine ---
def survey_engine():
    i = st.session_state.step
    q = questions[i]
    st.markdown(f"**Question {i+1} of {len(questions)}**")

    if q["type"] == "checkbox":
        ans = st.checkbox(q["text"], value=st.session_state.responses.get(q["key"], False))
    elif q["type"] == "slider":
        ans = st.slider(q["text"], q["min"], q["max"], q["default"])
    elif q["type"] == "select":
        default = st.session_state.responses.get(q["key"], q["options"][0])
        ans = st.selectbox(q["text"], q["options"], index=q["options"].index(default))
    elif q["type"] == "text":
        ans = st.text_input(q["text"], value=st.session_state.responses.get(q["key"], ""))

    st.session_state.responses[q["key"]] = ans

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("⬅️ Back", disabled=i == 0):
            st.session_state.step -= 1
            st.experimental_rerun()
    with col2:
        if st.button("Next ➡️"):
            if i + 1 < len(questions):
                st.session_state.step += 1
                st.experimental_rerun()
            else:
                st.session_state.summary_ready = True
                st.experimental_rerun()

# --- Summary Screen ---
def show_summary():
    st.subheader("📋 Review Your Answers")
    for q in questions:
        st.write(f"**{q['text']}**")
        st.write(f"➡️ {st.session_state.responses[q['key']]}")
        st.markdown("---")
    if st.button("✅ Generate My Exercise Plan"):
        st.session_state.complete = True
        st.experimental_rerun()
    if st.button("🔙 Go Back"):
        st.session_state.summary_ready = False
        st.session_state.step = len(questions) - 1
        st.experimental_rerun()

# --- Exercise Plan Generator ---
def show_recommendations():
    st.subheader("🎯 Your Personalized Exercise Plan")
    r = st.session_state.responses
    recs = []

    if r.get("balance_issues"):
        recs.append(("Chair Marches", "Improves balance and coordination", "https://youtu.be/6oL2sy-il6Y"))
    if r.get("joint_pain"):
        recs.append(("Wall Push-Ups", "Strengthens upper body with low joint stress", "https://youtu.be/0KNAwCGGzIE"))
    if r.get("daily_activity", 0) < 15:
        recs.append(("Seated Toe Taps", "Boosts circulation gently", "https://youtu.be/UvVZHLi4Gz0"))
    if r.get("goal", "").lower().find("strength") >= 0:
        recs.append(("Sit-to-Stand", "Builds lower body power", "https://youtu.be/o1ZLcg9Y_Do"))
    if r.get("shoulder_pain"):
        recs.append(("Arm Circles", "Increases shoulder mobility", "https://youtu.be/nq0N_j2XMQw"))

    recs = recs[:5]

    for name, desc, yt in recs:
        st.markdown(f"### 🏋️ {name}")
        st.caption(desc)
        st.video(yt)
        if client:
            try:
                img = client.images.generate(
                    model="dall-e-3",
                    prompt=f"An elderly person doing {name} indoors, safe, bright lighting",
                    n=1,
                    size="1024x1024"
                )
                st.image(img.data[0].url, caption=name)
            except Exception as e:
                st.warning(f"Image error: {e}")

# --- Flow Control ---
if not st.session_state.summary_ready and not st.session_state.complete:
    survey_engine()
elif st.session_state.summary_ready and not st.session_state.complete:
    show_summary()
else:
    show_recommendations()
