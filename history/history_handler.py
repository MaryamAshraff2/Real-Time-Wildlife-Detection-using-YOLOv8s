# history/history_handler.py
import streamlit as st
import json
from pathlib import Path

def update_history(history_file, new_entry):
    try:
        # Initialize with empty list if file doesn't exist or is empty
        if not Path(history_file).exists() or Path(history_file).stat().st_size == 0:
            history = []
        else:
            with open(history_file, "r") as f:
                history = json.load(f)
        
        history.append(new_entry)
        
        with open(history_file, "w") as f:
            json.dump(history, f, indent=2)
    except json.JSONDecodeError:
        # If file is corrupted, start fresh
        with open(history_file, "w") as f:
            json.dump([new_entry], f, indent=2)
    except Exception as e:
        st.error(f"Error updating history: {e}")

def show_history(history_file):
    st.title("📜 Prediction History")
    try:
        # Check if file exists and has content
        if not Path(history_file).exists() or Path(history_file).stat().st_size == 0:
            st.info("No history available yet.")
            return
            
        with open(history_file, "r") as f:
            history = json.load(f)

        if not history:
            st.info("No history available yet.")
            return

        for entry in reversed(history):
            with st.expander(f"📅 {entry.get('timestamp', 'Unknown time')} - {entry.get('filename', 'Unknown file')}"):
                if entry.get("type") == "image":
                    st.write(f"Detected: {entry['prediction'].get('animal', 'Unknown')} ({entry['prediction'].get('confidence', 0)}%)")
                elif entry.get("type") == "video":
                    st.write("🎥 Video Analysis")
                    if "status" in entry.get("prediction", {}):
                        st.write(f"Status: {entry['prediction']['status']}")
                elif entry.get("type") == "webcam":
                    st.write(f"🔴 Live Detection: {entry['prediction'].get('animal', 'Unknown')} ({entry['prediction'].get('confidence', 0):.2f} confidence)")
            st.markdown("---")
    except json.JSONDecodeError:
        st.error("History file is corrupted. Starting fresh.")
        with open(history_file, "w") as f:
            json.dump([], f)
    except Exception as e:
        st.error(f"Error loading history: {e}")