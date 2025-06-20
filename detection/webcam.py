import cv2
import streamlit as st
from datetime import datetime
from history.history_handler import update_history

def live_streaming(model, conf_threshold, selected_classes, history_file):
    stframe = st.empty()
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Added DSHOW for Windows compatibility

    if not cap.isOpened():
        st.error("Webcam not accessible.")
        return

    try:
        while st.session_state.get("is_detecting", False) and st.session_state.get("is_webcam_active", False):
            ret, frame = cap.read()
            if not ret:
                continue

            results = model.predict(source=frame, conf=conf_threshold)
            detections = results[0]

            boxes = detections.boxes.xyxy.cpu().numpy() if len(detections) > 0 else []
            confs = detections.boxes.conf.cpu().numpy() if len(detections) > 0 else []
            class_ids = detections.boxes.cls.cpu().numpy().astype(int) if len(detections) > 0 else []

            if selected_classes:
                filtered = [
                    (box, conf, class_id)
                    for box, conf, class_id in zip(boxes, confs, class_ids)
                    if model.names[class_id] in selected_classes  # Changed to model.names
                ]
                if filtered:
                    boxes, confs, class_ids = zip(*filtered)
                else:
                    boxes, confs, class_ids = [], [], []

            for i, box in enumerate(boxes):
                x1, y1, x2, y2 = map(int, box)
                label = f"{model.names[class_ids[i]]}: {confs[i]:.2f}"  # Changed to model.names
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                
                # Log detection in history
                update_history(history_file, {
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "type": "webcam",
                    "prediction": {
                        "animal": model.names[class_ids[i]],  # Changed to model.names
                        "confidence": float(confs[i])
                    }
                })

            stframe.image(frame, channels="BGR")
    finally:
        cap.release()
        cv2.destroyAllWindows()