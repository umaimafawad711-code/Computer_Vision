# Week 3 - Object Detection Hardening & Model Comparison

## Task Overview
This week's task was to test a YOLO model under difficult conditions and compare two different model sizes (`yolo11n` vs `yolo11x`) across different confidence thresholds.

## What was done:
1. **Video Modification:** Created 3 harder versions of the original video using OpenCV:
   - `dark_video.mp4` (Reduced brightness)
   - `blur_video.mp4` (Applied Gaussian Blur)
   - `noise_video.mp4` (Added random noise)
2. **Detection:** Used `main.py` to run object detection on the noisy video.
3. **Comparison (Colab):** Used `compare_models.ipynb` in Google Colab to test YOLO11n and YOLO11x on all 4 videos (Original, Dark, Blur, Noise) across 4 confidence levels: `0.2, 0.4, 0.6, 0.8`.
4. **Plotting:** Generated a matplotlib graph showing how detections drop as confidence increases and as the video gets harder.

## Files in this folder:
- `comparison_graphs.png`: The plot showing model comparison.
- `compare_models.ipynb`: The Colab notebook used for the sweep.
- `main.py`: Script to detect people in the noisy video.
- `make_video.py`: Script that generated the dark, blur, and noise videos.
- `video.mp4` / `output_video.mp4`: Original video and the YOLO detected output.

## Results Summary
- **Harder Videos:** Noise, blur, and darkness significantly reduced the number of detected persons (especially for YOLO11n).
- **Model Size:** YOLO11x detected slightly more people in hard conditions compared to YOLO11n, but it was slower.
- **Confidence:** Increasing confidence threshold from 0.2 to 0.8 drastically reduced total detections across all videos.
