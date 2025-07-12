import os
import uvicorn
import shutil
from pathlib import Path

from fastapi import BackgroundTasks
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from agents.conversation import run_conversation
from helpers.speech_to_text import transcribe_audio
from helpers.text_to_speech import generate_speech
from helpers.crisis import detect_crisis
from helpers.audio_cleanup import delete_file
from database import init_db, log_crisis
from helpers.logger import logger

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    init_db()

# Serve static files (HTML, CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

@app.get("/")
async def main():
    with open("templates/index.html") as f:
        return HTMLResponse(content=f.read(), status_code=200)

@app.get("/ping")
async def ping():
    return {"message": "pong"}

@app.post("/process")
async def process_input(
        audio: UploadFile = File(None),
        user_id: str = None,
        session_id: str = None,
        consent: str = None,
        background_tasks: BackgroundTasks = None
    ):

    try:
        with open(f"uploads/{audio.filename}", "wb") as buffer:
            shutil.copyfileobj(audio.file, buffer)

        ARABIC_VOICE_ID = "qi4PkV9c01kb869Vh7Su"
        PROJECT_ROOT = Path(__file__).parent
        FILE_PATH = PROJECT_ROOT / "uploads" / audio.filename
        OUTPUT_AUDIO_PATH = PROJECT_ROOT / "uploads" / "translated_arabic_output_gpt4o.mp3"

        if not FILE_PATH.exists():
            raise FileNotFoundError(f"Audio file not found at: {FILE_PATH}")

        # get text from the audio
        text_from_audio = transcribe_audio(FILE_PATH)
        logger.info(f'text_from_audio {text_from_audio}')

        # check if text is harmful or not
        harmful_text = detect_crisis(text_from_audio)
        logger.info(f'harmful text delteced from keyword match: {harmful_text}')

        bot_response = None
        if harmful_text:
            bot_response = harmful_text
        else:
            bot_response = await run_conversation(text_from_audio, user_id, session_id)

        # log crisis texts
        if consent == 'allow':
            log_crisis(text_from_audio, user_id, session_id)
            log_crisis(bot_response, user_id, session_id)

        # get speech from the text
        generate_speech(bot_response, ARABIC_VOICE_ID, OUTPUT_AUDIO_PATH)

        # Schedule cleanup for input file and output file
        background_tasks.add_task(delete_file, str(FILE_PATH))
        background_tasks.add_task(delete_file, str(OUTPUT_AUDIO_PATH), 3000)

        logger.info(bot_response)
        media_type = "audio/mpeg" if OUTPUT_AUDIO_PATH.suffix == ".mp3" else "audio/wav"
        return FileResponse(OUTPUT_AUDIO_PATH, media_type=media_type)
    except Exception as e:
        print(f"Error processing audio: {e}")
        return JSONResponse(status_code=500, content={"error": f"Server error during audio processing: {e}"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
