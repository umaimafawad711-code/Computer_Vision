import cv2 as cv
import numpy as np
import os

# Input video
input_video = 'Video.mp4'

# Output folder banao (agar nahi hai toh)
if not os.path.exists('hard_videos'):
    os.makedirs('hard_videos')

# 1. Original Video Load Karo
cap = cv.VideoCapture(input_video)
fps = int(cap.get(cv.CAP_PROP_FPS))
w = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
h = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
fourcc = cv.VideoWriter_fourcc(*'mp4v')

# Writers (3 alag videos save karne ke liye)
out_dark = cv.VideoWriter('hard_videos/dark_video.mp4', fourcc, fps, (w, h))
out_blur = cv.VideoWriter('hard_videos/blur_video.mp4', fourcc, fps, (w, h))
out_noise = cv.VideoWriter('hard_videos/noise_video.mp4', fourcc, fps, (w, h))

print("Video process ho rahi hai... thoda time lagega.")

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # ==========================================
    # 1. DARKEN (Andhera)
    # Har pixel ki value 0.4 se multiply kardo (40% brightness)
    # ==========================================
    dark_frame = cv.convertScaleAbs(frame, alpha=0.4, beta=0)
    out_dark.write(dark_frame)
    
    # ==========================================
    # 2. BLUR (Dhundla)
    # GaussianBlur lagao. (21, 21) ka matlab blur kitna hai. Bada number = zyada blur.
    # ==========================================
    blur_frame = cv.GaussianBlur(frame, (21, 21), 0)
    out_blur.write(blur_frame)
    
    # ==========================================
    # 3. NOISE (Dana / Gaussian Noise add karna)
    # ==========================================
    # Normal distribution se random noise generate karo
    noise = np.random.normal(0, 40, frame.shape).astype('uint8')
    # Original frame mein noise add kardo
    noise_frame = cv.add(frame, noise) 
    out_noise.write(noise_frame)

# Cleanup
cap.release()
out_dark.release()
out_blur.release()
out_noise.release()

print("Done! 'hard_videos' folder mein 3 videos ban gayi hain.")