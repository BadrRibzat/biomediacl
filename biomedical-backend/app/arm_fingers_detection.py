import cv2
import mediapipe as mp
import numpy as np

def detect_arm_fingers(image: np.ndarray) -> dict:
    """
    Detect hand and finger landmarks in an image using MediaPipe Hands.
    """
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(
        static_image_mode=True,  # Changed from False to True for better single image detection
        max_num_hands=2,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    )
    
    # Convert to RGB for MediaPipe
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image_rgb)
    
    if not results.multi_hand_landmarks:
        hands.close()
        return {"status": "no_hands_detected", "hands": []}
    
    hands_data = []
    for hand_idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
        # Get handedness (left/right hand)
        handedness = results.multi_handedness[hand_idx].classification[0].label.lower()
        
        landmarks = []
        for idx, landmark in enumerate(hand_landmarks.landmark):
            landmarks.append({
                "index": idx,
                "x": landmark.x * image.shape[1],
                "y": landmark.y * image.shape[0],
                "z": landmark.z,
                "visibility": landmark.visibility if hasattr(landmark, 'visibility') else 1.0
            })
        
        hands_data.append({
            "label": handedness,
            "landmarks": landmarks,
            "score": results.multi_handedness[hand_idx].classification[0].score
        })
    
    hands.close()
    return {"status": "success", "hands": hands_data}
