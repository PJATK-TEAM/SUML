import random

from fastapi import FastAPI, File, UploadFile

app = FastAPI(title="Bird Drone Classifier API", version="1.0.0")
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

@app.get("/")
def read_root():
    return {"message": "Welcome to the Bird Drone Classifier API!"}

@app.post("/classify")
async def classify(file: UploadFile = File(...)):
    if file.content_type not in ["image/jpg","image/jpeg", "image/png"]:
        return {"error": "Invalid file type. Only JPG and PNG are allowed."}

    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        return {"error": "File too large. Maximum size is 5MB."}
    await file.close()

    possible_results = ["Bird", "Drone"]
    return {"message": random.choice(possible_results)}