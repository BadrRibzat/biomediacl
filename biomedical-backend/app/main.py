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
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from collections import deque

app = FastAPI(
    title="Biomedical Detection API",
    description="API for real-time biomedical object detection, including arms, hands, eyes, heads, and people counting.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://biomedical-frontend.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory queue for processing detection tasks
detection_queue = deque()
queue_lock = asyncio.Lock()

# Store previous landmarks for people counting (simplified for single image)
previous_landmarks = None

@app.get("/")
async def root():
    """Root endpoint for the Biomedical Detection API."""
    return {"message": "Welcome to the Biomedical Detection API"}

async def process_detection_task(endpoint: str, image: np.ndarray):
    """Process a single detection task based on the endpoint."""
    global previous_landmarks
    if endpoint == "arm":
        return detect_arm(image)
    elif endpoint == "arm-fingers":
        return detect_arm_fingers(image)
    elif endpoint == "eyes":
        return detect_eyes(image)
    elif endpoint == "head":
        return detect_head(image)
    elif endpoint == "people":
        result = detect_people(image, previous_landmarks)
        previous_landmarks = result.get("previous_landmarks")
        return {
            "status": result["status"],
            "count": result["count"],
            "landmarks": result["landmarks"]
        }
    else:
        raise HTTPException(status_code=400, detail="Invalid endpoint")

async def process_queue():
    """Process tasks from the queue one at a time."""
    while True:
        async with queue_lock:
            if not detection_queue:
                await asyncio.sleep(0.1)
                continue
            endpoint, image, future = detection_queue.popleft()
        try:
            result = await process_detection_task(endpoint, image)
            future.set_result(result)
        except Exception as e:
            future.set_exception(HTTPException(status_code=500, detail=f"Error processing image: {str(e)}"))
        await asyncio.sleep(0.1)  # Small delay to prevent tight loop

# Start the queue processing task when the app starts
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(process_queue())

async def enqueue_detection(endpoint: str, image: np.ndarray):
    """Enqueue a detection task and wait for the result."""
    future = asyncio.Future()
    async with queue_lock:
        detection_queue.append((endpoint, image, future))
    return await future

@app.post("/detect/arm")
async def detect_arm_endpoint(file: UploadFile = File(...)):
    """
    Detect arm landmarks in an uploaded image using MediaPipe Pose.
    """
    image = await process_image(file)
    result = await enqueue_detection("arm", image)
    return JSONResponse(status_code=200, content=result)

@app.post("/detect/arm-fingers")
async def detect_arm_fingers_endpoint(file: UploadFile = File(...)):
    """
    Detect hand and finger landmarks in an uploaded image using MediaPipe Hands.
    """
    image = await process_image(file)
    result = await enqueue_detection("arm-fingers", image)
    return JSONResponse(status_code=200, content=result)

@app.post("/detect/eyes")
async def detect_eyes_endpoint(file: UploadFile = File(...)):
    """
    Detect eye landmarks in an uploaded image using MediaPipe Face Mesh.
    """
    image = await process_image(file)
    result = await enqueue_detection("eyes", image)
    return JSONResponse(status_code=200, content=result)

@app.post("/detect/head")
async def detect_head_endpoint(file: UploadFile = File(...)):
    """
    Detect head (face) bounding boxes in an uploaded image using MediaPipe Face Detection.
    """
    image = await process_image(file)
    result = await enqueue_detection("head", image)
    return JSONResponse(status_code=200, content=result)

@app.post("/detect/people")
async def detect_people_endpoint(file: UploadFile = File(...)):
    """
    Detect and count people in an uploaded image using MediaPipe Pose.
    """
    image = await process_image(file)
    result = await enqueue_detection("people", image)
    return JSONResponse(status_code=200, content=result)

async def process_image(file: UploadFile) -> np.ndarray:
    """
    Read and preprocess an uploaded image for detection.
    """
    contents = await file.read()
    image = Image.open(BytesIO(contents)).convert("RGB")
    image_np = np.array(image)
    return cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
