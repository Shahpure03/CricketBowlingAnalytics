import cv2
import os


def extract_frames(video_path, output_folder):
    """
    Extract all frames from a video and save them as image files.

    Parameters
    ----------
    video_path : str
        Path to the input video.

    output_folder : str
        Folder where the extracted frames will be saved.

    Returns
    -------
    int
        Number of frames extracted.
    """

    # Open the video
    video = cv2.VideoCapture(video_path)

    if not video.isOpened():
        raise ValueError(f"Could not open video: {video_path}")

    # Create output folder if it does not exist
    os.makedirs(output_folder, exist_ok=True)

    frame_number = 0

    while True:

        # Read one frame
        success, frame = video.read()

        # Stop when there are no more frames
        if not success:
            break

        # Create filename
        frame_path = os.path.join(
            output_folder,
            f"frame_{frame_number:04d}.jpg"
        )

        # Save frame
        cv2.imwrite(frame_path, frame)

        frame_number += 1

    # Release video
    video.release()

    print(f"Extracted {frame_number} frames.")
    print(f"Frames saved in: {output_folder}")

    return frame_number