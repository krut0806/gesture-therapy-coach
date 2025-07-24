# Gesture-Based Physical Therapy Coach

This is a webcam-based physical therapy assistant that uses hand gesture recognition to guide and monitor users through a series of therapeutic hand exercises. The app is built using Python, OpenCV, MediaPipe, and Streamlit.

## Features

- Real-time hand tracking using MediaPipe
- Five pre-defined physical therapy exercises:
  - Finger Flexion
  - Thumb Abduction
  - Wrist Rotation
  - Grip Opening
  - Finger Tapping
- Live webcam video feed with score and feedback overlay
- Automatic repetition counting based on gesture accuracy
- Final session summary including average scores per exercise
- Simple Streamlit interface to run in a browser
- 
- #  Demo & Showcase

Check out the live demo video of this project on LinkedIn:  
🔗 https://www.linkedin.com/posts/kruthika-reddy-nimma_computervision-physiotherapy-streamlit-activity-7354069608242319363-WbzY?utm_source=share&utm_medium=member_desktop&rcm=ACoAAETmrdoBSAQ33VKPD5wtrCwcfKQwTNfuK5U

In this video, you’ll see the **Gesture-Based Physical Therapy Coach** in action, guiding users through real-time hand rehabilitation exercises live

## Requirements

- Python 3.8+
- Webcam (built-in or USB)
- Modern web browser (Chrome, Firefox, etc.)

# Installation

1. **Clone the repository**:

   
   git clone https://github.com/krut0806/gesture-therapy-coach.git
   cd gesture-therapy-coach
   
2. **Create a virtual environment**:
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
3.**Install the dependencies**:
     pip install -r requirements.txt
4.**Run the App**
streamlit run main.py


## File Structure
**main.py** — Streamlit front-end with webcam logic and session loop

**tracker.py** — Handles hand tracking via MediaPipe

**exercise_logic.py** — Contains logic to evaluate each gesture

**logger.py** — Logs progress for each repetition

**requirements.txt** — Python dependencies


## License
This project is for educational and non-commercial use. For commercial use or deployment, please contact the kruthikar38@gmail.com.

