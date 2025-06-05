from moviepy.editor import VideoFileClip

def detect_scenes(video_path, max_duration=10):
    clip = VideoFileClip(video_path)
    total_duration = clip.duration

    scenes = []
    start = 0
    while start < total_duration:
        end = min(start + max_duration, total_duration)
        scenes.append((start, end))
        start = end

    return scenes
