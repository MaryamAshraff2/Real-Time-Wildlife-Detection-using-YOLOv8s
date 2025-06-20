import streamlit as st
from datetime import datetime
from PIL import Image
import tempfile
import cv2

from history.history_handler import update_history

def process_image(uploaded_file, model, history_file):
    st.image(uploaded_file, caption="Uploaded Image", width=400)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
        img = Image.open(uploaded_file)
        img.save(tmp.name)
        tmp_path = tmp.name

    with st.spinner("🔍 Analyzing image..."):
        results = model.predict(tmp_path, conf=0.5)
        boxes = results[0].boxes
        names = model.names

    if boxes:
        best_box = boxes[0]
        class_id = int(best_box.cls[0])
        confidence = float(best_box.conf[0])
        label = names[class_id]
        st.success(f"✅ Detected: {label} with {confidence*100:.1f}% confidence")

        update_history(history_file, {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "filename": uploaded_file.name,
            "type": "image",
            "prediction": {"animal": label, "confidence": round(confidence * 100, 1)}
        })
    else:
        st.warning("No animals detected in the image")
