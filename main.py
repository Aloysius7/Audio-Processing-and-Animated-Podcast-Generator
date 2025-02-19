import streamlit as st
import os
import subprocess
from pydub import AudioSegment
from voice_diarization import SpeakerDiarization
from VideoAI import TalkingCharacters

def convert_to_wav(input_audio_path, output_audio_path):
    audio = AudioSegment.from_file(input_audio_path)
    audio.export(output_audio_path, format="wav")

def get_audio_duration(audio_path, ffprobe_path="ffprobe"):
    """Returns the duration (in seconds) of the given audio file."""
    result = subprocess.run(
        [ffprobe_path, '-v', 'error', '-show_entries', 'format=duration',
         '-of', 'default=noprint_wrappers=1:nokey=1', audio_path],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    try:
        duration = float(result.stdout.strip())
        return duration
    except Exception as e:
        st.error("Could not determine audio duration.")
        return None

def main():
    st.title("Audio Processing and Animated Podcast Generator")
    st.write("Upload your audio file and an optional background image.")

    uploaded_audio = st.file_uploader("Upload Audio File", type=["wav", "mp3", "ogg", "flac", "aac", "m4a"])
    background_image = st.file_uploader("Upload Background Image (Optional)", type=["jpg", "jpeg", "png"])
    submit_button = st.button("Submit")

    if submit_button and uploaded_audio:
        # Save uploaded audio file
        audio_folder = "audio"
        os.makedirs(audio_folder, exist_ok=True)
        input_audio_path = os.path.join(audio_folder, uploaded_audio.name)
        with open(input_audio_path, "wb") as f:
            f.write(uploaded_audio.read())

        # Convert to WAV if necessary and save as sample.wav
        output_audio_path = os.path.join(audio_folder, "sample.wav")
        if not input_audio_path.endswith("sample.wav"):
            st.write("Converting to WAV format...")
            convert_to_wav(input_audio_path, output_audio_path)
        else:
            output_audio_path = input_audio_path

        # Run speaker diarization
        st.write("Running speaker diarization...")
        diarizer = SpeakerDiarization("pyannote/speaker-diarization-3.0")
        diarizer.run(output_audio_path, "sample.rttm", "sample.csv")

        # Generate animated video with custom background (if provided)
        st.write("Generating animated video...")
        scene = TalkingCharacters()
        if background_image:
            os.makedirs("Images", exist_ok=True)
            custom_bg_path = os.path.join("Images", background_image.name)
            with open(custom_bg_path, "wb") as f:
                f.write(background_image.read())
            scene.construct(custom_bg_path)
        else:
            scene.construct("Images/Background1.jpeg")
        scene.render()

        # Use the generated TalkingCharacters video
        video_path = "media/videos/480p15/TalkingCharacters.mp4"
        if not os.path.exists(video_path):
            video_path = "media/videos/1080p60/TalkingCharacters.mp4"

        # Get the duration of the audio to trim the video exactly to the audio's length
        audio_duration = get_audio_duration(output_audio_path)
        if audio_duration is None:
            return

        final_video_path = "final_animated_podcast.mp4"
        ffmpeg_path = r"D:\BIT n BUILD\pythonProject\animatedPodcast\animatedPodcast\External Requirements\ffmpeg-7.1-essentials_build\bin\ffmpeg.exe"
        subprocess.run([
            ffmpeg_path, "-y",
            "-i", video_path,
            "-i", output_audio_path,
            "-map", "0:v:0",  # Use video from TalkingCharacters output
            "-map", "1:a:0",  # Use our processed audio
            "-c:v", "libx264",
            "-c:a", "aac",
            "-t", str(audio_duration),  # Trim the final video to match the audio length
            "-movflags", "+faststart",
            final_video_path
        ])

        st.success(f"Final video saved as: {final_video_path}")
        st.video(final_video_path)

if __name__ == "__main__":
    main()
