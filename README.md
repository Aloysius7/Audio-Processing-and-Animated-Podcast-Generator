# Auto Animated Podcast AI

Auto Animated Podcast AI is a Python-based application that converts podcast audio files into engaging animated videos. By leveraging speaker diarization with `pyannote.audio` and dynamic animations using `Manim`, this tool creates visual representations where animated characters respond to audio amplitude and speaker changes.

> **Note:** This application is designed primarily for audio files containing two speakers.

## Features

- **Speaker Diarization:**  
  Utilizes the `pyannote/speaker-diarization-3.0` model to identify and segment different speakers within an audio file.

- **Dynamic Character Animation:**  
  Generates animations where characters' expressions and accompanying waveforms dynamically adjust based on the audio's properties.

- **Seamless Audio-Visual Integration:**  
  Merges the generated animations with the original audio to produce a cohesive final video.

- **Customization Options:**  
  Allows users to upload a custom background image for the animated video. If no custom image is provided, a default background is used.

- **User-Friendly Streamlit Interface:**  
  Interact with the application via a simple web interface. Upload your audio file and optional background image, then click **Submit** to start processing.

## Prerequisites

- **Python:** Python 3.10 is recommended.
- **FFmpeg & FFprobe:** Ensure these are installed on your system and that their paths are correctly set in the script To install these use this [link](https://www.gyan.dev/ffmpeg/builds/).
- **Other Dependencies:**  
  - `pyannote.audio`
  - `manim`
  - `pandas`
  - `pydub`
  - `onnxruntime`
  - `streamlit`
    
## Installation

It is advisable to work within a virtual environment. Follow these steps to set up the project:

```bash
# Clone the repository
git clone https://github.com/Aloysius7/Audio-Processing-and-Animated-Podcast-Generator.git
cd Audio-Processing-and-Animated-Podcast-Generator

# Create and activate a virtual environment
python3.10 -m venv venv
# On Unix/macOS:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
```
## Configuration
**Hugging Face Authentication**
```bash
from pyannote.audio import Pipeline

pipeline = Pipeline.from_pretrained(
    "pyannote/speaker-diarization-3.0",
    use_auth_token="YOUR_HUGGING_FACE_TOKEN"
)
```
**FFmpeg & FFprobe Paths**
Adjust the FFmpeg paths in your configuration (e.g., in your main script or configuration file):
```bash
from pydub import AudioSegment

AudioSegment.converter = r"/path/to/ffmpeg"
AudioSegment.ffprobe = r"/path/to/ffprobe"
```
## Execution
To run the Streamlit interface:
```bash
streamlit run main.py
```

## Demo Video
For a demonstration of the application's capabilities, please check out the demo video:

https://github.com/user-attachments/assets/7991060c-82e6-4665-9a9d-7bfecb067355

## Visuals
User Interface:
![image](https://github.com/user-attachments/assets/46ac917b-7761-43ae-85d7-8fb88dd632b9)
![image](https://github.com/user-attachments/assets/ddf1e22a-fc53-45ed-88b0-84683b81ce4e)

## Thank You for Reading 😋
