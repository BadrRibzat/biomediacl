from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.openapi.utils import get_openapi
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

# Initialize FastAPI app
app = FastAPI(
    title="Biomedical Detection API",
    description="API for real-time biomedical object detection, including arms, hands, eyes, heads, and people counting.",
    version="1.0.0",
    openapi_tags=[
        {
            "name": "detection",
            "description": "Endpoints for various detection types (arm, arm-fingers, eyes, head, people)."
        }
    ],
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS configuration
origins = [
    "http://localhost:8080",
    "http://localhost:5173",
    "https://biomedical-frontend.vercel.app",
    "https://biomedical-frontend-3ci0ch4vj-badr-ribzat-project.vercel.app",
    "https://biomedical-frontend-r6wxrqdlx-badr-ribzat-project.vercel.app",
    "https://biomedical-frontend-78ygwsva4-badr-ribzat-project.vercel.app",  # Added new frontend URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# In-memory queue for processing detection tasks
detection_queue = deque()
queue_lock = asyncio.Lock()
previous_landmarks = None

@app.get("/", tags=["root"])
async def root():
    """Root endpoint for the Biomedical Detection API."""
    return {"message": "Welcome to the Biomedical Detection API"}

async def process_detection_task(endpoint: str, image: np.ndarray):
    """Process a single detection task based on the endpoint."""
    global previous_landmarks
    try:
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
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Detection error: {str(e)}")

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
            future.set_exception(e)
        await asyncio.sleep(0.1)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(process_queue())

async def enqueue_detection(endpoint: str, image: np.ndarray):
    """Enqueue a detection task and wait for the result."""
    future = asyncio.Future()
    async with queue_lock:
        detection_queue.append((endpoint, image, future))
    return await future

@app.post("/detect/{endpoint}", tags=["detection"])
async def detect(endpoint: str, file: UploadFile = File(...)):
    """
    Unified detection endpoint that handles all detection types.

    Parameters:
    - endpoint: The type of detection to perform. Possible values:
        - `arm`: Detect arm landmarks (shoulder, elbow, wrist).
        - `arm-fingers`: Detect hand and finger landmarks.
        - `eyes`: Detect eye landmarks (iris).
        - `head`: Detect head (face) bounding boxes.
        - `people`: Count people in the image.
    - file: The image file to process.

    Returns:
    - JSON response with detection results specific to the endpoint.
    """
    try:
        # Validate endpoint
        valid_endpoints = ["arm", "arm-fingers", "eyes", "head", "people"]
        if endpoint not in valid_endpoints:
            raise HTTPException(status_code=400, detail=f"Invalid endpoint. Must be one of {valid_endpoints}")

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

# Custom OpenAPI schema
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    try:
        openapi_schema = get_openapi(
            title=app.title,
            version=app.version,
            description=app.description,
            routes=app.routes,
            tags=app.openapi_tags,
        )
        path = openapi_schema["paths"].get("/detect/{endpoint}", {}).get("post", {})
        if path and "parameters" in path and len(path["parameters"]) > 0:
            path["parameters"][0]["schema"] = {
                "type": "string",
                "enum": ["arm", "arm-fingers", "eyes", "head", "people"],
                "description": "The type of detection to perform."
            }
        app.openapi_schema = openapi_schema
        return openapi_schema
    except Exception as e:
        print(f"Error generating OpenAPI schema: {str(e)}")
        return {}

app.openapi = custom_openapi

async def process_image(file: UploadFile) -> np.ndarray:
    """
    Read and preprocess an uploaded image for detection.
    """
    contents = await file.read()
    image = Image.open(BytesIO(contents)).convert("RGB")
    image_np = np.array(image)
    return cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
