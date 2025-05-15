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
    try:
        with st.spinner("Connecting to backend..."):
            response = requests.get("http://backend:8000/")

        if response.status_code == 200:
            st.markdown("## 🔍 Bird vs Drone Classifier")

            st.markdown("---")

            col1, col2 = st.columns([2, 1])

            with col1:
                st.markdown("""
                ### Welcome to the Bird Drone Classifier!

                This application helps you determine whether an image contains a bird or a drone.

                **How to use:**
                1. Navigate to the **Upload** tab
                2. Upload an image file (JPG, JPEG, or PNG)
                3. Wait for the AI to classify your image
                4. View the detailed results
                """)

            with col2:
                st.markdown("### Classification Types:")
                st.success("🐦 Bird")
                st.warning("🛸 Drone")

        else:
            st.markdown("### 🔴 System Status: Ups... Something went wrong :/")
    except requests.exceptions.ConnectionError:
        st.markdown("### 🔴 System Status: Ups... Something went wrong :/")

#Upload
elif selected2 == "Upload":
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)

        with st.spinner("Classifying..."):
            try:
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                response = requests.post("http://backend:8000/classify", files=files)

                if response.status_code == 200:
                    result = response.json()

                    if "prediction" in result:
                        bird_prob = result["prediction"]["Bird"]
                        drone_prob = result["prediction"]["Drone"]

                        col1, col2 = st.columns(2)

                        with col1:
                            st.markdown("### 🐦 Bird")
                            st.progress(bird_prob)
                            st.markdown(f"**{bird_prob * 100:.2f}%**")

                        with col2:
                            st.markdown("### 🛸 Drone")
                            st.progress(drone_prob)
                            st.markdown(f"**{drone_prob * 100:.2f}%**")

                        st.markdown("---")
                        if bird_prob > drone_prob:
                            st.success(f"This is most likely a **Bird** 🐦 ({bird_prob * 100:.2f}%)")
                        else:
                            st.warning(f"This is most likely a **Drone** 🛸 ({drone_prob * 100:.2f}%)")
                    else:
                        st.write(result)
                else:
                    st.error(f"Failed to classify the image: {response.status_code} - {response.text}")
            except requests.exceptions.ConnectionError:
                st.error("Connection error: Backend server is not running. Please start the backend server first.")

# History
elif selected2 == "History":
    response = requests.get("http://backend:8000/history")
    if response.status_code == 200:
        history = response.json()
        for item in history:
            st.write(f"File: {item['file_name']}, Result: {item['result']}")
    else:
        # st.write("Failed to fetch history")
        st.write("Sorry, the feature hasn't been implemented yet.")

# Settings
elif selected2 == "Settings":
    response = requests.get("http://backend:8000/settings")
    if response.status_code == 200:
        settings = response.json()
        for item in settings:
            st.write(f"File: {item['file_name']}, Result: {item['result']}")
    else:
        # st.write("Failed to fetch settings")
        st.write("Sorry, the feature hasn't been implemented yet.")