import cv2
import mediapipe as mp
import numpy as np

def detect_head(image: np.ndarray) -> dict:
    """
    Detect head (face) bounding boxes in an image using MediaPipe Face Detection.
    """
    mp_face_detection = mp.solutions.face_detection
    face_detection = mp_face_detection.FaceDetection(
        model_selection=1,  # 0 for close-range, 1 for longer-range
        min_detection_confidence=0.3  # Lowered from 0.5 to 0.3 for better detection
    )
    
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
        
        # Calculate face bounding box coordinates
        xmin = max(0, int(bbox.xmin * w))
        ymin = max(0, int(bbox.ymin * h))
        width = min(w - xmin, int(bbox.width * w))
        height = min(h - ymin, int(bbox.height * h))
        
        # Get key points (eyes, nose, mouth center)
        keypoints = {}
        for keypoint in detection.location_data.relative_keypoints:
            keypoints[mp_face_detection.FaceKeyPoint(keypoint).name] = {
                "x": int(keypoint.x * w),
                "y": int(keypoint.y * h)
            }
        
        faces.append({
            "xmin": xmin,
            "ymin": ymin,
            "width": width,
            "height": height,
            "confidence": float(detection.score[0]),
            "keypoints": keypoints
        })
    
    face_detection.close()
    return {"status": "success", "faces": faces}
