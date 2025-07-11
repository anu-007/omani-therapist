import uvicorn
import shutil
from pathlib import Path
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from agents.conversation import run_conversation
from helpers.speech_to_text import transcribe_audio
from helpers.text_to_speech import generate_speech
from helpers.crisis import detect_crisis

app = FastAPI()

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
async def process_input(audio: UploadFile = File(None)):
    if audio:
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
        
        # check if text is harmful or not
        harmful_text = detect_crisis(text_from_audio)

        bot_response = None
        if harmful_text:
            bot_response = harmful_text
        else:
            bot_response = await run_conversation(text_from_audio)

        speech_from_text_path = generate_speech(bot_response, ARABIC_VOICE_ID, OUTPUT_AUDIO_PATH)
        return {"filename": speech_from_text_path}
        # print('bot_response', bot_response)

    return {"error": "No input received"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
