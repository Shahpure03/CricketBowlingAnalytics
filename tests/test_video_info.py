from src.video_processing.video_info import get_video_info


video_path = input("Enter video path: ")

info = get_video_info(video_path)


print("\n========== VIDEO INFORMATION ==========")
print(f"FPS          : {info['fps']}")
print(f"Frame count  : {info['frame_count']}")
print(f"Duration     : {info['duration']:.2f} seconds")
print(f"Resolution   : {info['width']} x {info['height']}")
print("=======================================\n")