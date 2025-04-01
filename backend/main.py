from fastapi import FastAPI, File, UploadFile

app = FastAPI(title="Bird Drone Classifier API", version="1.0.0")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Bird Drone Classifier API!"}

@app.post("/classify")
async def classify(file: UploadFile = File(...)):
    return {"filename": file.filename, "content_type": file.content_type}