import cv2
import mediapipe as mp
import tkinter as tk
from PIL import Image, ImageTk
import numpy as np

class HeadDetectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Head Detection - Biomedical Tutorial")
        
        # Initialize MediaPipe Face Detection
        self.mp_face_detection = mp.solutions.face_detection
        self.face_detection = self.mp_face_detection.FaceDetection(min_detection_confidence=0.5)
        self.mp_drawing = mp.solutions.drawing_utils
        
        # Video capture
        self.cap = cv2.VideoCapture(0)
        self.running = False
        
        # GUI elements
        self.canvas = tk.Canvas(root, width=640, height=480)
        self.canvas.pack()
        
        self.btn_toggle = tk.Button(root, text="Start Detection", command=self.toggle_detection)
        self.btn_toggle.pack(pady=10)
        
        self.update_frame()
    
    def toggle_detection(self):
        self.running = not self.running
        self.btn_toggle.config(text="Stop Detection" if self.running else "Start Detection")
    
    def update_frame(self):
        if self.running:
            ret, frame = self.cap.read()
            if ret:
                # Convert to RGB for MediaPipe
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = self.face_detection.process(frame_rgb)
                
                # Draw bounding boxes
                if results.detections:
                    for detection in results.detections:
                        self.mp_drawing.draw_detection(frame, detection)
                
                # Convert frame to ImageTk format
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame_rgb)
                img = ImageTk.PhotoImage(img)
                
                # Update canvas
                self.canvas.img = img  # Keep reference to avoid garbage collection
                self.canvas.create_image(0, 0, anchor=tk.NW, image=img)
        
        # Schedule next frame update
        self.root.after(10, self.update_frame)
    
    def __del__(self):
        if self.cap.isOpened():
            self.cap.release()

if __name__ == "__main__":
    root = tk.Tk()
    app = HeadDetectionApp(root)
    root.mainloop()
