<template>
  <div class="container mx-auto p-4">
    <h1 class="text-3xl font-bold mb-4">Detection</h1>

    <!-- Mode Selection -->
    <div class="mb-4">
      <h2 class="text-xl font-semibold mb-2">Select Detection Mode</h2>
      <div class="flex gap-2">
        <button
          @click="setMode('camera')"
          class="p-2 rounded"
          :class="mode === 'camera' ? 'bg-blue-500 text-white' : 'bg-gray-200'"
        >
          Use Camera
        </button>
        <button
          @click="setMode('upload')"
          class="p-2 rounded"
          :class="mode === 'upload' ? 'bg-blue-500 text-white' : 'bg-gray-200'"
        >
          Upload Image
        </button>
      </div>
    </div>

    <!-- Camera Mode -->
    <div v-if="mode === 'camera'">
      <div class="mb-4 flex flex-wrap gap-2">
        <button @click="startCamera" class="bg-green-500 hover:bg-green-700 text-white p-2 rounded" :disabled="isCameraActive">
          Start Camera
        </button>
        <button @click="stopCamera" class="bg-red-500 hover:bg-red-700 text-white p-2 rounded" :disabled="!isCameraActive">
          Stop Camera
        </button>
        <button @click="toggleDetection('arm')" class="bg-blue-500 hover:bg-blue-700 text-white p-2 rounded" :disabled="!isCameraActive">
          {{ activeDetection === 'arm' ? 'Stop Arm Detection' : 'Detect Arm' }}
        </button>
        <button @click="toggleDetection('arm-fingers')" class="bg-blue-500 hover:bg-blue-700 text-white p-2 rounded" :disabled="!isCameraActive || handsFailed">
          {{ activeDetection === 'arm-fingers' ? 'Stop Arm-Fingers Detection' : 'Detect Arm-Fingers' }}
          <span v-if="handsFailed" class="text-red-500 text-sm ml-2"> (Failed to load)</span>
        </button>
        <button @click="toggleDetection('eyes')" class="bg-blue-500 hover:bg-blue-700 text-white p-2 rounded" :disabled="!isCameraActive || faceMeshFailed">
          {{ activeDetection === 'eyes' ? 'Stop Eyes Detection' : 'Detect Eyes' }}
          <span v-if="faceMeshFailed" class="text-red-500 text-sm ml-2"> (Failed to load)</span>
        </button>
        <button @click="toggleDetection('head')" class="bg-blue-500 hover:bg-blue-700 text-white p-2 rounded" :disabled="!isCameraActive">
          {{ activeDetection === 'head' ? 'Stop Head Detection' : 'Detect Head' }}
        </button>
        <button @click="toggleDetection('people')" class="bg-blue-500 hover:bg-blue-700 text-white p-2 rounded" :disabled="!isCameraActive">
          {{ activeDetection === 'people' ? 'Stop People Detection' : 'Detect People' }}
        </button>
      </div>
      <div class="mb-4 relative">
        <video ref="videoElement" autoplay class="w-full max-w-md border rounded" v-show="isCameraActive"></video>
        <canvas ref="canvasElement" class="absolute top-0 left-0 w-full max-w-md" v-show="isCameraActive"></canvas>
        <p v-if="errorMessage" class="text-red-500 mt-2">{{ errorMessage }}</p>
      </div>
    </div>

    <!-- Upload Mode -->
    <div v-if="mode === 'upload'">
      <div class="mb-4">
        <input type="file" @change="handleImageUpload" accept="image/*" class="mb-2" />
        <div class="flex flex-wrap gap-2">
          <button @click="detectUploadedImage('arm')" class="bg-blue-500 hover:bg-blue-700 text-white p-2 rounded" :disabled="!uploadedImage">
            Detect Arm
          </button>
          <button @click="detectUploadedImage('arm-fingers')" class="bg-blue-500 hover:bg-blue-700 text-white p-2 rounded" :disabled="!uploadedImage">
            Detect Arm-Fingers
          </button>
          <button @click="detectUploadedImage('eyes')" class="bg-blue-500 hover:bg-blue-700 text-white p-2 rounded" :disabled="!uploadedImage">
            Detect Eyes
          </button>
          <button @click="detectUploadedImage('head')" class="bg-blue-500 hover:bg-blue-700 text-white p-2 rounded" :disabled="!uploadedImage">
            Detect Head
          </button>
          <button @click="detectUploadedImage('people')" class="bg-blue-500 hover:bg-blue-700 text-white p-2 rounded" :disabled="!uploadedImage">
            Detect People
          </button>
        </div>
      </div>
      <div class="mb-4" v-if="uploadedImage">
        <img :src="uploadedImage" class="w-full max-w-md border rounded" alt="Uploaded Image" />
      </div>
    </div>

    <!-- Results -->
    <div v-if="result" class="mt-4">
      <h2 class="text-xl font-semibold">Result</h2>
      <pre class="bg-gray-100 p-4 rounded">{{ result }}</pre>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onUnmounted, onMounted } from 'vue'
