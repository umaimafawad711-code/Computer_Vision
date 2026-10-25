# Week 4 - Object Tracking (ByteTrack)

## Task Overview
Add a tracker to the YOLO detector, show each person's ID, count unique people, and find an ID switch.

## What was done:
1. Used `model.track(tracker="bytetrack.yaml")` to assign IDs to persons.
2. Added an on-screen counter to display "Total Unique People".
3. Found and analyzed an ID Switch.

## Manual Count vs Tracker Count
- **Tracker Count:** The tracker counted **4** unique people.
- **Manual Count:** I manually counted **3** people in the video.
- **Difference:** The tracker count is higher by 1. 

## ID Switch Analysis
- **Frame/Time of Switch:** At around **00:03 - 00:04** seconds.
- **What Happened:** The person in the red hoodie (originally `ID: 1`) walks out of the camera's view for a moment. When he re-enters the frame, the tracker assigns him a new ID (`ID: 4`). 
- **Why it happened:** ByteTrack relies heavily on motion prediction. Because the person disappeared for a few frames, the tracker lost his motion track. When he reappeared, the tracker couldn't match his appearance with the old track, so it created a new ID. This is a common limitation of motion-based trackers in CCTV footage when objects temporarily leave the frame.

## Files
- `main.py`: The tracking script.
- `CCTV_Video.mp4`: Input video.
- `tracked_output.mp4`: Output video with tracking IDs and counter.
