import streamlit as st
import sys
import os

# Thêm đường dẫn để chắc chắn Python thấy được thư mục app/
sys.path.append(os.path.abspath("."))

from app.utils import save_uploaded_file
from app.scene_detection import detect_scenes
from app.clip_selector import generate_clips

st.title("🎬 Script-Based Video Cutter")

video_file = st.file_uploader("Upload MP4 video", type=["mp4"])
script_file = st.file_uploader("Upload script text", type=["txt"])

if video_file and script_file:
    with st.spinner("Processing..."):
        video_path = save_uploaded_file(video_file)
        script_text = script_file.read().decode("utf-8")
        
        scenes = detect_scenes(video_path)
        clips = generate_clips(video_path, scenes, script_text)
        
        for i, clip_path in enumerate(clips):
            st.video(clip_path)
            with open(clip_path, "rb") as f:
                st.download_button(f"Download Clip {i+1}", f, file_name=f"clip_{i+1}.mp4")
