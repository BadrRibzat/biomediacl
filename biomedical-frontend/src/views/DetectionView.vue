<template>
  <div class="container mx-auto p-4">
    <h1 class="text-3xl font-bold mb-4">Detection</h1>
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
      <button @click="toggleDetection('arm-fingers')" class="bg-blue-500 hover:bg-blue-700 text-white p-2 rounded" :disabled="!isCameraActive">
        {{ activeDetection === 'arm-fingers' ? 'Stop Arm-Fingers Detection' : 'Detect Arm-Fingers' }}
      </button>
      <button @click="toggleDetection('eyes')" class="bg-blue-500 hover:bg-blue-700 text-white p-2 rounded" :disabled="!isCameraActive">
        {{ activeDetection === 'eyes' ? 'Stop Eyes Detection' : 'Detect Eyes' }}
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
    <div v-if="result" class="mt-4">
      <h2 class="text-xl font-semibold">Result</h2>
      <pre class="bg-gray-100 p-4 rounded">{{ result }}</pre>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onUnmounted, onMounted } from 'vue'
import { useDetectionStore } from '../stores/detection'

// Load MediaPipe scripts dynamically
onMounted(() => {
  const loadScript = (src: string) => {
    return new Promise((resolve, reject) => {
      const script = document.createElement('script')
      script.src = src
      script.onload = resolve
      script.onerror = reject
      document.head.appendChild(script)
    })
  }

  Promise.all([
    loadScript('https://cdn.jsdelivr.net/npm/@mediapipe/pose@0.5/pose.min.js'),
    loadScript('https://cdn.jsdelivr.net/npm/@mediapipe/hands@0.4/hands.min.js'),
    loadScript('https://cdn.jsdelivr.net/npm/@mediapipe/face_mesh@0.4/face_mesh.min.js'),
    loadScript('https://cdn.jsdelivr.net/npm/@mediapipe/face_detection@0.4/face_detection.min.js')
  ]).catch(err => {
    console.error('Failed to load MediaPipe scripts:', err)
    errorMessage.value = 'Failed to load detection libraries. Please check your internet connection.'
  })
})

const store = useDetectionStore()
const videoElement = ref<HTMLVideoElement | null>(null)
const canvasElement = ref<HTMLCanvasElement | null>(null)
const isCameraActive = ref(false)
const errorMessage = ref('')
const result = ref(null)
const activeDetection = ref<string | null>(null)
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

const startCamera = async () => {
  try {
    stream = await navigator.mediaDevices.getUserMedia({ video: true })
    if (videoElement.value) {
      videoElement.value.srcObject = stream
      isCameraActive.value = true
      errorMessage.value = ''
      if (canvasElement.value) {
        canvasElement.value.width = videoElement.value.videoWidth
        canvasElement.value.height = videoElement.value.videoHeight
      }
    }
  } catch (error) {
    console.error('Error accessing camera:', error)
    errorMessage.value = 'Failed to access camera. Please grant permission or check device compatibility.'
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
    pose = new window.Pose({
      locateFile: (file: string) => `https://cdn.jsdelivr.net/npm/@mediapipe/pose@0.5/${file}`
    })
    pose.setOptions({
      modelComplexity: 1,
      minDetectionConfidence: 0.5,
      minTrackingConfidence: 0.5
    })
    pose.onResults((results: any) => drawPoseResults(endpoint, results))
  } else if (endpoint === 'arm-fingers') {
    hands = new window.Hands({
      locateFile: (file: string) => `https://cdn.jsdelivr.net/npm/@mediapipe/hands@0.4/${file}`
    })
    hands.setOptions({
      maxNumHands: 2,
      minDetectionConfidence: 0.5,
      minTrackingConfidence: 0.5
    })
    hands.onResults((results: any) => drawHandsResults(results))
  } else if (endpoint === 'eyes') {
    faceMesh = new window.FaceMesh({
      locateFile: (file: string) => `https://cdn.jsdelivr.net/npm/@mediapipe/face_mesh@0.4/${file}`
    })
    faceMesh.setOptions({
      maxNumFaces: 1,
      refineLandmarks: true,
      minDetectionConfidence: 0.5,
      minTrackingConfidence: 0.5
    })
    faceMesh.onResults((results: any) => drawFaceMeshResults(results))
  } else if (endpoint === 'head') {
    faceDetection = new window.FaceDetection({
      locateFile: (file: string) => `https://cdn.jsdelivr.net/npm/@mediapipe/face_detection@0.4/${file}`
    })
    faceDetection.setOptions({
      minDetectionConfidence: 0.5
    })
    faceDetection.onResults((results: any) => drawFaceDetectionResults(results))
  }

  // Start processing video frames
  const processFrame = async () => {
    if (!videoElement.value || !isCameraActive.value) return
    if (pose) await pose.send({ image: videoElement.value })
    if (hands) await hands.send({ image: videoElement.value })
    if (faceMesh) await faceMesh.send({ image: videoElement.value })
    if (faceDetection) await faceDetection.send({ image: videoElement.value })
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
    } catch (error) {
      console.error('Error fetching JSON:', error)
      result.value = { error: 'Failed to fetch JSON results' }
      errorMessage.value = 'JSON fetch failed. Check console for details.'
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
    z: lm.z
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
      [11, 12], [11, 13], [13, 15], [12, 14], [14, 16], // Arms
      [23, 24], [11, 23], [12, 24], [23, 25], [24, 26], // Torso and legs
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
    // People count will be updated via JSON
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
      z: l.z
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

  if (!results.multiFaceLandmarks) return

  const width = canvasElement.value.width
  const height = canvasElement.value.height

  results.multiFaceLandmarks.forEach((landmarks: any) => {
    const irisIndices = [...Array(6).keys()].map(i => 468 + i).concat([...Array(6).keys()].map(i => 474 + i))
    irisIndices.forEach(idx => {
      const lm = landmarks[idx]
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
  ctx.fillStyle = 'red'
  ctx.lineWidth = 2
  ctx.font = '16px Arial'

  if (!results.detections) return

  const width = canvasElement.value.width
  const height = canvasElement.value.height

  results.detections.forEach((detection: any) => {
    const bbox = detection.boundingBox
    const x = bbox.originX * width
    const y = bbox.originY * height
    const w = bbox.width * width
    const h = bbox.height * height
    ctx.beginPath()
    ctx.rect(x, y, w, h)
    ctx.stroke()
    // Confidence will be updated via JSON
  })
}

const clearCanvas = () => {
  if (!canvasElement.value) return
  const ctx = canvasElement.value.getContext('2d')
  if (ctx) {
    ctx.clearRect(0, 0, canvasElement.value.width, canvasElement.value.height)
  }
}

onUnmounted(() => {
  stopCamera()
})
</script>
