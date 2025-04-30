<template>
  <div class="container mx-auto px-4 py-8">
    <div class="text-center mb-8">
      <h1 class="text-3xl font-bold text-gray-900 mb-2">Biomedical Detection</h1>
      <p class="text-lg text-gray-600 max-w-2xl mx-auto">
        Real-time detection of biomedical features using computer vision and AI models.
      </p>
    </div>

    <!-- Mode selection -->
    <div class="bg-white rounded-lg shadow-md p-6 mb-8">
      <h2 class="text-xl font-semibold text-gray-800 mb-4">Detection Mode</h2>
      <div class="flex flex-wrap gap-2">
        <button
          @click="setMode('camera')"
          class="px-4 py-2 rounded-md transition-colors"
          :class="mode === 'camera' 
            ? 'bg-primary-600 text-white shadow-md' 
            : 'bg-gray-100 text-gray-700 hover:bg-gray-200'"
        >
          <span class="flex items-center">
            <VideoCameraIcon class="h-5 w-5 mr-2" />
            Camera Mode
          </span>
        </button>
        <button
          @click="setMode('upload')"
          class="px-4 py-2 rounded-md transition-colors"
          :class="mode === 'upload' 
            ? 'bg-primary-600 text-white shadow-md' 
            : 'bg-gray-100 text-gray-700 hover:bg-gray-200'"
        >
          <span class="flex items-center">
            <ArrowUpTrayIcon class="h-5 w-5 mr-2" />
            Upload Image
          </span>
        </button>
      </div>
    </div>

    <!-- Camera Mode -->
    <div v-if="mode === 'camera'" class="bg-white rounded-lg shadow-md p-6 mb-8">
      <div class="flex flex-wrap gap-4 mb-6">
        <button 
          @click="startCamera" 
          class="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 transition-colors flex items-center"
          :disabled="isCameraActive"
        >
          <PlayIcon class="h-5 w-5 mr-2" />
          {{ isCameraActive ? 'Camera Active' : 'Start Camera' }}
        </button>
        <button 
          @click="stopCamera" 
          class="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 transition-colors flex items-center"
          :disabled="!isCameraActive"
        >
          <StopIcon class="h-5 w-5 mr-2" />
          Stop Camera
        </button>
      </div>

      <!-- Camera feed -->
      <div class="relative mb-6">
        <video 
          ref="videoElement" 
          autoplay 
          playsinline
          class="w-full max-w-2xl mx-auto border-2 border-gray-200 rounded-lg shadow-sm"
          v-show="isCameraActive"
        ></video>
        <canvas 
          ref="canvasElement" 
          class="absolute top-0 left-1/2 transform -translate-x-1/2 w-full max-w-2xl h-full border-2 border-transparent"
          v-show="isCameraActive"
        ></canvas>
        
        <div v-if="!isCameraActive" class="w-full max-w-2xl mx-auto h-64 bg-gray-100 rounded-lg flex items-center justify-center">
          <div class="text-center p-4">
            <CameraIcon class="h-12 w-12 mx-auto text-gray-400 mb-2" />
            <p class="text-gray-500">Camera is inactive. Click "Start Camera" to begin.</p>
          </div>
        </div>
      </div>

      <!-- Detection controls -->
      <div v-if="isCameraActive" class="bg-gray-50 rounded-lg p-4 mb-6">
        <h3 class="text-lg font-medium text-gray-800 mb-3">Detection Options</h3>
        
        <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-3">
          <button
            v-for="option in detectionOptions"
            :key="option.id"
            @click="toggleDetection(option.id)"
            class="px-3 py-2 rounded-md transition-colors flex items-center justify-center"
            :class="[
              activeDetection === option.id 
                ? 'bg-primary-600 text-white shadow-md' 
                : 'bg-white text-gray-700 hover:bg-gray-100 border border-gray-200',
              option.disabled ? 'opacity-50 cursor-not-allowed' : ''
            ]"
            :disabled="option.disabled"
          >
            <component :is="option.icon" class="h-5 w-5 mr-2" />
            {{ activeDetection === option.id ? `Stop ${option.label}` : option.label }}
            <span v-if="option.failed" class="ml-2 text-xs text-red-500">(Failed)</span>
          </button>
        </div>
      </div>

      <!-- Error message -->
      <div v-if="errorMessage" class="bg-red-50 border-l-4 border-red-400 p-4 mb-6">
        <div class="flex">
          <div class="flex-shrink-0">
            <ExclamationCircleIcon class="h-5 w-5 text-red-400" />
          </div>
          <div class="ml-3">
            <p class="text-sm text-red-700">{{ errorMessage }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Upload Mode -->
    <div v-if="mode === 'upload'" class="bg-white rounded-lg shadow-md p-6 mb-8">
      <div class="mb-6">
        <label class="block text-sm font-medium text-gray-700 mb-2">Upload Image</label>
        <div class="mt-1 flex justify-center px-6 pt-5 pb-6 border-2 border-gray-300 border-dashed rounded-md">
          <div class="space-y-1 text-center">
            <div class="flex text-sm text-gray-600 justify-center">
              <label
                for="file-upload"
                class="relative cursor-pointer bg-white rounded-md font-medium text-primary-600 hover:text-primary-500 focus-within:outline-none"
              >
                <span>Upload a file</span>
                <input 
                  id="file-upload" 
                  name="file-upload" 
                  type="file" 
                  class="sr-only" 
                  @change="handleImageUpload" 
                  accept="image/*"
                />
              </label>
              <p class="pl-1">or drag and drop</p>
            </div>
            <p class="text-xs text-gray-500">PNG, JPG up to 5MB</p>
          </div>
        </div>
      </div>

      <!-- Preview and detection buttons -->
      <div v-if="uploadedImage" class="mb-6">
        <div class="flex flex-wrap gap-4 mb-4">
          <button
            v-for="option in detectionOptions"
            :key="option.id"
            @click="detectUploadedImage(option.id)"
            class="px-3 py-2 rounded-md transition-colors flex items-center justify-center"
            :class="[
              activeDetection === option.id 
                ? 'bg-primary-600 text-white shadow-md' 
                : 'bg-white text-gray-700 hover:bg-gray-100 border border-gray-200',
              option.disabled ? 'opacity-50 cursor-not-allowed' : ''
            ]"
            :disabled="option.disabled"
          >
            <component :is="option.icon" class="h-5 w-5 mr-2" />
            Detect {{ option.label }}
            <span v-if="option.failed" class="ml-2 text-xs text-red-500">(Failed)</span>
          </button>
        </div>

        <div class="relative">
          <img 
            :src="uploadedImage" 
            class="w-full max-w-2xl mx-auto border-2 border-gray-200 rounded-lg shadow-sm"
            alt="Uploaded image"
          />
          <canvas 
            ref="uploadCanvasElement" 
            class="absolute top-0 left-1/2 transform -translate-x-1/2 w-full max-w-2xl h-full border-2 border-transparent"
          ></canvas>
        </div>
      </div>
    </div>

    <!-- Results section -->
    <div v-if="result" class="bg-white rounded-lg shadow-md p-6">
      <h2 class="text-xl font-semibold text-gray-800 mb-4">Detection Results</h2>
      
      <div class="mb-4">
        <div class="flex items-center mb-2">
          <CheckBadgeIcon class="h-5 w-5 text-green-500 mr-2" />
          <span class="font-medium">Status:</span>
          <span class="ml-2 text-gray-700">{{ result.status }}</span>
        </div>
        
        <div v-if="'count' in result" class="flex items-center mb-2">
          <UsersIcon class="h-5 w-5 text-blue-500 mr-2" />
          <span class="font-medium">People Count:</span>
          <span class="ml-2 text-gray-700">{{ result.count }}</span>
        </div>
      </div>

      <!-- Detailed results -->
      <div class="bg-gray-50 rounded-lg p-4">
        <h3 class="text-lg font-medium text-gray-800 mb-2">Detailed Data</h3>
        <pre class="bg-gray-100 p-4 rounded-md overflow-x-auto text-sm">{{ JSON.stringify(result, null, 2) }}</pre>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onUnmounted, onMounted, computed } from 'vue'