import { useDetectionStore } from '../stores/detection'

// Define types for the detection results
interface ErrorResult {
  error: string
}

interface ArmResult {
  status: string
  landmarks: {
    name: string
    x: number
    y: number
    z: number
  }[]
}

interface ArmFingersResult {
  status: string
  hands: {
    label: string
    landmarks: { index: number; x: number; y: number; z: number }[]
  }[]
}

interface EyesResult {
  status: string
  landmarks: { name: string; x: number; y: number; z: number }[]
}

interface HeadResult {
  status: string
  faces: { xmin: number; ymin: number; width: number; height: number; confidence: number }[]
}

interface PeopleResult {
  status: string
  count: number
  landmarks: { x: number; y: number; z: number }[]
}

type DetectionResult = ArmResult | ArmFingersResult | EyesResult | HeadResult | PeopleResult | ErrorResult

// Load MediaPipe scripts dynamically
const handsFailed = ref(false)
const faceMeshFailed = ref(false)
const errorMessage = ref('')

onMounted(() => {
  const loadScript = (src: string, retryCount = 3, delay = 1000): Promise<void> => {
    return new Promise((resolve, reject) => {
      const attemptLoad = (attemptsLeft: number) => {
        const script = document.createElement('script')
        script.src = src
        script.onload = () => resolve()
        script.onerror = () => {
          if (attemptsLeft > 0) {
            console.warn(`Retrying to load script: ${src}, attempts left: ${attemptsLeft}`)
            setTimeout(() => attemptLoad(attemptsLeft - 1), delay)
          } else {
            reject(new Error(`Failed to load script: ${src}`))
          }
        }
        document.head.appendChild(script)
      }
      attemptLoad(retryCount)
    })
  }

  Promise.all([
    loadScript('https://cdn.jsdelivr.net/npm/@mediapipe/pose@0.5.1675469404/pose.min.js'),
    loadScript('https://cdn.jsdelivr.net/npm/@mediapipe/hands@0.4.1675469240/hands.min.js').catch(() => {
      handsFailed.value = true
      errorMessage.value = 'Failed to load hand detection library. Arm-Fingers detection is disabled.'
      console.error('Failed to load MediaPipe Hands script')
    }),
    loadScript('https://cdn.jsdelivr.net/npm/@mediapipe/face_mesh@0.4.1633559619/face_mesh.min.js').catch(() => {
      faceMeshFailed.value = true
      errorMessage.value = 'Failed to load face mesh library. Eye detection is disabled.'
      console.error('Failed to load MediaPipe Face Mesh script')
    }),
    loadScript('https://cdn.jsdelivr.net/npm/@mediapipe/face_detection@0.4.1646425229/face_detection.min.js').catch(() => {
      console.error('Failed to load MediaPipe Face Detection script')
    }),
  ]).catch(err => {
    console.error('Failed to load MediaPipe scripts:', err)
    errorMessage.value = 'Failed to load detection libraries. Some features may be unavailable.'
  })
})

