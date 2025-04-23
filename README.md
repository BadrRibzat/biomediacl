Biomedical Detection Tutorial
This is an open-source project tutorial for object detection in biomedical engineering, designed for educational purposes. It uses real-time laptop camera input to detect eyes, head, arms, arm-fingers, and count people, with a user-friendly frontend interface.
Features

Real-time detection:
Eyes Detection (using MediaPipe Face Mesh)
Head Detection (using MediaPipe Face Detection)
Arm Detection (using MediaPipe Pose)
Arm-Fingers Detection (using MediaPipe Hands)
People Counting (using MediaPipe Pose)


Frontend interface with buttons for each detection test (in progress)
Built with Python, Tkinter, OpenCV, MediaPipe, Nuxt.js, and TailwindCSS
Deployed on Fly.io (backend) and Vercel (frontend, planned)

Prerequisites

Ubuntu 20.04 LTS (or compatible system)
Miniconda installed
Node.js and npm installed (for frontend)
Git installed

Setup Instructions
Backend Setup

Clone the repository:
git clone https://github.com/BadrRibzat/biomediacl.git
cd biomediacl


Create and activate a Conda environment:
conda create -n biomedical python=3.11
conda activate biomedical


Install dependencies:
conda install opencv
pip install mediapipe


Run any detection script:
python eyes_detection.py
python head_detection.py
python arm_detection.py
python arm_fingers_detection.py
python people_counting.py



Frontend Setup

(In progress) Create a Nuxt.js project:
npx create-nuxt-app biomedical-frontend
cd biomedical-frontend
npm install


Copy the provided index.vue to pages/index.vue (to be provided).

Run the development server:
npm run dev



Deployment

Backend: Deploy to Fly.io (instructions TBD).
Frontend: Deploy to Vercel (instructions TBD).

Contributing
This is an open-source project. Feel free to fork, contribute, or suggest improvements!
License
MIT License