import { useDetectionStore } from '../stores/detection'
import VideoCameraIcon from '@heroicons/vue/24/outline/VideoCameraIcon'
import ArrowUpTrayIcon from '@heroicons/vue/24/outline/ArrowUpTrayIcon'
import PlayIcon from '@heroicons/vue/24/outline/PlayIcon'
import StopIcon from '@heroicons/vue/24/outline/StopIcon'
import CameraIcon from '@heroicons/vue/24/outline/CameraIcon'
import ExclamationCircleIcon from '@heroicons/vue/24/outline/ExclamationCircleIcon'
import CheckBadgeIcon from '@heroicons/vue/24/outline/CheckBadgeIcon'
import UsersIcon from '@heroicons/vue/24/outline/UsersIcon'
import HandRaisedIcon from '@heroicons/vue/24/outline/HandRaisedIcon'
import EyeIcon from '@heroicons/vue/24/outline/EyeIcon'
import UserIcon from '@heroicons/vue/24/outline/UserIcon'
import IdentificationIcon from '@heroicons/vue/24/outline/IdentificationIcon'
import ArrowPathIcon from '@heroicons/vue/24/outline/ArrowPathIcon'

declare global {
  interface Window {
    Pose: any
    Hands: any
    FaceMesh: any
    FaceDetection: any
  }
}

