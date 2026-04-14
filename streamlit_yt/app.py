import google.generativeai as genai
import streamlit as st

st.title("MY BOT")

genai.configure(api_key="AIzaSyBguROzz2IjBrAUUZuu0DDnz6pNtRoAapI")
model = genai.GenerativeModel("gemini-pro")
def generate_response(question):
    # Generate content based on the user's question
    response = model.generate_content(question)
    return response.text   