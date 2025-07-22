import streamlit as st
import cv2
import time
from tracker import HandTracker
from exercise_logic import (
    evaluate_finger_flexion,
    evaluate_thumb_abduction,
    evaluate_wrist_rotation,
    evaluate_grip_opening,
    evaluate_finger_taps
)
from logger import log_progress, init_log
import datetime


st.set_page_config(page_title="Therapy Coach", layout="wide")
st.title("Gesture-Based Physical Therapy Coach")


exercises = [
    {
        "name": "Finger Flexion",
        "instruction": "Make a full fist, then open wide.",
        "func": evaluate_finger_flexion,
    },
    {
        "name": "Thumb Abduction",
        "instruction": "Move your thumb away from the palm like a thumbs-up.",
        "func": evaluate_thumb_abduction,
    },
    {
        "name": "Wrist Rotation",
        "instruction": "Rotate your wrist in a circular motion.",
        "func": evaluate_wrist_rotation,
    },
    {
        "name": "Grip Opening",
        "instruction": "Spread your fingers out wide.",
        "func": evaluate_grip_opening,
    },
    {
        "name": "Finger Taps",
        "instruction": "Touch each fingertip with your thumb.",
        "func": evaluate_finger_taps,
    },
]

username = st.text_input("Enter your name", "patient_01")
stframe = st.empty()
instr_box = st.empty()
session_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
run_session = st.button("Start Therapy Session")

if run_session:
    cap = cv2.VideoCapture(0)
    tracker = HandTracker()
    init_log(username)

    for idx, exercise in enumerate(exercises):
        name = exercise["name"]
        instruction = exercise["instruction"]
        evaluator = exercise["func"]

        
        countdown_seconds = 3
        start_time = time.time()

        while time.time() - start_time < countdown_seconds:
            remaining = countdown_seconds - int(time.time() - start_time)
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)
            cv2.putText(frame, f"Next: {name} in {remaining}...", (30, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 0), 3)
            stframe.image(frame, channels="BGR")
            time.sleep(0.03)

       
        instr_box.markdown(f"<h2 style='text-align: center;'>{instruction}</h2>", unsafe_allow_html=True)

        reps = 0
        target_reps = 5

        while cap.isOpened() and reps < target_reps:
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)
            results, annotated = tracker.process_frame(frame)

            if results.multi_hand_landmarks:
                score, feedback = evaluator(results)

                
                if name == "Wrist Rotation":
                    threshold = 0.3
                elif name == "Finger Taps":
                    threshold = 0.2
                else:
                    threshold = 0.7

                cv2.putText(annotated, f"Score: {score:.2f}", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.putText(annotated, feedback, (10, 60),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

                if score > threshold:
                    reps += 1
                    log_progress(username, name, score, feedback)
                    time.sleep(0.5)

            stframe.image(annotated, channels="BGR")
            time.sleep(0.03)

       
        done_time = time.time() + 3
        while time.time() < done_time:
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.flip(frame, 1)
            results, annotated = tracker.process_frame(frame)

            cv2.putText(annotated, f"Completed: {target_reps} reps", (30, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 200, 0), 2)

            
            if idx == len(exercises) - 1:
                cv2.putText(annotated, "Therapy session complete!", (30, 100),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 150, 255), 2)

            stframe.image(annotated, channels="BGR")
            time.sleep(0.03)

    cap.release()
    instr_box.markdown(
        f"<h2 style='text-align: center; color: green;'>Therapy session complete! All progress has been logged.</h2>",
        unsafe_allow_html=True
    )
