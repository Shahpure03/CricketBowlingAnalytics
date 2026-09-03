from src.video_processing.trim_video import trim_video


trim_video(
    "data/raw/bowling1.mp4",
    1.5,
    4,
    "data/processed/bowling1_trimmed.mp4"
)