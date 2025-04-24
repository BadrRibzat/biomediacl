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
from flask import Flask, request, jsonify
from flask_cors import CORS

# Initialize Flask app
flask_app = Flask(__name__)

# Enable CORS for Flask with specific origins
CORS(flask_app, resources={
    r"/flask/detect/*": {
        "origins": [
            "http://localhost:8080",
            "https://biomedical-frontend.vercel.app"
        ],
        "methods": ["POST"],
        "allow_headers": ["*"]
    }
})

# Flask endpoint
@flask_app.route('/flask/detect/<endpoint>', methods=['POST'])
def flask_detect(endpoint):
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    try:
        # Read image file
        contents = file.read()
        image = Image.open(BytesIO(contents)).convert("RGB")
        image_np = np.array(image)
        image_bgr = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
        
        # Process based on endpoint
        if endpoint == "arm":
            result = detect_arm(image_bgr)
        elif endpoint == "arm-fingers":
            result = detect_arm_fingers(image_bgr)
        elif endpoint == "eyes":
            result = detect_eyes(image_bgr)
        elif endpoint == "head":
            result = detect_head(image_bgr)
        elif endpoint == "people":
            result = detect_people(image_bgr)
        else:
            return jsonify({'error': 'Invalid endpoint'}), 400
            
        return jsonify({
            'status': 'success',
            'result': result
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Initialize FastAPI app
fastapi_app = FastAPI(
    title="Biomedical Detection API",
    description="API for real-time biomedical object detection, including arms, hands, eyes, heads, and people counting.",
    version="1.0.0"
)

# CORS for FastAPI
origins = [
    "http://localhost:8080",
    "http://localhost:5173",
    "https://biomedical-frontend.vercel.app"
]

fastapi_app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory queue for processing detection tasks
detection_queue = deque()
queue_lock = asyncio.Lock()
previous_landmarks = None

@fastapi_app.get("/")
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
        await asyncio.sleep(0.1)

@fastapi_app.on_event("startup")
async def startup_event():
    asyncio.create_task(process_queue())

async def enqueue_detection(endpoint: str, image: np.ndarray):
    """Enqueue a detection task and wait for the result."""
    future = asyncio.Future()
    async with queue_lock:
        detection_queue.append((endpoint, image, future))
    return await future

@fastapi_app.post("/detect/{endpoint}")
async def fastapi_detect(endpoint: str, file: UploadFile = File(...)):
    """
    Unified detection endpoint for FastAPI that handles all detection types.
    """
    try:
        # Process the uploaded image
        contents = await file.read()
        image = Image.open(BytesIO(contents)).convert("RGB")
        image_np = np.array(image)
        image_bgr = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
        
        # Enqueue the detection task
        result = await enqueue_detection(endpoint, image_bgr)
        return JSONResponse(status_code=200, content=result)
        
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

async def process_image(file: UploadFile) -> np.ndarray:
    """
    Read and preprocess an uploaded image for detection.
    """
    contents = await file.read()
    image = Image.open(BytesIO(contents)).convert("RGB")
    image_np = np.array(image)
    return cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