const store = useDetectionStore()
const videoElement = ref<HTMLVideoElement | null>(null)
const canvasElement = ref<HTMLCanvasElement | null>(null)
const isCameraActive = ref(false)
const result = ref<DetectionResult | null>(null)
const activeDetection = ref<string | null>(null)
const mode = ref<'camera' | 'upload'>('camera')
const uploadedImage = ref<string | null>(null)
let stream: MediaStream | null = null
let pose: any | null = null
let hands: any | null = null
let faceMesh: any | null = null
let faceDetection: any | null = null
let rafId: number | null = null
let jsonInterval: number | null = null

// Since we're loading scripts dynamically, we'll access MediaPipe classes from the global window object
declare global {
  interface Window {
    Pose: any
    Hands: any
    FaceMesh: any
    FaceDetection: any
  }
}

const setMode = (newMode: 'camera' | 'upload') => {
  mode.value = newMode
  stopCamera()
  uploadedImage.value = null
  result.value = null
  errorMessage.value = ''
}

// Camera Mode Functions
const startCamera = async () => {
  try {
    // Enumerate devices to check for available cameras
    const devices = await navigator.mediaDevices.enumerateDevices()
    const videoDevices = devices.filter(device => device.kind === 'videoinput')
    console.log('Available video devices:', videoDevices) // Debug: Log detected devices

    if (videoDevices.length === 0) {
      console.warn('No video devices found. Attempting to access default camera.')
      // Proceed to try getUserMedia even if no devices are enumerated
    }

    stream = await navigator.mediaDevices.getUserMedia({
      video: { facingMode: 'user', width: { ideal: 640 }, height: { ideal: 480 } },
    })
    if (videoElement.value) {
      videoElement.value.srcObject = stream
      await videoElement.value.play()
      isCameraActive.value = true
      errorMessage.value = ''
      if (canvasElement.value) {
        canvasElement.value.width = videoElement.value.videoWidth
        canvasElement.value.height = videoElement.value.videoHeight
      }
      console.log('Camera started successfully:', stream.getVideoTracks())
    }
  } catch (error: any) {
    console.error('Error accessing camera:', error)
    if (error.name === 'NotAllowedError') {
      errorMessage.value = 'Camera access denied. Please grant camera permissions in your browser settings.'
    } else if (error.name === 'NotFoundError') {
      errorMessage.value = 'No camera found. Please connect a camera or use upload mode.'
    } else if (error.name === 'NotReadableError') {
      errorMessage.value = 'Camera is in use by another application. Please close other apps and try again.'
    } else {
      errorMessage.value = `Failed to access camera: ${error.message}`
    }
  }
}

const stopCamera = () => {
  if (stream) {
    stream.getTracks().forEach(track => track.stop())
    stream = null
    isCameraActive.value = false
    activeDetection.value = null
    if (videoElement.value) {
      videoElement.value.srcObject = null
    }
    stopDetection()
    clearCanvas()
  }
  if (pose) pose.close()
  if (hands) hands.close()
  if (faceMesh) faceMesh.close()
  if (faceDetection) faceDetection.close()
}

const toggleDetection = (endpoint: string) => {
  if (activeDetection.value === endpoint) {
    activeDetection.value = null
    stopDetection()
    clearCanvas()
  } else {
    activeDetection.value = endpoint
    startDetection(endpoint)
  }
}

