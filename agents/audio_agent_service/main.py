from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from audio_logic import analyze_audio
import os
import shutil

app = FastAPI()

UPLOAD_DIR = "/app/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    file_location = os.path.join(UPLOAD_DIR, file.filename)

    try:
        # Save uploaded file
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # DEBUG: Show file location
        print(f"📁 File saved at: {file_location}")

        # Analyze audio
        result = analyze_audio(file_location)

        return JSONResponse(content=result)

    except Exception as e:
        # Print full error to console
        print(f"🔥 Error while analyzing: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})
