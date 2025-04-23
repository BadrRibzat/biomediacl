import cv2
import mediapipe as mp
import numpy as np

def detect_arm(image: np.ndarray) -> dict:
    """
    Detect arm landmarks in an image using MediaPipe Pose.

    Args:
        image: Input image in BGR format.

    Returns:
        dict: Dictionary containing detection status and arm landmarks (shoulder, elbow, wrist).
              - status: "success" or "no_pose_detected"
              - landmarks: List of dictionaries with x, y, z coordinates for left and right arm landmarks
    """
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
    
    # Convert to RGB for MediaPipe
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = pose.process(image_rgb)
    
    if not results.pose_landmarks:
        pose.close()
        return {"status": "no_pose_detected", "landmarks": []}
    
    # Extract arm landmarks (left: 11, 13, 15; right: 12, 14, 16)
    arm_landmarks = []
    landmark_indices = [11, 13, 15, 12, 14, 16]  # Left shoulder, elbow, wrist; right shoulder, elbow, wrist
    landmark_names = ["left_shoulder", "left_elbow", "left_wrist", "right_shoulder", "right_elbow", "right_wrist"]
    
    for idx, name in zip(landmark_indices, landmark_names):
        landmark = results.pose_landmarks.landmark[idx]
        arm_landmarks.append({
            "name": name,
            "x": landmark.x * image.shape[1],
            "y": landmark.y * image.shape[0],
            "z": landmark.z
        })
    
    pose.close()
    return {"status": "success", "landmarks": arm_landmarks}
