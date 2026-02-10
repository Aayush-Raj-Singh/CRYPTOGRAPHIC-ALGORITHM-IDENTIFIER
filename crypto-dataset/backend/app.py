from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from backend.inference import predict_cipher

app = FastAPI(
    title="Cryptographic Algorithm Identifier API",
    description="ML-based cryptographic algorithm classification from ciphertext",
    version="1.0"
)

# Allow frontend access later
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {
        "message": "Cryptographic Algorithm Identifier API is running"
    }

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    # Basic validation
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded")

    content = await file.read()

    if len(content) == 0:
        raise HTTPException(status_code=400, detail="Empty file")

    if len(content) > 2 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="File too large (max 2MB)")

    try:
        result = predict_cipher(content)
    except ValueError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    return result
