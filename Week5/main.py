import cv2
import numpy as np
from ultralytics import YOLO
import supervision as sv

# 1. Load the YOLO model
model = YOLO("yolo11n.pt")

# 2. Load the video
video_path = "CCTV_Video.mp4"
cap = cv2.VideoCapture(video_path)

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS))

# 3. Setup Video Writer
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('week5_output.mp4', fourcc, fps, (width, height))

# 4. Setup Supervision Annotators
box_annotator = sv.BoxAnnotator(thickness=2)
label_annotator = sv.LabelAnnotator(text_scale=0.5, text_thickness=1)

# 5. Setup the Restricted Zone (Bottom-Left Corner)
restricted_polygon = np.array([
    [0, height - 300],          # Top-Left
    [400, height - 300],        # Top-Right
    [400, height],              # Bottom-Right
    [0, height]                 # Bottom-Left
])
zone = sv.PolygonZone(polygon=restricted_polygon)
zone_annotator = sv.PolygonZoneAnnotator(zone=zone, color=sv.Color.RED, thickness=2, text_scale=0.6)

# Naya: Ek Set banayein taaki duplicate IDs count na hon
unique_ids_in_zone = set()

print("Processing video... Please wait.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Run YOLO tracking
    results = model.track(frame, persist=True, tracker="bytetrack.yaml", classes=[0], conf=0.3, verbose=False)[0]
    detections = sv.Detections.from_ultralytics(results)

    if detections.tracker_id is not None:
        labels = [f"ID: {tracker_id}" for tracker_id in detections.tracker_id]
    else:
        labels = []

    # --- ZONE LOGIC ---
    # Check if people are inside the zone
    is_in_zone = zone.trigger(detections=detections)

    # Agar koi zone mein hai, toh uski ID ko hamare Set mein save karein
    if detections.tracker_id is not None:
        for i, inside in enumerate(is_in_zone):
            if inside:
                # Track ID ko set mein daal do (set duplicate IDs ko khud ignore kar dega)
                unique_ids_in_zone.add(detections.tracker_id[i])

    # Total unique log jo ab tak zone mein aaye hain
    total_entered_zone = len(unique_ids_in_zone)

    # --- DRAWING ---
    frame = zone_annotator.annotate(scene=frame)
    frame = box_annotator.annotate(scene=frame, detections=detections)
    frame = label_annotator.annotate(scene=frame, detections=detections, labels=labels)

    # Screen par Total Count likhein
    cv2.putText(frame, f"People Entered Zone: {total_entered_zone}", (20, 40), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    # Show ALERT
    if np.any(is_in_zone):
        cv2.putText(frame, "ALERT: RESTRICTED ZONE!", (50, 80), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

    out.write(frame)
    cv2.imshow("Week 5 - Zone Counting", frame)

    if cv2.waitKey(1) & 0xFF == ord('s'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()

print("-----------------------------------------")
print(f"Total Unique People who entered the Restricted Zone: {total_entered_zone}")
print("Done! Check 'week5_output.mp4'")