const startDetection = (endpoint: string) => {
  stopDetection()
  clearCanvas()

  // Initialize MediaPipe detectors
  if (endpoint === 'arm' || endpoint === 'people') {
    try {
      pose = new window.Pose({
        locateFile: (file: string) => `https://cdn.jsdelivr.net/npm/@mediapipe/pose@0.5.1675469404/${file}`,
      })
      pose.setOptions({
        modelComplexity: 1,
        minDetectionConfidence: 0.5,
        minTrackingConfidence: 0.5,
      })
      pose.onResults((results: any) => drawPoseResults(endpoint, results))
    } catch (err) {
      console.error('Failed to initialize Pose detection:', err)
      errorMessage.value = 'Pose detection failed. Please try another detection type.'
      activeDetection.value = null
      return
    }
  } else if (endpoint === 'arm-fingers' && !handsFailed.value) {
    try {
      hands = new window.Hands({
        locateFile: (file: string) => `https://cdn.jsdelivr.net/npm/@mediapipe/hands@0.4.1675469240/${file}`,
      })
      hands.setOptions({
        maxNumHands: 2,
        minDetectionConfidence: 0.5,
        minTrackingConfidence: 0.5,
      })
      hands.onResults((results: any) => drawHandsResults(results))
    } catch (err) {
      console.error('Failed to initialize Hands detection:', err)
      handsFailed.value = true
      errorMessage.value = 'Hands detection failed. Please try another detection type.'
      activeDetection.value = null
      return
    }
  } else if (endpoint === 'eyes' && !faceMeshFailed.value) {
    try {
      faceMesh = new window.FaceMesh({
        locateFile: (file: string) => `https://cdn.jsdelivr.net/npm/@mediapipe/face_mesh@0.4.1633559619/${file}`,
      })
      faceMesh.setOptions({
        maxNumFaces: 1,
        refineLandmarks: true,
        minDetectionConfidence: 0.5,
        minTrackingConfidence: 0.5,
      })
      faceMesh.onResults((results: any) => drawFaceMeshResults(results))
    } catch (err) {
      console.error('Failed to initialize FaceMesh detection:', err)
      faceMeshFailed.value = true
      errorMessage.value = 'Face mesh detection failed. Please try another detection type.'
      activeDetection.value = null
      return
    }
  } else if (endpoint === 'head') {
    // Head detection is handled by the backend, but we can initialize FaceDetection for visualization
    try {
      faceDetection = new window.FaceDetection({
        locateFile: (file: string) => `https://cdn.jsdelivr.net/npm/@mediapipe/face_detection@0.4.1646425229/${file}`,
      })
      faceDetection.setOptions({
        minDetectionConfidence: 0.5,
      })
      faceDetection.onResults((results: any) => drawFaceDetectionResults(results))
    } catch (err) {
      console.error('Failed to initialize Face Detection:', err)
      errorMessage.value = 'Head detection visualization failed. Results will still be available via JSON.'
    }
  } else {
    return // Skip if hands or face mesh detection failed for their respective endpoints
  }

  // Start processing video frames
  const processFrame = async () => {
    if (!videoElement.value || !isCameraActive.value) return
    try {
      if (pose) await pose.send({ image: videoElement.value })
      if (hands && !handsFailed.value) await hands.send({ image: videoElement.value })
      if (faceMesh && !faceMeshFailed.value) await faceMesh.send({ image: videoElement.value })
      if (faceDetection) await faceDetection.send({ image: videoElement.value })
    } catch (err) {
      console.error('Error processing frame:', err)
      errorMessage.value = 'Error processing video frame. Please try again.'
      stopDetection()
      return
    }
    rafId = requestAnimationFrame(processFrame)
  }

  processFrame()

  // Periodically send frames to backend for JSON results
  jsonInterval = setInterval(async () => {
    await fetchJsonResults(endpoint)
  }, 1000) // Fetch JSON every 1s
}

const stopDetection = () => {
  if (rafId) {
    cancelAnimationFrame(rafId)
    rafId = null
  }
  if (jsonInterval) {
    clearInterval(jsonInterval)
    jsonInterval = null
  }
  if (pose) {
    pose.close()
    pose = null
  }
  if (hands) {
    hands.close()
    hands = null
  }
  if (faceMesh) {
    faceMesh.close()
    faceMesh = null
  }
  if (faceDetection) {
    faceDetection.close()
    faceDetection = null
  }
}

