# app.py (Landing Page)
import streamlit as st

st.set_page_config(page_title="🏠 Home", layout="centered")

st.title("🏋️ Hevy Streamlit App")
st.markdown("Welcome! Select a page below to continue:")

pages = {
    "🏋️ Workout Dashboard": "pages/workout_dashboard.py",
    "📈 Another Page": "pages/another_page.py",
}

for label, path in pages.items():
    if st.button(label):
        st.switch_page(path)
