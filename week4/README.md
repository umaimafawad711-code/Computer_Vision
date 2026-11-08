# Week 5 - Events, Counting, and Alerts

## Task Overview
This week's task was to move from simple tracking to understanding events. I built a system to track people, define a restricted zone, trigger an alert when someone enters it, and compare the tracker's count with a manual count.

## What was done:
1. **Restricted Zone Setup:** Created a virtual polygon (red box) in the bottom-left corner of the frame using `supervision`.
2. **Event Detection:** Implemented logic to check if the "bottom-center" point (feet) of any person's bounding box entered the red zone.
3. **Alert System:** When a person enters the zone, the system raises an on-screen alert ("ALERT: RESTRICTED ZONE!") and counts them as a unique visitor.
4. **Unique Counting:** Used a Python `set()` to ensure that even if a person stays inside the zone for multiple frames, they are only counted once.

## Manual Count vs Tracker Count
- **Manual Count:** I manually observed the video. Only 1 person (the man in the red hoodie) entered the restricted zone on the bottom left. He stayed there for a few seconds.
- **Tracker Count:** The on-screen counter showed **1** unique person entering the zone.
- **Explanation:** The tracker count perfectly matched the manual count. The `set()` logic worked perfectly, preventing the same person from being counted 30 times (once for every frame he was inside the zone).

## Files included:
- `main.py`: The script to detect, track, and count zone entries.
- `CCTV_Video.mp4`: The input video.
- `week5_output.mp4`: The output video showing bounding boxes, the red restricted zone, the alert, and the total count.

## How to Run:
1. Install dependencies: `pip install ultralytics supervision opencv-python`
2. Run the script: `python main.py`
