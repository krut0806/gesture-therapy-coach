import numpy as np
import math

def get_coords(hand_landmarks, indices):
    return np.array([[hand_landmarks.landmark[i].x,
                      hand_landmarks.landmark[i].y,
                      hand_landmarks.landmark[i].z] for i in indices])


def evaluate_finger_flexion(results):
    landmarks = results.multi_hand_landmarks[0]
    finger_tip_ids = [8, 12, 16, 20]
    mcp_ids = [5, 9, 13, 17]
    total_flex = 0

    for tip, mcp in zip(finger_tip_ids, mcp_ids):
        tip_coord = np.array([landmarks.landmark[tip].x, landmarks.landmark[tip].y])
        mcp_coord = np.array([landmarks.landmark[mcp].x, landmarks.landmark[mcp].y])
        dist = np.linalg.norm(tip_coord - mcp_coord)
        total_flex += dist

    avg_flex = total_flex / 4
    score = 1 - min(avg_flex * 5, 1)  
    feedback = "Good Flex!" if score > 0.7 else "Try curling fingers more"
    return score, feedback


def evaluate_thumb_abduction(results):
    landmarks = results.multi_hand_landmarks[0]
    thumb_tip = np.array([landmarks.landmark[4].x, landmarks.landmark[4].y])
    index_mcp = np.array([landmarks.landmark[5].x, landmarks.landmark[5].y])
    distance = np.linalg.norm(thumb_tip - index_mcp)
    score = min(distance * 5, 1.0)
    feedback = "Nice thumb stretch!" if score > 0.6 else "Spread your thumb more"
    return score, feedback


def evaluate_wrist_rotation(results):
    landmarks = results.multi_hand_landmarks[0]
    wrist = np.array([landmarks.landmark[0].x, landmarks.landmark[0].y])
    index = np.array([landmarks.landmark[5].x, landmarks.landmark[5].y])
    pinky = np.array([landmarks.landmark[17].x, landmarks.landmark[17].y])
    
    vec1 = index - wrist
    vec2 = pinky - wrist
    angle = angle_between(vec1, vec2)

    score = angle / 180  
    feedback = "Great rotation!" if score > 0.3 else "Rotate your wrist more"
    return score, feedback






def evaluate_finger_taps(results):
    landmarks = results.multi_hand_landmarks[0]
    thumb = np.array([landmarks.landmark[4].x, landmarks.landmark[4].y])
    finger_tips = [8, 12, 16, 20]  # Index to pinky tips

    distances = []
    for tip in finger_tips:
        tip_coord = np.array([landmarks.landmark[tip].x, landmarks.landmark[tip].y])
        distance = np.linalg.norm(thumb - tip_coord)
        distances.append(1 - min(distance * 10, 1.0))  # Scale & invert for scoring

    score = np.mean(distances)
    feedback = "Great tapping!" if score > 0.2 else "Tap each fingertip with your thumb"
    return score, feedback




def evaluate_grip_opening(results):
    if not results.multi_hand_landmarks:
        return 0.0, "No hand detected"

    hand_landmarks = results.multi_hand_landmarks[0]
    landmarks = hand_landmarks.landmark

    
    finger_tips = [8, 12, 16, 20]

    
    palm_indices = [0, 5, 9, 13, 17] 
    palm_coords = np.array([[landmarks[i].x, landmarks[i].y] for i in palm_indices])
    palm_center = np.mean(palm_coords, axis=0)

    dists = []
    for tip in finger_tips:
        tip_coord = np.array([landmarks[tip].x, landmarks[tip].y])
        dists.append(np.linalg.norm(tip_coord - palm_center))

    avg_dist = np.mean(dists)

    
    score = min(avg_dist * 5, 1.0)

    feedback = "Good! Now relax your fingers." if score > 0.8 else "Spread your fingers wide!"
    return score, feedback




def compute_spread_score(results):
    if not results.multi_hand_landmarks:
        return 0.0

    hand_landmarks = results.multi_hand_landmarks[0]
    landmarks = hand_landmarks.landmark

    
    finger_tips = [8, 12, 16, 20]

    
    palm_indices = [0, 1, 5, 9, 13, 17]  
    palm_coords = np.array([[landmarks[i].x, landmarks[i].y] for i in palm_indices])
    palm_center = np.mean(palm_coords, axis=0)

    dists = []
    for tip in finger_tips:
        tip_coord = np.array([landmarks[tip].x, landmarks[tip].y])
        dist = np.linalg.norm(tip_coord - palm_center)
        dists.append(dist)

    avg_dist = np.mean(dists)

    
    spread_score = np.clip((avg_dist - 0.05) / (0.20 - 0.05), 0, 1)

    return spread_score


    

def angle_between(v1, v2):
    unit1 = v1 / np.linalg.norm(v1)
    unit2 = v2 / np.linalg.norm(v2)
    dot = np.dot(unit1, unit2)
    return np.degrees(np.arccos(np.clip(dot, -1.0, 1.0)))
