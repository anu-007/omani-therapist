import uvicorn
import shutil
from pathlib import Path
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from agents.conversation import run_conversation
from helpers.speech_to_text import transcribe_audio
from helpers.text_to_speech import generate_speech

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
async def process_input(text: str = Form(None), audio: UploadFile = File(None)):
    if text:
        print(f"Received text: {text}")
        return {"text": text}
    if audio:
        # Save the audio file
        with open(f"uploads/{audio.filename}", "wb") as buffer:
            shutil.copyfileobj(audio.file, buffer)

        ARABIC_VOICE_ID = "qi4PkV9c01kb869Vh7Su"
        PROJECT_ROOT = Path(__file__).parent
        FILE_PATH = PROJECT_ROOT / "uploads" / audio.filename
        OUTPUT_AUDIO_PATH = PROJECT_ROOT / "uploads" / "translated_arabic_output_gpt4o.mp3"

        if not FILE_PATH.exists():
            raise FileNotFoundError(f"Audio file not found at: {FILE_PATH}")

        print('FILE_PATH', FILE_PATH)
        text_from_audio = transcribe_audio(FILE_PATH)

        print('text_from_audio', text_from_audio)
        conv = await run_conversation(text_from_audio)
        print('conv', conv)

        speech_from_text_path = generate_speech(conv, ARABIC_VOICE_ID, OUTPUT_AUDIO_PATH)

        print(f"Response audio file: {speech_from_text_path}")
        return {"filename": speech_from_text_path}

    return {"error": "No input received"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
