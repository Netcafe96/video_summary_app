import tempfile
import os
import zipfile
from moviepy.editor import VideoFileClip
from scenedetect import VideoManager, SceneManager
from scenedetect.detectors import ContentDetector
import whisper
from sentence_transformers import SentenceTransformer, util

def process_video_and_script(video_file, script_file):
    # Load the video
    video_path = tempfile.mktemp(suffix=".mp4")
    with open(video_path, "wb") as f:
        f.write(video_file.read())

    # Load the script
    script_path = tempfile.mktemp(suffix=".txt")
    with open(script_path, "w") as f:
        f.write(script_file.read())

    # Detect scenes in the video
    video_manager = VideoManager([video_path])
    scene_manager = SceneManager()
    scene_manager.add_detector(ContentDetector())
    video_manager.start()
    scene_manager.detect_scenes(frame_source=video_manager)
    scene_list = scene_manager.get_scene_list()

    # Load Whisper model for transcription
    model = whisper.load_model("base")
    transcription = model.transcribe(video_path)
    spoken_text = transcription['text']

    # Load Sentence Transformer model
    sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
    script_embedding = sentence_model.encode(script_file.read().splitlines(), convert_to_tensor=True)
    spoken_embedding = sentence_model.encode(spoken_text.split('.'), convert_to_tensor=True)

    # Find best matching clips
    clips = []
    for i, sentence in enumerate(script_file.read().splitlines()):
        similarity = util.pytorch_cos_sim(script_embedding[i], spoken_embedding)
        if similarity > 0.5:  # Threshold for matching
            start_time = scene_list[i][0].get_seconds()
            end_time = start_time + 10  # Limit to 10 seconds
            clips.append((start_time, end_time))

    # Export clips
    output_files = []
    for i, (start, end) in enumerate(clips):
        clip = VideoFileClip(video_path).subclip(start, end)
        output_path = tempfile.mktemp(suffix=f"clip_{i+1}.mp4")
        clip.write_videofile(output_path, codec="libx264")
        output_files.append(output_path)

    # Clean up
    os.remove(video_path)
    os.remove(script_path)

    return output_files
