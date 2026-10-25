import cv2 as cv
from ultralytics import YOLO

# 1. Load the YOLO model
model = YOLO("yolo11n.pt")

# 2. Open the CCTV Video
video_path = 'CCTV_Video.mp4'
cap = cv.VideoCapture(video_path)

if not cap.isOpened():
    print("Error: Video not found!")
    exit()

# Get video properties for saving
fps = int(cap.get(cv.CAP_PROP_FPS))
width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))

# 3. Setup Video Writer to save the output
fourcc = cv.VideoWriter_fourcc(*'mp4v')
out = cv.VideoWriter('tracked_output.mp4', fourcc, fps, (width, height))

# 4. Create a set to store UNIQUE IDs
# A set automatically removes duplicates. If we see ID 1 five times, it only stores it once.
unique_ids = set()

print("Processing video... Please wait.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 5. Run YOLO Tracking
    # persist=True tells the model to remember IDs from the previous frame
    # tracker="bytetrack.yaml" uses ByteTrack algorithm
    # classes=[0] means we only track persons
    results = model.track(frame, persist=True, tracker="bytetrack.yaml", classes=[0], conf=0.3, verbose=False)

    # 6. Process the results and draw bounding boxes
    if results[0].boxes is not None and results[0].boxes.id is not None:
        # Get all bounding boxes, track IDs, and confidences for this frame
        boxes = results[0].boxes.xyxy.cpu().numpy().astype(int)
        ids = results[0].boxes.id.cpu().numpy().astype(int)
        confs = results[0].boxes.conf.cpu().numpy()

        for box, track_id, conf in zip(boxes, ids, confs):
            x1, y1, x2, y2 = box
            
            # Add the ID to our unique set
            unique_ids.add(track_id)

            # Draw the bounding box (Green)
            cv.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
            # Prepare the text label
            label = f"ID: {track_id} ({conf:.2f})"
            
            # Draw a background rectangle for the text so it's readable
            (w, h), _ = cv.getTextSize(label, cv.FONT_HERSHEY_SIMPLEX, 0.6, 2)
            cv.rectangle(frame, (x1, y1 - 25), (x1 + w, y1), (0, 255, 0), -1)
            
            # Put the text on the frame (Black text on green background)
            cv.putText(frame, label, (x1, y1 - 5), cv.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)

    # 7. Draw the Total Unique Count Box on the Top-Left
    count_text = f"Total Unique People: {len(unique_ids)}"
    
    # Background box for the counter (Black box with white border)
    cv.rectangle(frame, (20, 20), (450, 70), (0, 0, 0), -1)
    cv.rectangle(frame, (20, 20), (450, 70), (255, 255, 255), 2)
    
    # Text for the counter (Yellow color)
    cv.putText(frame, count_text, (30, 55), cv.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

    # 8. Save and Show the frame
    out.write(frame)
    cv.imshow('CCTV Tracking', frame)

    # Press 's' to stop early
    if cv.waitKey(1) & 0xFF == ord('s'):
        break

# 9. Cleanup
cap.release()
out.release()
cv.destroyAllWindows()
print(f"Done! Video saved as 'tracked_output.mp4'.")
print(f"Total unique people tracked in this video: {len(unique_ids)}")