import cv2
from src.pose_estimation.movenet import detect_pose, KEYPOINT_NAMES


frame_path = "data/processed/frames/bowling1/frame_0140.jpg"

frame = cv2.imread(frame_path)

if frame is None:
    raise FileNotFoundError(
        f"Could not read image: {frame_path}"
    )

# OpenCV reads images as BGR.
# MoveNet function expects RGB.
frame_rgb = cv2.cvtColor(
    frame,
    cv2.COLOR_BGR2RGB
)

keypoints = detect_pose(frame_rgb)


print("Number of keypoints:", len(keypoints))

for i, (y, x, confidence) in enumerate(keypoints):

    print(
        f"{i:2d} "
        f"{KEYPOINT_NAMES[i]:15s} "
        f"y={y:.4f} "
        f"x={x:.4f} "
        f"conf={confidence:.4f}"
    )