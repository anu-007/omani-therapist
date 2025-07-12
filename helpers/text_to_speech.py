import os
from elevenlabs.client import ElevenLabs
from .logger import logger

def generate_speech(text, voice_id, output_path):
    """
    Generates speech from text using ElevenLabs API.
    """
    api_key = os.getenv("ELEVENLABS_API_KEY")

    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY environment variable not set.")
    
    elevenlabs_client = ElevenLabs(api_key=api_key)

    if not text:
        return None

    try:
        audio_stream = elevenlabs_client.text_to_speech.convert(
            voice_id=voice_id,
            text=text,
            model_id="eleven_multilingual_v2",
            output_format="mp3_44100_128",
        )

        with open(output_path, "wb") as f:
            for chunk in audio_stream:
                f.write(chunk)
        logger.info(f"Generated audio saved to: {output_path}")

        return output_path
    except Exception as e:
        logger.error(f"Error during ElevenLabs TTS: {e}")
        return None