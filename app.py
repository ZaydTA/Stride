import streamlit as st
from openai import OpenAI

# Set up your app
st.set_page_config(page_title="Stride AI", layout="centered")
st.title("🧓 Stride AI: Personalized Exercises for Older Adults")
st.markdown("Answer a few questions and get 5 custom exercises with AI-generated images!")

# Load your OpenAI API key from Streamlit secrets
if "OPENAI_API_KEY" not in st.secrets:
    st.error("API key not found in secrets. Please add OPENAI_API_KEY.")
else:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

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
    q10 = st.slider("How many minutes of physical activity do you get per day?", 0, 120, 30)

    if st.button("Generate My Exercises"):
        st.markdown("---")
        st.subheader("🧠 AI-Powered Results")

        responses = {
            "balance": q1,
            "joint_pain": q2,
            "breath": q3,
            "chair_stand": not q4,
            "grip": q5,
            "tired": q6,
            "stiff": q7,
            "shoulders": not q8,
            "injury": q9,
            "low_activity": q10 < 30
        }

        # Recommendation Logic
        exercises = []

        if responses["balance"]:
            exercises.append(("Chair Marches", "Improves coordination and balance."))
        if responses["joint_pain"]:
            exercises.append(("Wall Push-Ups", "Gentle upper-body strength without joint strain."))
        if responses["grip"]:
            exercises.append(("Towel Squeeze", "Boosts grip strength and forearm control."))
        if responses["chair_stand"]:
            exercises.append(("Sit-to-Stand", "Trains leg strength for daily mobility."))
        if responses["low_activity"]:
            exercises.append(("Seated Toe Taps", "Light cardio to build movement endurance."))
        if responses["stiff"]:
            exercises.append(("Neck Rotations", "Relieves stiffness in upper spine."))
        if responses["shoulders"]:
            exercises.append(("Arm Circles", "Improves shoulder mobility and control."))

        selected = exercises[:5]

        # Generate AI Images
        for name, desc in selected:
            st.markdown(f"### 🏋️ {name}")
            st.caption(desc)

            prompt = f"An elderly person doing {name}, realistic, safe indoor setting, natural lighting"

            with st.spinner("Generating image..."):
                try:
                    response = client.images.generate(
                        model="dall-e-3",
                        prompt=prompt,
                        n=1,
                        size="1024x1024"
                    )
                    image_url = response.data[0].url if response.data and response.data[0].url else None

                    if image_url:
                        st.image(image_url, caption=name)
                    else:
                        st.warning("Image URL was not returned. Try again or check your OpenAI usage limits.")
                except Exception as e:
                    st.error(f"Image generation failed: {e}")
