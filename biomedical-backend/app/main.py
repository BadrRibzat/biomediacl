from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import cv2
import numpy as np
from io import BytesIO
from PIL import Image
from .arm_detection import detect_arm
from .arm_fingers_detection import detect_arm_fingers
from .eyes_detection import detect_eyes
from .head_detection import detect_head
from .people_counting import detect_people

app = FastAPI(
    title="Biomedical Detection API",
    description="API for real-time biomedical object detection, including arms, hands, eyes, heads, and people counting.",
    version="1.0.0"
)

# Store previous landmarks for people counting (simplified for single image)
previous_landmarks = None

@app.get("/")
async def root():
    """Root endpoint for the Biomedical Detection API."""
    return {"message": "Welcome to the Biomedical Detection API"}

@app.post("/detect/arm")
async def detect_arm_endpoint(file: UploadFile = File(...)):
    """
    Detect arm landmarks in an uploaded image using MediaPipe Pose.

    Parameters:
        file: Uploaded image file (e.g., PNG, JPEG).

    Returns:
        JSON response with detection status and arm landmarks (shoulder, elbow, wrist).
    """
    try:
        image = await process_image(file)
        result = detect_arm(image)
        return JSONResponse(status_code=200, content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

@app.post("/detect/arm-fingers")
async def detect_arm_fingers_endpoint(file: UploadFile = File(...)):
    """
    Detect hand and finger landmarks in an uploaded image using MediaPipe Hands.

    Parameters:
        file: Uploaded image file (e.g., PNG, JPEG).

    Returns:
        JSON response with detection status and hand landmarks.
    """
    try:
        image = await process_image(file)
        result = detect_arm_fingers(image)
        return JSONResponse(status_code=200, content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

@app.post("/detect/eyes")
async def detect_eyes_endpoint(file: UploadFile = File(...)):
    """
    Detect eye landmarks in an uploaded image using MediaPipe Face Mesh.

    Parameters:
        file: Uploaded image file (e.g., PNG, JPEG).

    Returns:
        JSON response with detection status and eye landmarks (iris points).
    """
    try:
        image = await process_image(file)
        result = detect_eyes(image)
        return JSONResponse(status_code=200, content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

@app.post("/detect/head")
async def detect_head_endpoint(file: UploadFile = File(...)):
    """
    Detect head (face) bounding boxes in an uploaded image using MediaPipe Face Detection.

    Parameters:
        file: Uploaded image file (e.g., PNG, JPEG).

    Returns:
        JSON response with detection status and face bounding boxes.
    """
    try:
        image = await process_image(file)
        result = detect_head(image)
        return JSONResponse(status_code=200, content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

@app.post("/detect/people")
async def detect_people_endpoint(file: UploadFile = File(...)):
    """
    Detect and count people in an uploaded image using MediaPipe Pose.

    Parameters:
        file: Uploaded image file (e.g., PNG, JPEG).

    Returns:
        JSON response with detection status, people count, and pose landmarks.
    """
    global previous_landmarks
    try:
        image = await process_image(file)
        result = detect_people(image, previous_landmarks)
        previous_landmarks = result.get("previous_landmarks")
        return JSONResponse(status_code=200, content={
            "status": result["status"],
            "count": result["count"],
            "landmarks": result["landmarks"]
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

async def process_image(file: UploadFile) -> np.ndarray:
    """
    Read and preprocess an uploaded image for detection.

    Args:
        file: Uploaded image file.

    Returns:
        NumPy array of the image in BGR format.
    """
    contents = await file.read()
    image = Image.open(BytesIO(contents)).convert("RGB")
    image_np = np.array(image)
    return cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
