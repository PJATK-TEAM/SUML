import os
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import kagglehub
import gradio as gr

# setting randomness
def set_seed(seed=42):
    tf.random.set_seed(seed)
    np.random.seed(seed)

set_seed(42)

#path to normalized data
path = "./data_split" 

# load data from folders
def load_birds_vs_drone_dataset(path, img_size=(120, 120)):
    train_dir = os.path.join(path, 'train')
    val_dir = os.path.join(path, 'val')
    test_dir = os.path.join(path, 'test')

    train_datagen = ImageDataGenerator(rescale=1.0/255.0)
    val_datagen = ImageDataGenerator(rescale=1.0/255.0)
    test_datagen = ImageDataGenerator(rescale=1.0/255.0)


    train_generator = train_datagen.flow_from_directory(
        train_dir,
        target_size=img_size,
        batch_size=32,
        class_mode='binary'
    )

    val_generator = val_datagen.flow_from_directory(
        val_dir,
        target_size=img_size,
        batch_size=32,
        class_mode='binary'
    )

    test_generator = test_datagen.flow_from_directory(
        test_dir,
        target_size=img_size,
        batch_size=32,
        class_mode='binary'
    )

    return train_generator, val_generator, test_generator


train_generator, val_generator, test_generator = load_birds_vs_drone_dataset(path)

# model
def create_model():
    model = tf.keras.models.Sequential([
 
        tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(120, 120, 3)),
        tf.keras.layers.MaxPooling2D(2, 2),

        tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
        tf.keras.layers.MaxPooling2D(2, 2),

        tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
        tf.keras.layers.MaxPooling2D(2, 2),

        tf.keras.layers.Flatten(),

        tf.keras.layers.Dense(128, activation='relu'),

        tf.keras.layers.Dense(1, activation='sigmoid')
    ])
    model.compile(
        optimizer='adam',
        loss='binary_crossentropy',
        metrics=['accuracy']
    )
    return model


model = create_model()

# training 10 epochs
history = model.fit(
    train_generator,
    validation_data=val_generator,
    epochs=10,
    batch_size=32
)

# checking accuracy
test_loss, test_accuracy = model.evaluate(test_generator)
print(f"Test accuracy: {test_accuracy:.2f}")

# save model
model.save("bird_vs_drone_model.h5")

class_names = ['Bird', 'Drone']

def predict_image(img):
    # Przygotowanie obrazu
    img = img.resize((120, 120)).convert('RGB')
    img = np.array(img).astype('float32') / 255.0 
    img = np.expand_dims(img, axis=0)

    prediction = model.predict(img)[0] 

    prob_bird = 1 - prediction # % bird
    prob_drone = prediction  # % drone

    return {class_names[0]: float(prob_bird), class_names[1]: float(prob_drone)}

# UI using Gradio
gr.Interface(fn=predict_image,
             inputs=gr.Image(type="pil"),
             outputs=gr.Label(num_top_classes=2),
             title="Bird vs Drone Classifier").launch()
