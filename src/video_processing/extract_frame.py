import cv2

VIDEO_PATH = "data/raw/bowling1.mp4"
OUTPUT_PATH = "data/processed/test_frame.jpg"

video = cv2.VideoCapture(VIDEO_PATH)

if not video.isOpened():
    print("Error: Could not open video.")
    exit()

success, frame = video.read()

if success:
    cv2.imwrite(OUTPUT_PATH, frame)
    print("Frame extracted successfully!")
    print("Saved to:", OUTPUT_PATH)
else:
    print("Error: Could not read frame.")

video.release()