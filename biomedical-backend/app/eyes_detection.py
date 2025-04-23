import cv2
import mediapipe as mp
import numpy as np

def detect_eyes(image: np.ndarray) -> dict:
    """
    Detect eye landmarks in an image using MediaPipe Face Mesh.

    Args:
        image: Input image in BGR format.

    Returns:
        dict: Dictionary containing detection status and eye landmarks (left and right irises).
              - status: "success" or "no_face_detected"
              - landmarks: List of dictionaries with x, y, z coordinates for iris landmarks
    """
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True)
    
    # Convert to RGB for MediaPipe
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(image_rgb)
    
    if not results.multi_face_landmarks:
        face_mesh.close()
        return {"status": "no_face_detected", "landmarks": []}
    
    eye_landmarks = []
    # Example iris landmarks: left eye (468-473), right eye (474-479)
    iris_indices = list(range(468, 474)) + list(range(474, 480))
    iris_names = [f"left_iris_{i-468}" for i in range(468, 474)] + [f"right_iris_{i-474}" for i in range(474, 480)]
    
    for face_landmarks in results.multi_face_landmarks:
        for idx, name in zip(iris_indices, iris_names):
            landmark = face_landmarks.landmark[idx]
            eye_landmarks.append({
                "name": name,
                "x": landmark.x * image.shape[1],
                "y": landmark.y * image.shape[0],
                "z": landmark.z
            })
    
    face_mesh.close()
    return {"status": "success", "landmarks": eye_landmarks}
