import cv2 as cv
Video= cv.VideoCapture('Video.mp4')

# 2. Video Properties
fps = int(Video.get(cv.CAP_PROP_FPS))
width = int(Video.get(cv.CAP_PROP_FRAME_WIDTH))
height = int(Video.get(cv.CAP_PROP_FRAME_HEIGHT))

# 3. Writer of  Video
fourcc = cv.VideoWriter_fourcc(*'mp4v')   # MP4 codec
out = cv.VideoWriter('output_video.mp4', fourcc, fps, (width, height))

while True:
    ret, frame = Video.read()
    
    if not ret:
        break
    
    #showing rectangle 
    cv.rectangle(frame, (0, 0), (300, 300), (0, 0, 0), 6)

    #showing Text
    cv.putText(frame, 'Hello', (100,100), cv.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)

    #Write frames on output video
    out.write(frame)
    
    #show frames 
    cv.imshow('My Video', frame)

    # Press s to stop  showing the video
    if cv.waitKey(25) & 0xFF == ord('s'):
        break
Video.release()
cv.destroyAllWindows()

# img = cv.imread('Image.jpg')

#     # Original Shape of Image
# print("Original size:", img.shape)   # (height, width, channels)
    
#     #Setting the new size for image
# new_width = 1000
# new_height = 600

#     # Resizing 
# resized = cv.resize(img, (new_width, new_height))
    
# cv.imshow('Whale', resized)
# cv.waitKey(0)
# cv.destroyAllWindows()
