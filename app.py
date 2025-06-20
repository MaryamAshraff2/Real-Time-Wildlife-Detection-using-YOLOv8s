# app.py (updated)
import streamlit as st
st.set_page_config(page_title="Wildlife Detection", layout="wide")

import os
import json
from pathlib import Path
from datetime import datetime

from utils.theme import apply_custom_theme
from utils.classes import load_model
from detection.image import process_image
from detection.video import video_streaming
from detection.webcam import live_streaming
from history.history_handler import update_history, show_history

# === Page Functions ===
# app.py (updated snippet)
def show_home(model, history_file):
    st.title("📷 Wildlife Detection")
    input_type = st.radio(
        "Select input type:",
        ["Upload Image", "Upload Video", "Webcam"],
        horizontal=True
    )
    
    if input_type == "Upload Image":
        uploaded_file = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png"])
        if uploaded_file:
            process_image(uploaded_file, model, history_file)
            
    elif input_type == "Upload Video":
        uploaded_file = st.file_uploader("Choose a video file", type=["mp4", "mov", "avi"])
        if uploaded_file:
            st.session_state.is_detecting = True
            video_streaming(model, uploaded_file, conf_threshold=0.5, selected_classes=None, history_file=history_file)
            
    elif input_type == "Webcam":
        if st.button("Start Webcam"):
            st.session_state.is_detecting = True
            st.session_state.is_webcam_active = True
            live_streaming(model, conf_threshold=0.5, selected_classes=None, history_file=history_file)
        
        if st.button("Stop Webcam"):
            st.session_state.is_detecting = False
            st.session_state.is_webcam_active = False
            st.experimental_rerun()



def show_settings():
    st.title("⚙️ Settings")
    dark_mode = st.toggle("🌙 Enable Dark Mode", st.session_state.dark_mode)
    st.session_state.dark_mode = dark_mode
    apply_custom_theme(dark_mode)
    st.info("🔄 Refresh the page to apply changes.")

def main():
    if "dark_mode" not in st.session_state:
        st.session_state.dark_mode = False
    if "is_detecting" not in st.session_state:
        st.session_state.is_detecting = False
    if "is_webcam_active" not in st.session_state:
        st.session_state.is_webcam_active = False
        
    apply_custom_theme(st.session_state.dark_mode)

    st.sidebar.title("📌 Navigate")
    page = st.sidebar.radio("Navigation", ["🏠 Home", "📊 History", "⚙️ Settings"], 
                       label_visibility="collapsed" if st.session_state.get('hide_labels', False) else "visible")

    model_choice = st.sidebar.radio(
        "Choose model:",
        ["Custom Model (Lion/Tiger)", "Pretrained Model (Zebra, Bear, Giraffe, Elephant)"],
        index=1
    )
    model = load_model(model_choice)

    # In the main() function of app.py:
    HISTORY_FILE = "history.json"
    # Ensure the file exists and is valid JSON
    if not os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "w") as f:
            json.dump([], f)
    else:
        # Check if file is valid JSON
        try:
            with open(HISTORY_FILE, "r") as f:
                json.load(f)
        except json.JSONDecodeError:
            with open(HISTORY_FILE, "w") as f:
                json.dump([], f)

    if page == "🏠 Home":
        show_home(model, HISTORY_FILE)
    elif page == "📊 History":
        show_history(HISTORY_FILE)
    elif page == "⚙️ Settings":
        show_settings()

if __name__ == "__main__":
    main()