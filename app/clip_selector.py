from moviepy.editor import VideoFileClip
import tempfile
import os

def generate_clips(video_path, scenes, script_text):
    clips = []
    for i, (start_sec, end_sec) in enumerate(scenes):
        clip = VideoFileClip(video_path).subclip(start_sec, end_sec)
        output_path = os.path.join(tempfile.gettempdir(), f"clip_{i+1}.mp4")
        clip.write_videofile(output_path, codec="libx264", audio_codec="aac", logger=None)
        clips.append(output_path)
    return clips
