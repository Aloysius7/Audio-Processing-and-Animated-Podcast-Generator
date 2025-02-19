from pyannote.audio import Pipeline
import pandas as pd

class SpeakerDiarization:
    def __init__(self, model_name = "pyannote/speaker-diarization-3.0", auth_token = "YOUR_HUGGING_FACE_TOKEN"):
        self.pipeline = Pipeline.from_pretrained(model_name, use_auth_token=auth_token)

    def process_audio(self, audio_path, output_rttm):
        diarization = self.pipeline(audio_path, num_speakers=2)
        with open(output_rttm, "w") as rttm_file:
            diarization.write_rttm(rttm_file)

    @staticmethod
    def rttm_to_dataframe(rttm_file_path):
        columns = ["Type", "File ID", "Channel", "Start Time", "Duration", "Orthography", "Confidence", "Speaker", 'x',
                   'y']

        with open(rttm_file_path, "r") as rttm_file:
            lines = rttm_file.readlines()

        data = [line.strip().split()[3:] for line in lines]  # Extract relevant columns

        df = pd.DataFrame(data, columns=columns[3:])
        df = df.astype({'Start Time': 'float', 'Duration': 'float'})
        df['End Time'] = df['Start Time'] + df['Duration']

        return df[["Start Time", "Duration", "Speaker", "End Time"]]

    def run(self, audio_path, output_rttm, output_csv):
        self.process_audio(audio_path, output_rttm)
        df = self.rttm_to_dataframe(output_rttm)
        df.to_csv(output_csv, encoding='utf-8', index=False)