const store = useDetectionStore()
const videoElement = ref<HTMLVideoElement | null>(null)
const canvasElement = ref<HTMLCanvasElement | null>(null)
const uploadCanvasElement = ref<HTMLCanvasElement | null>(null)
const isCameraActive = ref(false)
const result = ref<any>(null)
const activeDetection = ref<string | null>(null)
const mode = ref<'camera' | 'upload'>('camera')
const uploadedImage = ref<string | null>(null)
const errorMessage = ref('')
const handsFailed = ref(false)
const faceMeshFailed = ref(false)
const faceDetectionFailed = ref(false)

let stream: MediaStream | null = null
let pose: any | null = null
let hands: any | null = null
let faceMesh: any | null = null
let faceDetection: any | null = null
let rafId: number | null = null
let jsonInterval: number | null = null

const detectionOptions = computed(() => [
  { 
    id: 'arm', 
    label: 'Arm', 
    icon: HandRaisedIcon,
    disabled: !isCameraActive.value && mode.value === 'camera',
    failed: false
  },
  { 
    id: 'arm-fingers', 
    label: 'Arm & Fingers', 
    icon: IdentificationIcon,
    disabled: (!isCameraActive.value && mode.value === 'camera') || handsFailed.value,
    failed: handsFailed.value
  },
  { 
    id: 'eyes', 
    label: 'Eyes', 
    icon: EyeIcon,
    disabled: (!isCameraActive.value && mode.value === 'camera') || faceMeshFailed.value,
    failed: faceMeshFailed.value
  },
  { 
    id: 'head', 
    label: 'Head', 
    icon: UserIcon,
    disabled: (!isCameraActive.value && mode.value === 'camera') || faceDetectionFailed.value,
    failed: faceDetectionFailed.value
  },
  { 
    id: 'people', 
    label: 'People', 
    icon: UsersIcon,
    disabled: !isCameraActive.value && mode.value === 'camera',
    failed: false
  }
])

onMounted(async () => {
  try {
    await Promise.all([
      loadScript('/mediapipe/pose.min.js'),
      loadScript('/mediapipe/hands.min.js'),
      loadScript('/mediapipe/face_mesh.min.js'),
      loadScript('/mediapipe/face_detection.min.js')
    ])
    console.log('All MediaPipe scripts loaded successfully')
  } catch (err) {
    console.error('Error loading MediaPipe scripts:', err)
    errorMessage.value = 'Failed to load detection libraries. Please refresh the page.'
  }
})

