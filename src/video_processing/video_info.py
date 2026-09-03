import cv2


def get_video_info(video_path):
    """
    Get basic information about a video.

    Parameters
    ----------
    video_path : str
        Path to the video.

    Returns
    -------
    dict
        Video information including FPS, frame count,
        duration, width, and height.
    """

    video = cv2.VideoCapture(video_path)

    if not video.isOpened():
        raise ValueError(f"Could not open video: {video_path}")

    # Get video properties
    fps = video.get(cv2.CAP_PROP_FPS)
    frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Calculate duration
    duration = frame_count / fps

    video.release()

    return {
        "fps": fps,
        "frame_count": frame_count,
        "duration": duration,
        "width": width,
        "height": height
    }