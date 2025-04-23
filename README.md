# Biomedical Detection Tutorial

This is an open-source project tutorial for object detection in biomedical engineering, designed for educational purposes. It provides a FastAPI backend for detecting eyes, head, arms, arm-fingers, and counting people, with a planned frontend interface.

## Features

- **Real-time detection** (backend):
  - Eyes Detection (using MediaPipe Face Mesh)
  - Head Detection (using MediaPipe Face Detection)
  - Arm Detection (using MediaPipe Pose)
  - Arm-Fingers Detection (using MediaPipe Hands)
  - People Counting (using MediaPipe Pose)
- FastAPI backend deployed on Fly.io
- Planned frontend with Vue 3 and TailwindCSS
- Dockerized for easy deployment

## Prerequisites

- Ubuntu 20.04 LTS (or compatible system)
- Docker installed
- Fly.io CLI (`flyctl`) installed
- Git installed
- Node.js and npm (for frontend, planned)

## Repository Structure

- `biomedical-backend/`: FastAPI backend
  - `app/`: Application code (`main.py`, detection modules)
  - `Dockerfile`: Docker configuration
  - `fly.toml`: Fly.io configuration
  - `requirements.txt`: Python dependencies
- `README.md`: Project documentation

## Setup Instructions

### Backend Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/BadrRibzat/biomediacl.git
   cd biomediacl/biomedical-backend
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the FastAPI server locally**:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```
   - Access Swagger UI at `http://localhost:8000/docs`.

5. **Test endpoints**:
   - Use Swagger UI to test `/detect/arm`, `/detect/arm-fingers`, `/detect/eyes`, `/detect/head`, `/detect/people` with a JPEG image.

### Docker Setup

1. **Build the Docker image**:
   ```bash
   docker build -t biomedical-detection .
   ```

2. **Run the Docker container**:
   ```bash
   docker run -p 8000:8000 biomedical-detection
   ```
   - Test at `http://localhost:8000/docs`.

### Fly.io Deployment

1. **Install Fly.io CLI**:
   ```bash
   curl -L https://fly.io/install.sh | sh
   ```

2. **Log in to Fly.io**:
   ```bash
   fly auth login
   ```

3. **Deploy the app**:
   ```bash
   fly deploy
   ```
   - Access at `https://biomedical-detection.fly.dev/docs` (update with your app URL).

### Frontend Setup

(In progress) To be developed with Vue 3 and TailwindCSS.

## Contributing

This is an open-source project. Feel free to fork, contribute, or suggest improvements!

## License

MIT License
