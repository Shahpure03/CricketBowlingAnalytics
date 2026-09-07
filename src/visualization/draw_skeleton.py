import cv2
import numpy as np


# ============================================================
# MoveNet keypoint indices
# ============================================================

NOSE = 0
LEFT_EYE = 1
RIGHT_EYE = 2
LEFT_EAR = 3
RIGHT_EAR = 4

LEFT_SHOULDER = 5
RIGHT_SHOULDER = 6

LEFT_ELBOW = 7
RIGHT_ELBOW = 8

LEFT_WRIST = 9
RIGHT_WRIST = 10

LEFT_HIP = 11
RIGHT_HIP = 12

LEFT_KNEE = 13
RIGHT_KNEE = 14

LEFT_ANKLE = 15
RIGHT_ANKLE = 16


# ============================================================
# Colours (BGR format used by OpenCV)
# ============================================================

HEAD_COLOR = (0, 0, 255)          # Red
LEFT_ARM_COLOR = (255, 0, 0)      # Blue
RIGHT_ARM_COLOR = (0, 255, 255)   # Yellow
TORSO_COLOR = (0, 255, 0)         # Green
LOWER_BODY_COLOR = (150, 150, 150) # Grey


# ============================================================
# Skeleton connections
# ============================================================

HEAD_CONNECTIONS = [
    (NOSE, LEFT_EYE),
    (NOSE, RIGHT_EYE),
    (LEFT_EYE, LEFT_EAR),
    (RIGHT_EYE, RIGHT_EAR)
]


LEFT_ARM_CONNECTIONS = [
    (LEFT_SHOULDER, LEFT_ELBOW),
    (LEFT_ELBOW, LEFT_WRIST)
]


RIGHT_ARM_CONNECTIONS = [
    (RIGHT_SHOULDER, RIGHT_ELBOW),
    (RIGHT_ELBOW, RIGHT_WRIST)
]


TORSO_CONNECTIONS = [
    (LEFT_SHOULDER, RIGHT_SHOULDER),
    (LEFT_SHOULDER, LEFT_HIP),
    (RIGHT_SHOULDER, RIGHT_HIP),
    (LEFT_HIP, RIGHT_HIP)
]


LOWER_BODY_CONNECTIONS = [
    (LEFT_HIP, LEFT_KNEE),
    (LEFT_KNEE, LEFT_ANKLE),
    (RIGHT_HIP, RIGHT_KNEE),
    (RIGHT_KNEE, RIGHT_ANKLE)
]


# ============================================================
# Draw one connection
# ============================================================

def draw_connection(frame, keypoints, point_a, point_b,
                    color, confidence_threshold=0.3):

    height, width = frame.shape[:2]

    y1, x1, confidence1 = keypoints[point_a]
    y2, x2, confidence2 = keypoints[point_b]

    # Ignore unreliable points
    if confidence1 < confidence_threshold:
        return

    if confidence2 < confidence_threshold:
        return

    # Convert normalized coordinates
    # to original frame coordinates

    x1 = int(x1 * width)
    y1 = int(y1 * height)

    x2 = int(x2 * width)
    y2 = int(y2 * height)

    cv2.line(
        frame,
        (x1, y1),
        (x2, y2),
        color,
        3
    )


# ============================================================
# Draw one keypoint
# ============================================================

def draw_keypoint(frame, keypoints, index,
                  color, confidence_threshold=0.3):

    height, width = frame.shape[:2]

    y, x, confidence = keypoints[index]

    if confidence < confidence_threshold:
        return

    x = int(x * width)
    y = int(y * height)

    cv2.circle(
        frame,
        (x, y),
        6,
        color,
        -1
    )


# ============================================================
# Draw complete skeleton
# ============================================================

def draw_skeleton(frame, keypoints, confidence_threshold=0.3):

    output = frame.copy()

    # --------------------------------------------------------
    # Head / face
    # --------------------------------------------------------

    for a, b in HEAD_CONNECTIONS:
        draw_connection(
            output,
            keypoints,
            a,
            b,
            HEAD_COLOR,
            confidence_threshold
        )

    # --------------------------------------------------------
    # Left arm
    # --------------------------------------------------------

    for a, b in LEFT_ARM_CONNECTIONS:
        draw_connection(
            output,
            keypoints,
            a,
            b,
            LEFT_ARM_COLOR,
            confidence_threshold
        )

    # --------------------------------------------------------
    # Right arm
    # --------------------------------------------------------

    for a, b in RIGHT_ARM_CONNECTIONS:
        draw_connection(
            output,
            keypoints,
            a,
            b,
            RIGHT_ARM_COLOR,
            confidence_threshold
        )

    # --------------------------------------------------------
    # Torso
    # --------------------------------------------------------

    for a, b in TORSO_CONNECTIONS:
        draw_connection(
            output,
            keypoints,
            a,
            b,
            TORSO_COLOR,
            confidence_threshold
        )

    # --------------------------------------------------------
    # Lower body
    # --------------------------------------------------------

    for a, b in LOWER_BODY_CONNECTIONS:
        draw_connection(
            output,
            keypoints,
            a,
            b,
            LOWER_BODY_COLOR,
            confidence_threshold
        )

    # --------------------------------------------------------
    # Draw points
    # --------------------------------------------------------

    for index in [
        NOSE,
        LEFT_EYE,
        RIGHT_EYE,
        LEFT_EAR,
        RIGHT_EAR
    ]:
        draw_keypoint(
            output,
            keypoints,
            index,
            HEAD_COLOR,
            confidence_threshold
        )

    for index in [
        LEFT_SHOULDER,
        LEFT_ELBOW,
        LEFT_WRIST
    ]:
        draw_keypoint(
            output,
            keypoints,
            index,
            LEFT_ARM_COLOR,
            confidence_threshold
        )

    for index in [
        RIGHT_SHOULDER,
        RIGHT_ELBOW,
        RIGHT_WRIST
    ]:
        draw_keypoint(
            output,
            keypoints,
            index,
            RIGHT_ARM_COLOR,
            confidence_threshold
        )

    for index in [
        LEFT_HIP,
        RIGHT_HIP
    ]:
        draw_keypoint(
            output,
            keypoints,
            index,
            TORSO_COLOR,
            confidence_threshold
        )

    for index in [
        LEFT_KNEE,
        RIGHT_KNEE,
        LEFT_ANKLE,
        RIGHT_ANKLE
    ]:
        draw_keypoint(
            output,
            keypoints,
            index,
            LOWER_BODY_COLOR,
            confidence_threshold
        )

    return output