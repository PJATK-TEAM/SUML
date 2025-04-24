import tensorflow as tf
from tensorflow import keras
import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import kagglehub
from fastapi import FastAPI, File, UploadFile

app = FastAPI(title="Bird Drone Classifier API", version="1.0.0")
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

model = tf.keras.models.load_model("backend/bird_vs_drone_model.h5")
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
    return {"prediction": result}


def predict_image(img):
    img = img.resize((120, 120)).convert('RGB')
    img = np.array(img).astype('float32') / 255.0
    img = np.expand_dims(img, axis=0)

    prediction = model.predict(img)[0]

    prob_bird = 1 - prediction # % bird
    prob_drone = prediction  # % drone

    return {class_names[0]: float(prob_bird), class_names[1]: float(prob_drone)}