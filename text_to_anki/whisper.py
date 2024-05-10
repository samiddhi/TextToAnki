from tkinter import filedialog, Tk
from typing import List, Dict
from pydub import AudioSegment
from openai import OpenAI

import json


class AudioTranscriber:
    """
    A class to handle audio file loading, segmenting, and transcribing using OpenAI's Whisper model.

    :param api_key: str: The API key for OpenAI services.
    """
    def __init__(self, api_key: str, prompt='') -> None:
        self.api_key = api_key
        self.client = OpenAI(api_key=api_key)
        self.prompt = prompt

    def load_audio_file(self, file_path: str) -> None:
        """
        Loads the audio file from the provided path.

        :param file_path: str: The path to the audio file.
        """
        # Determine the file format based on the file extension
        file_extension = file_path.split('.')[-1]
        supported_formats = {
            'mp3': 'mp3',
            'm4a': 'mp4',
            'wav': 'wav'
        }
        format = supported_formats.get(file_extension, 'mp3')  # Default to 'mp3' if unknown
        self.audio_file = AudioSegment.from_file(file_path, format=format)

    def segment_audio(self, segment_length: int) -> list:
        """
        Segments the audio file into chunks of the specified length in minutes.
        Handles files shorter than the segment length.

        :param segment_length: int: Length of each segment in minutes.
        :return: list: List of audio segments.
        """
        segment_length_ms = segment_length * 60 * 1000
        if len(self.audio_file) < segment_length_ms:
            return [self.audio_file]  # Return the whole file as one segment if it's shorter than the segment length
        return [self.audio_file[i:i + segment_length_ms] for i in range(0, len(self.audio_file), segment_length_ms)]

    def transcribe_audio(self, audio_segment: AudioSegment) -> str:
        """
        Transcribes a single audio segment.

        :param audio_segment: AudioSegment: The audio segment to transcribe.
        :return: str: The transcription of the audio segment.
        """
        audio_segment.export("temp_audio.mp3", format="mp3")  # Export to a common format
        with open("temp_audio.mp3", "rb") as file:
            transcription = self.client.audio.transcriptions.create(
                model="whisper-1",
                file=file,
                prompt=self.prompt
            )
            return transcription.text

    def transcribe(self, segment_length: int) -> list:
        """
        Segments and transcribes the entire audio file.

        :param segment_length: int: Length of each segment in minutes.
        :return: list: List of transcriptions for each segment.
        """
        segments = self.segment_audio(segment_length)
        return [self.transcribe_audio(segment) for segment in segments]


def select_file():
    """
    Opens a file dialog to select an audio file, and transcribes it.
    """
    root = Tk()
    root.withdraw()  # prevent root window from showing
    file_path = filedialog.askopenfilename()
    return file_path


def main(
        prompt: str = '',
        file_path: str = None,
        segment_length: int = 15
):
    user_path = (r"C:\Users\sangha\Documents\Danny's\TextToAnki\data\users"
                 r"\user.json")
    with open(user_path, "r", encoding="utf-8") as user_data:
        user: Dict = json.load(user_data)
        user_api = user.get("api", None)
    if user_api is None:
        return "OpenAI API key needed for this action"
    transcriber = AudioTranscriber(user_api, prompt)
    if file_path is None:
        file_path = select_file()
    if file_path:
        transcriber.load_audio_file(file_path)
        transcriptions: List[str] = transcriber.transcribe(segment_length)
        return transcriptions


if __name__ == "__main__":
    kps = '''
        Dobro jutro, dragi poslušalci. Danes bomo raziskali povezavo med umom in telesom.

        Good morning, dear listeners. Today, we are going to explore the connection between the mind and the body. This is an interesting topic that draws on both ancient wisdom and modern scientific understanding.

        In many traditions, the body is seen as a vessel that carries the mind. Yet, contemporary research shows us that the state of the body can influence mental health and cognition.

        'Naše telo reagira na stres na različne načine. Nekateri od teh vključujejo pospešeno bitje srca in zvišanje krvnega tlaka.'

        Our body responds to stress in various ways. Some of these include an accelerated heartbeat and elevated blood pressure. It's a primitive response that prepares us to face or flee from perceived threats.

        But how can we manage this in today's world, where the threats we face are not so immediate? Meditation, mindfulness, and physical exercise are just a few methods that can help.

        'Kako pa to vpliva na naše vsakdanje življenje? Razmislite o tem, kako bi lahko bolje skrbeli za svoje telo in um.'

        How does this impact our daily life? Think about how you might better care for your body and mind. It's not only about reducing stress but also about enhancing overall well-being.

        'Ko govorimo o umu, ne smemo pozabiti na pomembnost spanja. Spanje omogoča našim možganom, da se regenerirajo.'

        As we talk about the mind, we must not overlook the importance of sleep. Sleep allows our brains to regenerate and consolidate memories. It's crucial for maintaining mental clarity and emotional stability.

        In conclusion, taking care of your body is not separate from taking care of your mind. They are deeply interconnected, and our wellbeing depends on both being in good shape.

        Hvala, da ste se nam pridružili. Upam, da ste našli nekaj koristnega v tem pogovoru.
        Naj vas pot vodi k miru in zdravju. Nasvidenje.
    '''
