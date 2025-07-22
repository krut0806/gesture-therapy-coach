# main.py
import streamlit as st
import cv2
import time
import numpy as np
import datetime
from tracker import HandTracker
from exercise_logic import (
    evaluate_finger_flexion,
    evaluate_thumb_abduction,
    evaluate_wrist_rotation,
    evaluate_grip_opening,
    evaluate_finger_taps,
)
from logger import log_progress, init_log


st.set_page_config(page_title="Therapy Coach", layout="wide")
st.title("Gesture-Based Physical Therapy Coach")


exercises = [
    {"name": "Finger Flexion", "instruction": "Make a full fist, then open wide.", "func": evaluate_finger_flexion},
    {"name": "Thumb Abduction", "instruction": "Move your thumb away from the palm like a thumbs-up.", "func": evaluate_thumb_abduction},
    {"name": "Wrist Rotation", "instruction": "Rotate your wrist in a circular motion.", "func": evaluate_wrist_rotation},
    {"name": "Grip Opening", "instruction": "Spread your fingers out wide.", "func": evaluate_grip_opening},
    {"name": "Finger Taps", "instruction": "Touch each fingertip with your thumb.", "func": evaluate_finger_taps},
]


username = st.text_input("Enter your name:", "patient_01")
stframe = st.empty()
st.sidebar.markdown("### Session Info")
session_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

run_session = st.button("Start Therapy Session")
restart_session = st.button(" Restart Session")


session_results = []

if run_session or restart_session:
    cap = cv2.VideoCapture(0)
    tracker = HandTracker()
    init_log(username)

    for exercise in exercises:
        name = exercise["name"]
        instruction = exercise["instruction"]
        evaluator = exercise["func"]

        st.markdown(f"<h2 style='text-align: center;'>{instruction}</h2>", unsafe_allow_html=True)
        time.sleep(2)

        reps = 0
        target_reps = 5
        scores = []

        while cap.isOpened() and reps < target_reps:
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)
            results, annotated = tracker.process_frame(frame)

            if results.multi_hand_landmarks:
                score, feedback = evaluator(results)

                threshold = 0.2 if name in ["Wrist Rotation", "Finger Taps"] else 0.7

                cv2.putText(annotated, f"Score: {score:.2f}", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.putText(annotated, feedback, (10, 60),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

                if score > threshold:
                    reps += 1
                    scores.append(score)
                    log_progress(username, name, score, feedback)
                    time.sleep(0.5)

            stframe.image(annotated, channels="BGR")
            time.sleep(0.03)

        avg_score = round(sum(scores) / len(scores), 2) if scores else 0.0
        session_results.append({"Exercise": name, "Reps": reps, "Avg Score": avg_score})

    cap.release()

    
    final_frame = np.zeros((480, 640, 3), dtype=np.uint8)
    cv2.putText(final_frame, "Therapy Session Completed", (30, 240),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.putText(final_frame, " Well Done! ", (180, 300),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    stframe.image(final_frame, channels="BGR")

    
    st.markdown("<h2 style='text-align: center; color: green;'> The therapy session has ended!!</h2>", unsafe_allow_html=True)

    st.markdown(" Session result")
    st.table(session_results)
