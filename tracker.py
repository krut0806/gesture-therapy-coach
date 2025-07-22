import cv2
import numpy as np
import mediapipe as mp

class HandTracker:
    def __init__(self, max_num_hands=1, detection_confidence=0.5):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=max_num_hands,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=0.5
        )
        self.mp_draw = mp.solutions.drawing_utils

        
        self.segmentation = mp.solutions.selfie_segmentation.SelfieSegmentation(model_selection=1)

    def process_frame(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(
                    frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS
                )

        return results, frame

    def remove_background(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.segmentation.process(rgb)

        mask = results.segmentation_mask > 0.5
        white_bg = np.ones(frame.shape, dtype=np.uint8) * 255

        output = np.where(mask[:, :, None], frame, white_bg)
        return output
