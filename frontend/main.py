import streamlit as st
from streamlit_option_menu import option_menu
import requests

st.set_page_config(page_title="AmIdrone")

# Horizontal menu
selected2 = option_menu(None, ["Home", "Upload", "History", 'Settings'],
    icons=['house', 'cloud-upload', "list-task", 'gear'],
    menu_icon="cast", default_index=0, orientation="horizontal")

# Home
if selected2 == "Home":
    response = requests.get("http://127.0.0.1:8000/")
    if response.status_code == 200:
        st.write(response.text)
    else:
        st.write("Failed to fetch data from the API")

# Upload
elif selected2 == "Upload":
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
        response = requests.post("http://127.0.0.1:8000/classify", files=files)
        if response.status_code == 200:
            st.write(response.json())
        else:
            st.write("Failed to classify the image")
            st.write(f"Server responded with error: {response.status_code} - {response.text}")

# History
elif selected2 == "History":
    response = requests.get("http://127.0.0.1:8000/history")
    if response.status_code == 200:
        history = response.json()
        for item in history:
            st.write(f"File: {item['file_name']}, Result: {item['result']}")
    else:
        # st.write("Failed to fetch history")
        st.write("Sorry, the feature hasn't been implemented yet.")

# Settings
elif selected2 == "Settings":
    response = requests.get("http://127.0.0.1:8000/settings")
    if response.status_code == 200:
        settings = response.json()
        for item in settings:
            st.write(f"File: {item['file_name']}, Result: {item['result']}")
    else:
        # st.write("Failed to fetch settings")
        st.write("Sorry, the feature hasn't been implemented yet.")