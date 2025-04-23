import cv2
import mediapipe as mp
import numpy as np

def detect_arm_fingers(image: np.ndarray) -> dict:
    """
    Detect hand and finger landmarks in an image using MediaPipe Hands.

    Args:
        image: Input image in BGR format.

    Returns:
        dict: Dictionary containing detection status and hand landmarks.
              - status: "success" or "no_hands_detected"
              - hands: List of dictionaries, each with hand label (left/right) and landmarks
    """
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)
    
    # Convert to RGB for MediaPipe
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image_rgb)
    
    if not results.multi_hand_landmarks:
        hands.close()
        return {"status": "no_hands_detected", "hands": []}
    
    hands_data = []
    for hand_idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
        hand_label = results.multi_handedness[hand_idx].classification[0].label.lower()
        landmarks = []
        for idx, landmark in enumerate(hand_landmarks.landmark):
            landmarks.append({
                "index": idx,
                "x": landmark.x * image.shape[1],
                "y": landmark.y * image.shape[0],
                "z": landmark.z
            })
        hands_data.append({"label": hand_label, "landmarks": landmarks})
    
    hands.close()
    return {"status": "success", "hands": hands_data}
