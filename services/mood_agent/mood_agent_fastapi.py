from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from services.mood_agent.mood_logic import analyze_mood_energy
import tempfile, uvicorn

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/ping")
def ping():
    return {"ok": True, "service": "mood"}


def _process(upload: UploadFile):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(upload.file.read())
        file_path = tmp.name
    return analyze_mood_energy(file_path)


@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    return _process(file)


@app.post("/mood")
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
    return _process(upload)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
