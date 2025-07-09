
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import shutil

app = FastAPI()

# Serve static files (HTML, CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

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
        print(f"Received audio file: {audio.filename}")
        return {"filename": audio.filename}
    return {"error": "No input received"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
