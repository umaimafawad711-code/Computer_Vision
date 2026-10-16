import cv2 as cv
from ultralytics import YOLO

model = YOLO("yolo11n.pt")
Video = cv.VideoCapture('Video.mp4')

if not Video.isOpened():
    print("Video is not loaded!")
    exit()

fps = int(Video.get(cv.CAP_PROP_FPS))
orig_width = int(Video.get(cv.CAP_PROP_FRAME_WIDTH))
orig_height = int(Video.get(cv.CAP_PROP_FRAME_HEIGHT))
print(f"Original: {orig_width}x{orig_height}, FPS: {fps}")

new_width = 640
new_height = 360

fourcc = cv.VideoWriter_fourcc(*'mp4v')
out = cv.VideoWriter('output_video.mp4', fourcc, fps, (new_width, new_height))

cv.namedWindow('YOLO Detection', cv.WINDOW_NORMAL)
cv.resizeWindow('YOLO Detection', new_width, new_height)

frame_count = 0

while True:
    ret, frame = Video.read()
    if not ret:
        break
    
    frame = cv.resize(frame, (new_width, new_height))
    
    # ✅  for not adiing boxes below conf=0.5 
    results = model(frame, classes=[0], conf=0.5, verbose=False)
    
    for result in results:
        boxes = result.boxes
        for box in boxes:
            cls_id = int(box.cls[0])
            
            # ✅ Double check - (class 0)
            if cls_id != 0:
                continue
            
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            confidence = float(box.conf[0])
            
            # draw box 
            cv.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
            # ✅ Text background
            label = f"person {confidence:.2f}"
            (label_w, label_h), _ = cv.getTextSize(
                label, cv.FONT_HERSHEY_SIMPLEX, 0.5, 1)
            
            # Background rectangle (green)
            cv.rectangle(frame, (x1, y1 - label_h - 8),
                         (x1 + label_w + 5, y1), (0, 255, 0), -1)
            
            # Text (black)
            cv.putText(frame, label, (x1 + 2, y1 - 5),
                       cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
    
    out.write(frame)
    cv.imshow('YOLO Detection', frame)
    
    frame_count += 1
    if frame_count % 10 == 0:
        print(f"Processed {frame_count} frames...")
    
    if cv.waitKey(1) & 0xFF == ord('s'):
        print("Stopped by user")
        break

Video.release()
out.release()
cv.destroyAllWindows()
print(f"Done! Total frames: {frame_count}")
