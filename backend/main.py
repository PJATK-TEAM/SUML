import tensorflow as tf
from tensorflow import keras
import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from fastapi import FastAPI, File, UploadFile
from PIL import Image
import io
from azure.storage.blob import BlobServiceClient
from datetime import datetime
import json, os, uuid
from dotenv import load_dotenv


app = FastAPI(title="Bird Drone Classifier API", version="1.0.0")
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

load_dotenv()

blob_service = BlobServiceClient.from_connection_string(os.getenv("AZURE_STORAGE_CONNECTION_STRING"))
container_client = blob_service.get_container_client("logs")


model = tf.keras.models.load_model("bird_vs_drone_model.h5")
class_names = ['Bird', 'Drone']


@app.get("/")
def read_root():
    return {"message": "Welcome to the Bird Drone Classifier API!"}


@app.post("/classify")
async def classify(file: UploadFile = File(...)):
    if file.content_type not in ["image/jpg", "image/jpeg", "image/png"]:
        return {"error": "Invalid file type. Only JPG and PNG are allowed."}

    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        return {"error": "File too large. Maximum size is 5MB."}
    await file.close()

    result = predict_image(content)
    save_log_to_blob(file.filename, result)

    return {"prediction": result}

@app.get("/history")
def get_classification_history():
    logs = []
    try:
        blobs = container_client.list_blobs()
        for blob in blobs:
            blob_client = container_client.get_blob_client(blob.name)
            content = blob_client.download_blob().readall()
            data = json.loads(content)

            logs.append({
                "file_name": data.get("filename"),
                "timestamp": data.get("timestamp"),
                "result": data.get("prediction")
            })

        # Posortuj po najnowszych
        logs = sorted(logs, key=lambda x: x["timestamp"], reverse=True)
        return logs
    except Exception as e:
        return {"error": f"Failed to fetch history: {str(e)}"}


def predict_image(img_data):
    img = Image.open(io.BytesIO(img_data))  # decode raw data as image
    img = img.resize((120, 120)).convert('RGB')  
    img = np.array(img).astype('float32') / 255.0  
    img = np.expand_dims(img, axis=0)  

    prediction = model.predict(img)
    print("Prediction raw output:", prediction)

    prob_drone = float(prediction[0])
    prob_bird = 1.0 - prob_drone

    return {
        class_names[0]: round(prob_bird, 4),
        class_names[1]: round(prob_drone, 4)
    }

def save_log_to_blob(filename: str, prediction: dict):
    log_entry = {
        "filename": filename,
        "timestamp": datetime.utcnow().isoformat(),
        "prediction": prediction
    }

    blob_name = f"{uuid.uuid4()}.json"
    blob_data = json.dumps(log_entry)

    container_client.upload_blob(
        name=blob_name,
        data=blob_data,
        overwrite=True,
        content_type="application/json"
    )