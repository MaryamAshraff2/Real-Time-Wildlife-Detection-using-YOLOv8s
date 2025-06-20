# detection/video.py (updated)
import cv2
import streamlit as st
import tempfile
from datetime import datetime
from history.history_handler import update_history

def video_streaming(model, uploaded_file, conf_threshold, selected_classes, history_file):
    stframe = st.empty()
    
    # Save the uploaded video temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_file:
        tmp_file.write(uploaded_file.read())
        video_path = tmp_file.name

    cap = cv2.VideoCapture(video_path)
    
    # Log video processing start
    update_history(history_file, {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "filename": uploaded_file.name,
        "type": "video",
        "prediction": {"status": "video processing started"}
    })

    while cap.isOpened() and st.session_state.is_detecting:
        ret, frame = cap.read()
        if not ret:
            break

        results = model.predict(source=frame, conf=conf_threshold)
        detections = results[0]

        boxes = detections.boxes.xyxy.cpu().numpy()
        confs = detections.boxes.conf.cpu().numpy()
        class_ids = detections.boxes.cls.cpu().numpy().astype(int)

        if selected_classes:
            filtered = [
                (box, conf, class_id)
                for box, conf, class_id in zip(boxes, confs, class_ids)
                if model.names[class_id] in selected_classes  # Changed to use model.names
            ]
            if filtered:
                boxes, confs, class_ids = zip(*filtered)
            else:
                boxes, confs, class_ids = [], [], []

        for i, box in enumerate(boxes):
            x1, y1, x2, y2 = map(int, box)
            label = f"{model.names[class_ids[i]]}: {confs[i]:.2f}"  # Changed to use model.names
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        stframe.image(frame, channels="BGR")

    cap.release()
    
    # Log video processing completion
    update_history(history_file, {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "filename": uploaded_file.name,
        "type": "video",
        "prediction": {"status": "video processing completed"}
    })