const loadScript = (src: string, retryCount = 3, delay = 1000): Promise<void> => {
  return new Promise((resolve, reject) => {
    const attemptLoad = (attemptsLeft: number) => {
      const script = document.createElement('script')
      script.src = src
      script.onload = () => resolve()
      script.onerror = () => {
        if (attemptsLeft > 0) {
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

const setMode = (newMode: 'camera' | 'upload') => {
  mode.value = newMode
  stopCamera()
  uploadedImage.value = null
  result.value = null
  errorMessage.value = ''
}

const startCamera = async () => {
  try {
    stream = await navigator.mediaDevices.getUserMedia({
      video: { 
        facingMode: 'user', 
        width: { ideal: 1280 }, 
        height: { ideal: 720 } 
      },
      audio: false
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
    }
  } catch (error: any) {
    console.error('Error accessing camera:', error)
    handleCameraError(error)
  }
}

const handleCameraError = (error: any) => {
  let message = 'Error accessing camera'
  
  switch(error.name) {
    case 'NotAllowedError':
      message = 'Camera access denied. Please grant camera permissions.'
      break
    case 'NotFoundError':
      message = 'No camera found. Please connect a camera or use upload mode.'
      break
    case 'NotReadableError':
      message = 'Camera is in use by another application. Please close other apps.'
      break
    case 'OverconstrainedError':
      message = 'Camera constraints could not be satisfied. Try different settings.'
      break
    default:
      message = `Camera error: ${error.message}`
  }
  
  errorMessage.value = message
}

const stopCamera = () => {
  if (stream) {
    stream.getTracks().forEach(track => track.stop())
    stream = null
  }
  
  isCameraActive.value = false
  activeDetection.value = null
  
  if (videoElement.value) {
    videoElement.value.srcObject = null
  }
  
  stopDetection()
  clearCanvas()
  
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

  try {
    switch(endpoint) {
      case 'arm':
      case 'people':
        pose = new window.Pose({
          locateFile: (file: string) => `/mediapipe/${file}`
        })
        pose.setOptions({
          modelComplexity: 1,
          minDetectionConfidence: 0.5,
          minTrackingConfidence: 0.5
        })
        pose.onResults((results: any) => drawPoseResults(endpoint, results))
        break
        
      case 'arm-fingers':
        if (handsFailed.value) return
        hands = new window.Hands({
          locateFile: (file: string) => `/mediapipe/${file}`
        })
        hands.setOptions({
          maxNumHands: 2,
          minDetectionConfidence: 0.5,
          minTrackingConfidence: 0.5
        })
        hands.onResults((results: any) => drawHandsResults(results))
        break
        
      case 'eyes':
        if (faceMeshFailed.value) return
        faceMesh = new window.FaceMesh({
          locateFile: (file: string) => `/mediapipe/${file}`
        })
        faceMesh.setOptions({
          maxNumFaces: 1,
          refineLandmarks: true,
          minDetectionConfidence: 0.5,
          minTrackingConfidence: 0.5
        })
        faceMesh.onResults((results: any) => drawFaceMeshResults(results))
        break
        
      case 'head':
        faceDetection = new window.FaceDetection({
          locateFile: (file: string) => `/mediapipe/${file}`
        })
        faceDetection.setOptions({
          minDetectionConfidence: 0.3
        })
        faceDetection.onResults((results: any) => drawFaceDetectionResults(results))
        break
    }

    const processFrame = async () => {
      if (!videoElement.value || !isCameraActive.value) return
      
      try {
        if (pose && (endpoint === 'arm' || endpoint === 'people')) {
          await pose.send({ image: videoElement.value })
        }
        if (hands && endpoint === 'arm-fingers' && !handsFailed.value) {
          await hands.send({ image: videoElement.value })
        }
        if (faceMesh && endpoint === 'eyes' && !faceMeshFailed.value) {
          await faceMesh.send({ image: videoElement.value })
        }
        if (faceDetection && endpoint === 'head') {
          await faceDetection.send({ image: videoElement.value })
        }
      } catch (err) {
        console.error('Error processing frame:', err)
        errorMessage.value = 'Error processing video frame. Please try again.'
        stopDetection()
        return
      }
      
      rafId = requestAnimationFrame(processFrame)
    }

    processFrame()

    jsonInterval = setInterval(async () => {
      await fetchJsonResults(endpoint)
    }, 1000)
  } catch (err) {
    console.error('Error initializing detection:', err)
    errorMessage.value = `Failed to initialize ${endpoint} detection. Please try again.`
    activeDetection.value = null
  }
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
}

const clearCanvas = () => {
  const canvas = mode.value === 'camera' ? canvasElement.value : uploadCanvasElement.value
  if (!canvas) return
  
  const ctx = canvas.getContext('2d')
  if (ctx) {
    ctx.clearRect(0, 0, canvas.width, canvas.height)
  }
}

const drawPoseResults = (endpoint: string, results: any) => {
  const canvas = mode.value === 'camera' ? canvasElement.value : uploadCanvasElement.value
  if (!canvas) return
  
  const ctx = canvas.getContext('2d')
  if (!ctx || !results.poseLandmarks) return

  const video = mode.value === 'camera' ? videoElement.value : null
  if (video && (canvas.width !== video.videoWidth || canvas.height !== video.videoHeight)) {
    canvas.width = video.videoWidth
    canvas.height = video.videoHeight
  }

  ctx.clearRect(0, 0, canvas.width, canvas.height)
  
  const width = canvas.width
  const height = canvas.height
  const landmarks = results.poseLandmarks.map((lm: any) => ({
    x: lm.x * width,
    y: lm.y * height,
    z: lm.z,
    visibility: lm.visibility
  }))

  if (endpoint === 'arm') {
    drawArm(ctx, landmarks, [11, 13, 15], 'red')
    drawArm(ctx, landmarks, [12, 14, 16], 'blue')
  } else if (endpoint === 'people') {
    drawFullPose(ctx, landmarks)
  }
}

const drawArm = (ctx: CanvasRenderingContext2D, landmarks: any[], indices: number[], color: string) => {
  ctx.strokeStyle = color
  ctx.fillStyle = color
  ctx.lineWidth = 2

  ctx.beginPath()
  indices.forEach((idx, i) => {
    const lm = landmarks[idx]
    if (lm.visibility < 0.5) return
    
    if (i === 0) ctx.moveTo(lm.x, lm.y)
    else ctx.lineTo(lm.x, lm.y)
    
    ctx.beginPath()
    ctx.arc(lm.x, lm.y, 4, 0, 2 * Math.PI)
    ctx.fill()
  })
  ctx.stroke()
}

const drawFullPose = (ctx: CanvasRenderingContext2D, landmarks: any[]) => {
  const connections = [
    [11, 12], [11, 13], [13, 15], [12, 14], [14, 16],
    [11, 23], [12, 24], [23, 24], [23, 25], [24, 26]
  ]

  ctx.strokeStyle = 'rgba(0, 255, 0, 0.6)'
  ctx.fillStyle = 'rgba(0, 255, 0, 0.6)'
  ctx.lineWidth = 2

  connections.forEach(([i, j]) => {
    const lm1 = landmarks[i]
    const lm2 = landmarks[j]
    
    if (lm1.visibility < 0.5 || lm2.visibility < 0.5) return
    
    ctx.beginPath()
    ctx.moveTo(lm1.x, lm1.y)
    ctx.lineTo(lm2.x, lm2.y)
    ctx.stroke()
  })

  landmarks.forEach((lm, idx) => {
    if (lm.visibility < 0.5) return
    
    ctx.beginPath()
    ctx.arc(lm.x, lm.y, 3, 0, 2 * Math.PI)
    ctx.fill()
  })
}

const drawHandsResults = (results: any) => {
  const canvas = mode.value === 'camera' ? canvasElement.value : uploadCanvasElement.value
  if (!canvas) return
  
  const ctx = canvas.getContext('2d')
  if (!ctx || !results.multiHandLandmarks) return

  ctx.clearRect(0, 0, canvas.width, canvas.height)
  
  const width = canvas.width
  const height = canvas.height

  results.multiHandLandmarks.forEach((landmarks: any, idx: number) => {
    const handedness = results.multiHandedness[idx].classification[0].label
    const color = handedness === 'Left' ? 'rgba(255, 0, 0, 0.8)' : 'rgba(0, 0, 255, 0.8)'
    
    ctx.fillStyle = color
    landmarks.forEach((lm: any) => {
      const x = lm.x * width
      const y = lm.y * height
      ctx.beginPath()
      ctx.arc(x, y, 3, 0, 2 * Math PI)
      ctx.fill()
    })

    ctx.strokeStyle = color
    ctx.lineWidth = 2
    
    const palmConnections = [
      [0, 1, 2, 5, 9, 13, 17, 0],
      [1, 5], [5, 9], [9, 13], [13, 17], [17, 0]
    ]
    
    palmConnections.forEach(conn => {
      ctx.beginPath()
      conn.forEach((idx, i) => {
        const lm = landmarks[idx]
        const x = lm.x * width
        const y = lm.y * height
        if (i === 0) ctx.moveTo(x, y)
        else ctx.lineTo(x, y)
      })
      ctx.stroke()
    })

    const fingers = [
      [0, 1, 2, 3, 4],
      [0, 5, 6, 7, 8],
      [0, 9, 10, 11, 12],
      [0, 13, 14, 15, 16],
      [0, 17, 18, 19, 20]
    ]
    
    fingers.forEach(finger => {
      ctx.beginPath()
      finger.forEach((idx, i) => {
        const lm = landmarks[idx]
        const x = lm.x * width
        const y = lm.y * height
        if (i === 0) ctx.moveTo(x, y)
        else ctx.lineTo(x, y)
      })
      ctx.stroke()
    })
  })
}

const drawFaceMeshResults = (results: any) => {
  const canvas = mode.value === 'camera' ? canvasElement.value : uploadCanvasElement.value
  if (!canvas) return
  
  const ctx = canvas.getContext('2d')
  if (!ctx || !results.multiFaceLandmarks) return

  ctx.clearRect(0, 0, canvas.width, canvas.height)
  
  const width = canvas.width
  const height = canvas.height

  results.multiFaceLandmarks.forEach((landmarks: any) => {
    ctx.fillStyle = 'rgba(0, 255, 255, 0.8)'
    
    const leftIrisIndices = Array.from({length: 6}, (_, i) => 468 + i)
    const rightIrisIndices = Array.from({length: 6}, (_, i) => 474 + i)
    
    leftIrisIndices.concat(rightIrisIndices).forEach(idx => {
      const lm = landmarks[idx]
      if (!lm) return
      
      const x = lm.x * width
      const y = lm.y * height
      ctx.beginPath()
      ctx.arc(x, y, 2, 0, 2 * Math.PI)
      ctx.fill()
    })
  })
}

const drawFaceDetectionResults = (results: any) => {
  const canvas = mode.value === 'camera' ? canvasElement.value : uploadCanvasElement.value
  if (!canvas) return
  
  const ctx = canvas.getContext('2d')
  if (!ctx || !results.detections) return

  ctx.clearRect(0, 0, canvas.width, canvas.height)
  
  const width = canvas.width
  const height = canvas.height

  results.detections.forEach((detection: any) => {
    const bbox = detection.locationData.relativeBoundingBox
    const x = bbox.xmin * width
    const y = bbox.ymin * height
    const w = bbox.width * width
    const h = bbox.height * height

    ctx.strokeStyle = 'rgba(255, 165, 0, 0.8)'
    ctx.lineWidth = 2
    ctx.beginPath()
    ctx.rect(x, y, w, h)
    ctx.stroke()

    ctx.fillStyle = 'rgba(255, 165, 0, 0.8)'
    ctx.font = '14px Arial'
    ctx.fillText(`Confidence: ${(detection.score[0] * 100).toFixed(1)}%`, x, y - 10)

    if (detection.locationData.relativeKeypoints) {
      ctx.fillStyle = 'rgba(255, 0, 0, 0.8)'
      detection.locationData.relativeKeypoints.forEach((kp: any) => {
        const kpX = kp.x * width
        const kpY = kp.y * height
        ctx.beginPath()
        ctx.arc(kpX, kpY, 3, 0, 2 * Math.PI)
        ctx.fill()
      })
    }
  })
}

const fetchJsonResults = async (endpoint: string) => {
  try {
    let imageSource: HTMLVideoElement | HTMLImageElement | null = null
    
    if (mode.value === 'camera') {
      if (!videoElement.value) return
      imageSource = videoElement.value
    } else {
      if (!uploadedImage.value) return
      const img = new Image()
      img.src = uploadedImage.value!
      await new Promise((resolve) => {
        img.onload = resolve
      })
      imageSource = img
    }

    if (!imageSource) return
    
    const canvas = document.createElement('canvas')
    // Use type guard to handle HTMLVideoElement vs HTMLImageElement
    if (imageSource instanceof HTMLVideoElement) {
      canvas.width = imageSource.videoWidth
      canvas.height = imageSource.videoHeight
    } else {
      canvas.width = imageSource.naturalWidth
      canvas.height = imageSource.naturalHeight
    }
    
    const ctx = canvas.getContext('2d')
    if (!ctx) return
    
    ctx.drawImage(imageSource, 0, 0, canvas.width, canvas.height)
    
    const blob = await new Promise<Blob | null>((resolve) => {
      canvas.toBlob(resolve, 'image/jpeg', 0.9)
    })
    
    if (!blob) return
    
    const file = new File([blob], 'frame.jpg', { type: 'image/jpeg' })
    store.setFile(file)

    const response = await store.uploadImage(endpoint)
    result.value = response
    errorMessage.value = ''
    
  } catch (error: any) {
    console.error('Error fetching JSON:', error)
    result.value = { error: `Failed to fetch results: ${error.message}` }
    errorMessage.value = 'Detection failed. Check network or backend status.'
  }
}

const handleImageUpload = (event: Event) => {
  const input = event.target as HTMLInputElement
  if (!input.files || !input.files[0]) return
  
  const file = input.files[0]
  if (file.size > 5 * 1024 * 1024) {
    errorMessage.value = 'Image size exceeds 5MB limit'
    return
  }
  
  const reader = new FileReader()
  reader.onload = (e) => {
    uploadedImage.value = e.target?.result as string
    store.setFile(file)
    result.value = null
    errorMessage.value = ''
    
    if (uploadCanvasElement.value) {
      const img = new Image()
      img.onload = () => {
        uploadCanvasElement.value!.width = img.width
        uploadCanvasElement.value!.height = img.height
      }
      img.src = uploadedImage.value
    }
  }
  reader.readAsDataURL(file)
}

const detectUploadedImage = async (endpoint: string) => {
  if (!store.file) {
    errorMessage.value = 'Please upload an image first'
    return
  }

  try {
    activeDetection.value = endpoint
    
    if (endpoint === 'arm-fingers' && !handsFailed.value && uploadCanvasElement.value) {
      if (!hands) {
        hands = new window.Hands({
          locateFile: (file: string) => `/mediapipe/${file}`
        })
        hands.setOptions({
          maxNumHands: 2,
          minDetectionConfidence: 0.5,
          minTrackingConfidence: 0.5
        })
        hands.onResults((results: any) => drawHandsResults(results))
      }
      
      if (uploadedImage.value) {
        const img = new Image()
        img.onload = () => {
          hands.send({ image: img })
        }
        img.src = uploadedImage.value
      }
    }

    const response = await store.uploadImage(endpoint)
    result.value = response
    errorMessage.value = ''
    
  } catch (error: any) {
    console.error('Error detecting image:', error)
    result.value = { error: `Detection failed: ${error.message}` }
    errorMessage.value = 'Detection failed. Check network or backend status.'
    activeDetection.value = null
  }
}

onUnmounted(() => {
  stopCamera()
})
</script>

<style scoped>
.container {
  max-width: 1200px;
}

video, canvas {
  display: block;
  margin: 0 auto;
  background: #f3f4f6;
}

canvas {
  pointer-events: none;
}

pre {
  font-family: 'Fira Code', monospace;
  font-size: 0.875rem;
  line-height: 1.5;
}
</style>
