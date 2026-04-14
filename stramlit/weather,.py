import streamlit as st
import urllib.parse

def generate_map_url(location, api_key):
    base_url = "https://www.google.com/maps/embed/v1/place"
    params = {
        "q": location,
        "key": api_key
    }
    encoded_params = urllib.parse.urlencode(params)
    return f"{base_url}?{encoded_params}"

def process_message(message, api_key):
    if "map" in message.lower():
        location = st.text_input("Please enter a location:")
        if location:
            map_url = generate_map_url(location, api_key)
            st.write("Here is the map for", location)
            st.markdown(f'<iframe width="600" height="450" frameborder="0" style="border:0" src="{map_url}"></iframe>', unsafe_allow_html=True)
    else:
        st.write("You said:", message)

st.title("Map Bot")

# Replace 'YOUR_API_KEY_HERE' with your actual Google Maps API key
api_key = "AIzaSyDxh9mzu93K1Uxggh4ov5KOhvetlXX95DY"

message = st.text_input("Please enter your message:")

if message:
    process_message(message, api_key)
