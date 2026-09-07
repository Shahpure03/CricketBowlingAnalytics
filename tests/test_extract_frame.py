from src.video_processing.extract_frame import extract_frames


video_path = "data/processed/bowling1_trimmed.mp4"

output_folder = "data/processed/frames/bowling1"

extract_frames(
    video_path,
    output_folder
)