const fetchJsonResults = async (endpoint: string) => {
  if (!videoElement.value) return

  const canvas = document.createElement('canvas')
  canvas.width = videoElement.value.videoWidth
  canvas.height = videoElement.value.videoHeight
  const ctx = canvas.getContext('2d')
  if (!ctx) return
  ctx.drawImage(videoElement.value, 0, 0, canvas.width, canvas.height)

  canvas.toBlob(async (blob) => {
    if (!blob) return

    const file = new File([blob], 'frame.jpg', { type: 'image/jpeg' })
    store.setFile(file)

    try {
      const response = await store.uploadImage(endpoint)
      result.value = response
      errorMessage.value = ''
    } catch (error: any) {
      console.error('Error fetching JSON:', error)
      result.value = { error: `Failed to fetch JSON results: ${error.message}` }
      errorMessage.value = 'JSON fetch failed. Check network or backend status.'
    }
  }, 'image/jpeg')
}

const drawPoseResults = (endpoint: string, results: any) => {
  if (!canvasElement.value) return
  const ctx = canvasElement.value.getContext('2d')
  if (!ctx) return

  ctx.clearRect(0, 0, canvasElement.value.width, canvasElement.value.height)
  ctx.strokeStyle = 'red'
  ctx.fillStyle = 'red'
  ctx.lineWidth = 2
  ctx.font = '16px Arial'

  if (!results.poseLandmarks) return

  const width = canvasElement.value.width
  const height = canvasElement.value.height
  const landmarks = results.poseLandmarks.map((lm: any) => ({
    x: lm.x * width,
    y: lm.y * height,
    z: lm.z,
  }))

  if (endpoint === 'arm') {
    const leftArm = [11, 13, 15].map(idx => landmarks[idx]) // Left shoulder, elbow, wrist
    const rightArm = [12, 14, 16].map(idx => landmarks[idx]) // Right shoulder, elbow, wrist

    ctx.beginPath()
    leftArm.forEach((lm: any, idx: number) => {
      if (idx === 0) ctx.moveTo(lm.x, lm.y)
      else ctx.lineTo(lm.x, lm.y)
      ctx.arc(lm.x, lm.y, 3, 0, 2 * Math.PI)
      ctx.fill()
    })
    ctx.stroke()

    ctx.beginPath()
    rightArm.forEach((lm: any, idx: number) => {
      if (idx === 0) ctx.moveTo(lm.x, lm.y)
      else ctx.lineTo(lm.x, lm.y)
      ctx.arc(lm.x, lm.y, 3, 0, 2 * Math.PI)
      ctx.fill()
    })
    ctx.stroke()
  } else if (endpoint === 'people') {
    const connections = [
      [11, 12],
      [11, 13],
      [13, 15],
      [12, 14],
      [14, 16], // Arms
      [23, 24],
      [11, 23],
      [12, 24],
      [23, 25],
      [24, 26], // Torso and legs
    ]
    connections.forEach(([i, j]) => {
      const lm1 = landmarks[i]
      const lm2 = landmarks[j]
      ctx.beginPath()
      ctx.moveTo(lm1.x, lm1.y)
      ctx.lineTo(lm2.x, lm2.y)
      ctx.stroke()
      ctx.arc(lm1.x, lm1.y, 3, 0, 2 * Math.PI)
      ctx.arc(lm2.x, lm2.y, 3, 0, 2 * Math.PI)
      ctx.fill()
    })
  }
}

