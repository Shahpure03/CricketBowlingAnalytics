import cv2


def trim_video(video_path, start_time, end_time, output_path):
    """
    Trim a video and save only the requested portion.

    Parameters
    ----------
    video_path : str
        Path to the original video.

    start_time : float
        Start time of the required portion, in seconds.

    end_time : float
        End time of the required portion, in seconds.

    output_path : str
        Path where the trimmed video should be saved.
    """

    # ============================================================
    # 1. Open the original video
    # ============================================================

    video = cv2.VideoCapture(video_path)

    if not video.isOpened():
        raise ValueError(f"Could not open video: {video_path}")


    # ============================================================
    # 2. Get video information
    # ============================================================

    fps = video.get(cv2.CAP_PROP_FPS)
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

    duration = total_frames / fps


    # ============================================================
    # 3. Validate the start and end times
    # ============================================================

    # Start time cannot be negative.

    if start_time < 0:
        video.release()
        raise ValueError("Start time cannot be negative.")


    # End time must be greater than start time.

    if end_time <= start_time:
        video.release()
        raise ValueError("End time must be greater than start time.")


    # End time cannot exceed video duration.

    if end_time > duration:
        video.release()
        raise ValueError(
            f"End time exceeds the video duration ({duration:.2f} seconds)."
        )


    # ============================================================
    # 4. Create the output video
    # ============================================================

    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # MP4 output
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")

    output_video = cv2.VideoWriter(
        output_path,
        fourcc,
        fps,
        (width, height)
    )

    if not output_video.isOpened():
        video.release()
        raise ValueError(f"Could not create output video: {output_path}")


    # ============================================================
    # 5. Move to the starting position
    # ============================================================

    video.set(cv2.CAP_PROP_POS_MSEC, start_time * 1000)


    # ============================================================
    # 6. Read and write only the required section
    # ============================================================

    while True:

        ret, frame = video.read()

        if not ret:
            break

        # Current position in milliseconds
        current_time = video.get(cv2.CAP_PROP_POS_MSEC) / 1000

        # Stop when we reach the requested end time
        if current_time > end_time:
            break

        output_video.write(frame)


    # ============================================================
    # 7. Close the videos
    # ============================================================

    video.release()
    output_video.release()


    # ============================================================
    # 8. Tell the user where the file was created
    # ============================================================

    print("\nTrimmed video created successfully.")
    print(f"Saved at: {output_path}")