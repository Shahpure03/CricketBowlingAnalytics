import cv2

from src.pose_estimation.movenet import detect_pose
from src.visualization.draw_skeleton import draw_skeleton


# ============================================================
# Read one extracted frame
# ============================================================

frame_path = "data/processed/frames/bowling1/frame_0140.jpg"

frame = cv2.imread(frame_path)

if frame is None:
    raise ValueError("Could not read frame.")


# ============================================================
# Convert BGR → RGB for MoveNet
# ============================================================

frame_rgb = cv2.cvtColor(
    frame,
    cv2.COLOR_BGR2RGB
)


# ============================================================
# Detect pose
# ============================================================

keypoints = detect_pose(frame_rgb)


# ============================================================
# Draw skeleton
# ============================================================

annotated_frame = draw_skeleton(
    frame,
    keypoints,
    confidence_threshold=0.3
)


# ============================================================
# Save result
# ============================================================

output_path = "data/processed/frame_0000_skeleton.jpg"

cv2.imwrite(
    output_path,
    annotated_frame
)


print("Skeleton created successfully.")
print(f"Saved at: {output_path}")