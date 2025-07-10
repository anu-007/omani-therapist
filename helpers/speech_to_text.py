import openai
import os

def transcribe_audio(audio_file_path):
    """
    Transcribes an audio file using OpenAI's Whisper API.
    Handles a maximum file size of 25MB for the API.
    """
    try:
        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set.")

        client = openai.OpenAI(api_key=api_key)

        with open(audio_file_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model = "whisper-1",
                file = audio_file,
                language = 'ar'
            )
        return transcript.text
    except Exception as e:
        print(f"Error during Whisper transcription: {e}")
        return None