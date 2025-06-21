import streamlit as st
from .openai import OpenAI
from .utils import some_function

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def generate_recommendations():
    st.subheader("🧠 AI-Powered Exercise Plan")
    responses = st.session_state.responses
    exercises = get_exercises(responses)[:5]

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

