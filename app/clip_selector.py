from moviepy.video.io.VideoFileClip import VideoFileClip
import tempfile
import os

def generate_clips(video_path, scenes, script_text):
    clips = []
    for i, (start_time, end_time) in enumerate(scenes):
        duration = end_time.get_seconds() - start_time.get_seconds()
        if duration > 10:
            continue  # Skip long clips
        clip = VideoFileClip(video_path).subclip(start_time.get_seconds(), end_time.get_seconds())
        output_path = os.path.join(tempfile.gettempdir(), f"clip_{i+1}.mp4")
        clip.write_videofile(output_path, codec="libx264")
        clips.append(output_path)
    return clips

