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
        return {"error": "Invalid file type. Only JPEG and PNG files are allowed."}
    if file.size > MAX_FILE_SIZE:
        return {"error": "File too large. Maximum size is 5MB."}

    possible_results = ["Bird", "Drone"]
    return {"message": random.choice(possible_results)}