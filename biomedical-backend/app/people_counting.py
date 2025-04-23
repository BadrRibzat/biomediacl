import cv2
import mediapipe as mp
import numpy as np

def detect_people(image: np.ndarray, previous_landmarks: list = None) -> dict:
    """
    Detect and count people in an image using MediaPipe Pose.

    Args:
        image: Input image in BGR format.
        previous_landmarks: List of previous pose landmarks for tracking (optional).

    Returns:
        dict: Dictionary containing detection status, people count, and landmarks.
              - status: "success" or "no_pose_detected"
              - count: Number of new people detected (1 or 0)
              - landmarks: List of pose landmarks
              - previous_landmarks: Updated landmarks for next call
    """
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
    
    # Convert to RGB for MediaPipe
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = pose.process(image_rgb)
    
    if not results.pose_landmarks:
        pose.close()
        return {
            "status": "no_pose_detected",
            "count": 0,
            "landmarks": [],
            "previous_landmarks": previous_landmarks
        }
    
    current_landmarks = [
        {"x": lm.x * image.shape[1], "y": lm.y * image.shape[0], "z": lm.z}
        for lm in results.pose_landmarks.landmark
    ]
    
    # Check if this is a new person
    count = 1 if is_new_person(current_landmarks, previous_landmarks) else 0
    
    pose.close()
    return {
        "status": "success",
        "count": count,
        "landmarks": current_landmarks,
        "previous_landmarks": current_landmarks
    }

def is_new_person(current_landmarks: list, previous_landmarks: list) -> bool:
    """
    Determine if the current pose represents a new person based on landmark movement.

    Args:
        current_landmarks: List of current pose landmarks.
        previous_landmarks: List of previous pose landmarks.

    Returns:
        bool: True if a new person is detected, False otherwise.
    """
    if not previous_landmarks:
        return True
    for curr, prev in zip(current_landmarks, previous_landmarks):
        if abs(curr["x"] - prev["x"]) > 0.2 * 640 or abs(curr["y"] - prev["y"]) > 0.2 * 480:
            return True
    return False
