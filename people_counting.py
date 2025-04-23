import cv2
import mediapipe as mp
import tkinter as tk
from PIL import Image, ImageTk
import numpy as np

class PeopleCountingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("People Counting - Biomedical Tutorial")
        
        # Initialize MediaPipe Pose
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.mp_drawing = mp.solutions.drawing_utils
        
        # Video capture
        self.cap = cv2.VideoCapture(0)
        self.running = False
        self.people_count = 0
        self.previous_landmarks = None
        
        # GUI elements
        self.canvas = tk.Canvas(root, width=640, height=480)
        self.canvas.pack()
        
        self.count_label = tk.Label(root, text=f"People Count: {self.people_count}", font=("Arial", 14))
        self.count_label.pack(pady=5)
        
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
                results = self.pose.process(frame_rgb)
                
                # Count people
                if results.pose_landmarks:
                    current_landmarks = results.pose_landmarks.landmark
                    if self.previous_landmarks is None or self.is_new_person(current_landmarks):
                        self.people_count += 1
                        self.count_label.config(text=f"People Count: {self.people_count}")
                    self.previous_landmarks = current_landmarks
                    
                    # Draw pose landmarks
                    self.mp_drawing.draw_landmarks(
                        frame,
                        results.pose_landmarks,
                        self.mp_pose.POSE_CONNECTIONS,
                        landmark_drawing_spec=self.mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2),
                        connection_drawing_spec=self.mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2)
                    )
                
                # Convert frame to ImageTk format
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame_rgb)
                img = ImageTk.PhotoImage(img)
                
                # Update canvas
                self.canvas.img = img
                self.canvas.create_image(0, 0, anchor=tk.NW, image=img)
        
        # Schedule next frame update
        self.root.after(10, self.update_frame)
    
    def is_new_person(self, current_landmarks):
        if self.previous_landmarks is None:
            return True
        # Simple heuristic: check if landmarks have moved significantly
        for curr, prev in zip(current_landmarks, self.previous_landmarks):
            if abs(curr.x - prev.x) > 0.2 or abs(curr.y - prev.y) > 0.2:
                return True
        return False
    
    def __del__(self):
        if self.cap.isOpened():
            self.cap.release()

if __name__ == "__main__":
    root = tk.Tk()
    app = PeopleCountingApp(root)
    root.mainloop()
