from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from services.audio_agent.audio_logic import analyze_audio
import os, shutil

app = FastAPI()
UPLOAD_DIR = "/app/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/ping")
def ping():
    return {"ok": True, "service": "audio"}


def _process(upload: UploadFile):
    file_location = os.path.join(UPLOAD_DIR, upload.filename)
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(upload.file, buffer)
    return analyze_audio(file_location)


@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    try:
        return JSONResponse(content=_process(file))
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


# 👇 tolerant alias used by some UIs (axios, etc.)
@app.post("/audio")
async def analyze_alias(
    file: UploadFile | None = File(default=None),
    track: UploadFile | None = File(default=None),
):
    upload = file or track
    if not upload:
        raise HTTPException(
            status_code=400,
            detail="No file provided. Use multipart/form-data with field 'file'.",
        )
    try:
        return JSONResponse(content=_process(upload))
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
