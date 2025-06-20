from ultralytics import YOLO
import streamlit as st
from pathlib import Path

@st.cache_resource
def load_model(model_type):
    if model_type == "Custom Model (Lion/Tiger)":
        return YOLO(str(Path("model/best.pt")))
    return YOLO(str(Path("model/yolov8x.pt")))
