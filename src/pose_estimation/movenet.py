import tensorflow as tf
import numpy as np


# ============================================================
# Configuration
# ============================================================

MODEL_PATH = "models/movenet/3.tflite"


# ============================================================
# MoveNet keypoint names
# ============================================================

KEYPOINT_NAMES = [
    "nose",
    "left_eye",
    "right_eye",
    "left_ear",
    "right_ear",
    "left_shoulder",
    "right_shoulder",
    "left_elbow",
    "right_elbow",
    "left_wrist",
    "right_wrist",
    "left_hip",
    "right_hip",
    "left_knee",
    "right_knee",
    "left_ankle",
    "right_ankle"
]


# ============================================================
# Load MoveNet
# ============================================================

interpreter = tf.lite.Interpreter(
    model_path=MODEL_PATH
)

interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()


# ============================================================
# Model information
# ============================================================

INPUT_HEIGHT = input_details[0]["shape"][1]
INPUT_WIDTH = input_details[0]["shape"][2]

INPUT_DTYPE = input_details[0]["dtype"]


# ============================================================
# Pose detection
# ============================================================

def detect_pose(image, crop=None):
    """
    Detect 17 body keypoints using MoveNet Lightning.

    Parameters
    ----------
    image : numpy.ndarray
        RGB image.

    crop : tuple or None
        Optional crop:
        (x1, y1, x2, y2)

        Coordinates are relative to the original image.

    Returns
    -------
    numpy.ndarray
        Shape: (17, 3)

        Each keypoint contains:

        [y, x, confidence]

        y and x are normalized to the ORIGINAL image.
    """

    # ========================================================
    # 0. Validate image
    # ========================================================

    if image is None:
        raise ValueError("Input image is None.")

    if not isinstance(image, np.ndarray):
        raise TypeError(
            "Input image must be a NumPy array."
        )

    if image.ndim != 3 or image.shape[2] != 3:
        raise ValueError(
            "Input image must have shape "
            "(height, width, 3)."
        )


    # ========================================================
    # 1. Save original image dimensions
    # ========================================================

    original_height, original_width = image.shape[:2]


    # ========================================================
    # 2. Optional crop
    # ========================================================

    crop_x1 = 0
    crop_y1 = 0

    if crop is not None:

        x1, y1, x2, y2 = crop

        x1 = int(x1)
        y1 = int(y1)
        x2 = int(x2)
        y2 = int(y2)

        # Keep crop inside image
        x1 = max(
            0,
            min(x1, original_width - 1)
        )

        y1 = max(
            0,
            min(y1, original_height - 1)
        )

        x2 = max(
            x1 + 1,
            min(x2, original_width)
        )

        y2 = max(
            y1 + 1,
            min(y2, original_height)
        )

        # Store crop offset
        crop_x1 = x1
        crop_y1 = y1

        # Apply crop
        image = image[y1:y2, x1:x2]


    # ========================================================
    # 3. Resize directly to 192 x 192
    #
    # This matches the preprocessing used in the
    # MathWorks example for this exact 3.tflite model.
    # ========================================================

    resized = tf.image.resize(
        image,
        (INPUT_HEIGHT, INPUT_WIDTH),
        method=tf.image.ResizeMethod.BILINEAR
    ).numpy()


    # ========================================================
    # 4. Convert to model input type
    #
    # For this 3.tflite model:
    #
    # InputType = single / float32
    #
    # But the pixel values are kept in the original
    # 0-255 range.
    #
    # DO NOT normalize to [-1, 1].
    # ========================================================

    resized = resized.astype(
        INPUT_DTYPE
    )


    # ========================================================
    # 5. Add batch dimension
    #
    # (192, 192, 3)
    #
    # becomes
    #
    # (1, 192, 192, 3)
    # ========================================================

    input_image = np.expand_dims(
        resized,
        axis=0
    )


    # ========================================================
    # 6. Run MoveNet
    # ========================================================

    interpreter.set_tensor(
        input_details[0]["index"],
        input_image
    )

    interpreter.invoke()


    # ========================================================
    # 7. Get model output
    #
    # Expected:
    #
    # (1, 1, 17, 3)
    #
    # Each keypoint:
    #
    # [y, x, confidence]
    # ========================================================

    keypoints = interpreter.get_tensor(
        output_details[0]["index"]
    )


    # Remove batch / person dimensions
    keypoints = keypoints[0, 0, :, :]


    # ========================================================
    # 8. Convert coordinates back to original image
    # ========================================================

    converted_keypoints = []


    for y, x, confidence in keypoints:

        # ----------------------------------------------------
        # Model coordinates are normalized 0-1.
        #
        # Convert them to coordinates in the resized
        # 192 x 192 image.
        # ----------------------------------------------------

        model_y = y * INPUT_HEIGHT
        model_x = x * INPUT_WIDTH


        # ----------------------------------------------------
        # Convert from 192 x 192 back to the dimensions
        # of the image that was passed to MoveNet.
        #
        # Because we directly resized:
        #
        # resized_y / original_y
        #
        # and
        #
        # resized_x / original_x
        # ----------------------------------------------------

        image_height, image_width = image.shape[:2]

        image_y = (
            model_y / INPUT_HEIGHT
        ) * image_height

        image_x = (
            model_x / INPUT_WIDTH
        ) * image_width


        # ----------------------------------------------------
        # If a crop was used, restore coordinates to the
        # original full frame.
        # ----------------------------------------------------

        image_y += crop_y1
        image_x += crop_x1


        # ----------------------------------------------------
        # Normalize to ORIGINAL full-frame coordinates.
        # ----------------------------------------------------

        normalized_y = (
            image_y / original_height
        )

        normalized_x = (
            image_x / original_width
        )


        converted_keypoints.append([
            float(normalized_y),
            float(normalized_x),
            float(confidence)
        ])


    # ========================================================
    # 9. Return
    # ========================================================

    return np.array(
        converted_keypoints,
        dtype=np.float32
    )