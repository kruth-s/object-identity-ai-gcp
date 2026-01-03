from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    # Will be filled with GCS + Gemini soon
    content = await file.read()
    size_kb = round(len(content) / 1024, 2)
    return JSONResponse({
        "message": "Pipeline stub working",
        "filename": file.filename,
        "size_kb": size_kb,
    })