const drawHandsResults = (results: any) => {
  if (!canvasElement.value) return
  const ctx = canvasElement.value.getContext('2d')
  if (!ctx) return

  ctx.clearRect(0, 0, canvasElement.value.width, canvasElement.value.height)
  ctx.strokeStyle = 'red'
  ctx.fillStyle = 'red'
  ctx.lineWidth = 2

  if (!results.multiHandLandmarks) return

  const width = canvasElement.value.width
  const height = canvasElement.value.height

  results.multiHandLandmarks.forEach((landmarks: any) => {
    const lm = landmarks.map((l: any) => ({
      x: l.x * width,
      y: l.y * height,
      z: l.z,
    }))
    const connections = [
      [0, 1, 2, 3, 4], // Thumb
      [0, 5, 6, 7, 8], // Index
      [0, 9, 10, 11, 12], // Middle
      [0, 13, 14, 15, 16], // Ring
      [0, 17, 18, 19, 20], // Pinky
    ]
    connections.forEach(conn => {
      ctx.beginPath()
      conn.forEach((idx: number, i: number) => {
        const l = lm[idx]
        if (i === 0) ctx.moveTo(l.x, l.y)
        else ctx.lineTo(l.x, l.y)
        ctx.arc(l.x, l.y, 3, 0, 2 * Math.PI)
        ctx.fill()
      })
      ctx.stroke()
    })
  })
}

const drawFaceMeshResults = (results: any) => {
  if (!canvasElement.value) return
  const ctx = canvasElement.value.getContext('2d')
  if (!ctx) return

  ctx.clearRect(0, 0, canvasElement.value.width, canvasElement.value.height)
  ctx.fillStyle = 'red'

  if (!results.multiFaceLandmarks || results.multiFaceLandmarks.length === 0) return

  const width = canvasElement.value.width
  const height = canvasElement.value.height

  results.multiFaceLandmarks.forEach((landmarks: any) => {
    const irisIndices = [...Array(6).keys()].map(i => 468 + i).concat([...Array(6).keys()].map(i => 474 + i))
    irisIndices.forEach(idx => {
      const lm = landmarks[idx]
      if (!lm) return // Skip if landmark is undefined
      const x = lm.x * width
      const y = lm.y * height
      ctx.beginPath()
      ctx.arc(x, y, 3, 0, 2 * Math.PI)
      ctx.fill()
    })
  })
}

const drawFaceDetectionResults = (results: any) => {
  if (!canvasElement.value) return
  const ctx = canvasElement.value.getContext('2d')
  if (!ctx) return

  ctx.clearRect(0, 0, canvasElement.value.width, canvasElement.value.height)
  ctx.strokeStyle = 'red'
  ctx.lineWidth = 2
  ctx.font = '16px Arial'
  ctx.fillStyle = 'red'

  if (!results.detections || results.detections.length === 0) return

  const width = canvasElement.value.width
  const height = canvasElement.value.height

  results.detections.forEach((detection: any) => {
    const bbox = detection.locationData.relativeBoundingBox
    const x = bbox.xmin * width
    const y = bbox.ymin * height
    const w = bbox.width * width
    const h = bbox.height * height

    ctx.beginPath()
    ctx.rect(x, y, w, h)
    ctx.stroke()
    ctx.fillText(`Confidence: ${(detection.score[0] * 100).toFixed(1)}%`, x, y - 10)
  })
}

const clearCanvas = () => {
  if (!canvasElement.value) return
  const ctx = canvasElement.value.getContext('2d')
  if (ctx) {
    ctx.clearRect(0, 0, canvasElement.value.width, canvasElement.value.height)
  }
}

// Upload Mode Functions
const handleImageUpload = (event: Event) => {
  const input = event.target as HTMLInputElement
  if (input.files && input.files[0]) {
    const file = input.files[0]
    const reader = new FileReader()
    reader.onload = (e) => {
      uploadedImage.value = e.target?.result as string
      store.setFile(file)
      result.value = null
      errorMessage.value = ''
    }
    reader.readAsDataURL(file)
  }
}

const detectUploadedImage = async (endpoint: string) => {
  if (!store.file) {
    errorMessage.value = 'Please upload an image first.'
    return
  }

  try {
    const response = await store.uploadImage(endpoint)
    result.value = response
    errorMessage.value = ''
  } catch (error: any) {
    console.error('Error detecting image:', error)
    result.value = { error: `Failed to detect image: ${error.message}` }
    errorMessage.value = 'Detection failed. Check network or backend status.'
  }
}

onUnmounted(() => {
  stopCamera()
})
</script>
