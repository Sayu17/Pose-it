import cv2
import mediapipe as mp
import numpy as np
import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog
from PIL import Image, ImageTk

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

# Function to process video
def process_video(video_path):
    cap = cv2.VideoCapture(video_path)
    with mp_pose.Pose(min_detection_confidence=0.6, min_tracking_confidence=0.6) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Convert the BGR image to RGB
            RGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            frame1 = cv2.resize(frame, (output_width, output_height))

            # Process the RGB frame to get the result
            results = pose.process(RGB)

            # Draw detected skeleton on the frame
            if results.pose_landmarks:
                mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            # Resize the frame for display
            resized_frame = cv2.resize(frame, (output_width, output_height))

            combined_frame = np.hstack((frame1, resized_frame))

            # Convert the frame to ImageTk format
            img = Image.fromarray(cv2.cvtColor(combined_frame, cv2.COLOR_BGR2RGB))
            imgtk = ImageTk.PhotoImage(image=img)

            # Update the GUI with the new frame
            lbl_video.imgtk = imgtk
            lbl_video.configure(image=imgtk)
            lbl_video.update()

            if cv2.waitKey(1) == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()

# Function to open file dialog and select video
def open_file():
    video_path = filedialog.askopenfilename()
    if video_path:
        process_video(video_path)

ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")

# Create the main window
root = ctk.CTk()
root.title("Pose It!")
root.geometry("600x400")  # Set window size
root.configure(bg="#2B2B2B") 

# Heading Label
heading_label = ctk.CTkLabel(
    root,
    text="Pose it!",
    font=("Arial", 36, "bold"),
    text_color="#FFD700"  
)
heading_label.pack(pady=40)  # Add spacing above the heading

# Description Label
description_label = ctk.CTkLabel(
    root,
    text="Upload your video to generate the pose output!",
    font=("Arial", 18),
    text_color="white",
    wraplength=500,  
    justify="center"  
)
description_label.pack(pady=20)

# Upload Button
upload_button = ctk.CTkButton(
    root,
    text="Upload Video",
    font=("Arial", 16),
    text_color="white",
    fg_color="#1E90FF",  # Dodger Blue 
    hover_color="#4682B4",  # Steel Blue 
    corner_radius=10, 
    command=open_file)

upload_button.pack(pady=30)

# Create a frame to display the video
video_frame = tk.Frame(root, bg="#2B2B2B")
video_frame.pack(pady=20, fill="both", expand=True)

# Input Video Label
input_video_label = ctk.CTkLabel(
    video_frame,
    text="Input Video",
    font=("Arial", 18),
    text_color="white"
)
input_video_label.grid(row=0, column=0, padx=20, pady=10, sticky="n")

# Output Video Label
output_video_label = ctk.CTkLabel(
    video_frame,
    text="Output Video",
    font=("Arial", 18),
    text_color="white"
)
output_video_label.grid(row=0, column=1, padx=20, pady=10, sticky="n")

# Create a label to display the video
lbl_video = tk.Label(video_frame, bg="#2B2B2B")
lbl_video.grid(row=1, column=0, columnspan=2, padx=20, pady=10)
# Set the output width and height
output_width = 640
output_height = 480

# Run the GUI loop
root.mainloop()
