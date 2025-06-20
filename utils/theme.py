import streamlit as st

def apply_custom_theme(dark_mode):
    if dark_mode:
        primary_color = "#2E4E2F"
        background_color = "#1E2B20"
        secondary_background = "#2C3A28"
        text_color = "#E5E5E5"
    else:
        primary_color = "#6B4F2A"
        background_color = "#FAF5EC"
        secondary_background = "#F3EDE1"
        text_color = "#2E3D24"

    st.markdown(f"""
        <style>
            body, .stApp {{
                background-color: {background_color};
                color: {text_color};
            }}
            .stSidebar {{
                background-color: {secondary_background};
            }}
            .stButton > button {{
                background-color: {primary_color};
                color: white;
                border-radius: 8px;
                padding: 8px 16px;
                font-weight: bold;
                border: none;
            }}
            .stFileUploader {{
                background-color: {secondary_background};
                border-radius: 8px;
                padding: 10px;
            }}
            .css-1cpxqw2 a {{
                color: {primary_color} !important;
            }}
        </style>
    """, unsafe_allow_html=True)
