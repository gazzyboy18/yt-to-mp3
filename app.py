import streamlit as st
import yt_dlp
import os
import uuid
import shutil

st.set_page_config(page_title="YouTube to MP3", page_icon="🎧")

st.title("🎧 Free YouTube to MP3 Converter")
st.write("Paste a YouTube link below and convert it to MP3. Free of charge.")

url = st.text_input("YouTube URL")

if st.button("Convert"):
    if not url:
        st.error("Please enter a YouTube URL.")
        st.stop()

    temp_folder = "temp_downloads"
    os.makedirs(temp_folder, exist_ok=True)

    mp3_id = str(uuid.uuid4())
    output_path = os.path.join(temp_folder, f"{mp3_id}.mp3")

    ydl_opts = {
        "format": "bestaudio/best",
        "ffmpeg_location": r"C:\ffmpeg-8.0.1-full_build\bin",
        "outtmpl": os.path.join(temp_folder, "%(title)s.%(ext)s"),
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get("title", "audio")
            filename = ydl.prepare_filename(info)
            mp3_file = filename.rsplit(".", 1)[0] + ".mp3"

        with open(mp3_file, "rb") as f:
            st.success("Conversion complete!")
            st.download_button(
                label="⬇️ Download MP3",
                data=f,
                file_name=f"{title}.mp3",
                mime="audio/mpeg",
            )

        shutil.rmtree(temp_folder)

    except Exception as e:
        st.error(f"⚠️ Error: {e}")
