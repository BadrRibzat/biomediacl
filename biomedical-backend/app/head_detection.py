import cv2
import mediapipe as mp
import numpy as np

def detect_head(image: np.ndarray) -> dict:
    """
    Detect head (face) bounding boxes in an image using MediaPipe Face Detection.

    Args:
        image: Input image in BGR format.

    Returns:
        dict: Dictionary containing detection status and face bounding boxes.
              - status: "success" or "no_faces_detected"
              - faces: List of dictionaries with bounding box coordinates and confidence
    """
    mp_face_detection = mp.solutions.face_detection
    face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.5)
    
    # Convert to RGB for MediaPipe
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = face_detection.process(image_rgb)
    
    if not results.detections:
        face_detection.close()
        return {"status": "no_faces_detected", "faces": []}
    
    faces = []
    for detection in results.detections:
        bbox = detection.location_data.relative_bounding_box
        h, w = image.shape[:2]
        faces.append({
            "xmin": int(bbox.xmin * w),
            "ymin": int(bbox.ymin * h),
            "width": int(bbox.width * w),
            "height": int(bbox.height * h),
            "confidence": float(detection.score[0])
        })
    
    face_detection.close()
    return {"status": "success", "faces": faces}
