# -*- coding: utf-8 -*-
"""soil farming agent.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/11cJY2Zh_jyA4hsMgV3ziAb2JS69nGQnJ
"""

import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.model_selection import train_test_split
import numpy as np
import os
from glob import glob
from PIL import Image

from google.colab import drive
drive.mount('/content/drive')

# Load your dataset - assuming images are in a folder with subfolders for classes
# Adjust this part based on your dataset's structure

def load_dataset(image_dir, img_size=(224, 224)):
    X, y = [], []
    class_names = sorted(os.listdir(image_dir))
    class_indices = {class_name: idx for idx, class_name in enumerate(class_names)}

    for class_name in class_names:
        class_dir = os.path.join(image_dir, class_name)
        for image_file in glob(os.path.join(class_dir, '*.jpg')):  # assuming jpg images
            img = Image.open(image_file)
            img = img.resize(img_size)
            img = np.array(img) / 255.0  # normalize images
            X.append(img)
            y.append(class_indices[class_name])

    return np.array(X), np.array(y), class_names

image_dir = '/content/drive/MyDrive/Soil-Dataset'
X, y, class_names = load_dataset(image_dir)

X

y

class_names

# Split dataset into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Data Augmentation using tf.keras.layers (without ImageDataGenerator)
data_augmentation = tf.keras.Sequential([
    layers.RandomFlip("horizontal"),
    layers.RandomRotation(0.1),
    layers.RandomZoom(0.1),
])

# Define the MobileNetV2 model
def build_model(num_classes):
    base_model = MobileNetV2(input_shape=(224, 224, 3), include_top=False, weights='imagenet')
    base_model.trainable = False  # Freeze base model

    model = models.Sequential([
        data_augmentation,
        base_model,
        layers.GlobalAveragePooling2D(),
        layers.Dense(128, activation='relu'),
        layers.Dropout(0.3),
        layers.Dense(num_classes, activation='softmax')
    ])

    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    return model

# Build the model
model = build_model(num_classes=len(class_names))

# Early Stopping to prevent overfitting
early_stopping = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)

# Train the model
history = model.fit(
    X_train, y_train,
    validation_data=(X_val, y_val),
    epochs=50,
    callbacks=[early_stopping],
    batch_size=16
)

val_loss, val_acc = model.evaluate(X_val, y_val)
print(f"Validation Accuracy: {val_acc:.2f}")

# Save the model if needed
#model.save('mobilenet_soil_classifier.keras')

! pip install gradio

import gradio as gr

import gradio as gr
import tensorflow as tf
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
import numpy as np
from PIL import Image

class_names = ['Black Soil', 'Cinder Soil', 'Laterite Soil', 'Peat Soil', 'Yellow Soil']  # Update with your actual class names

def preprocess_image(image):
    image = image.resize((224, 224))  # Resize to 224x224 (input size for MobileNet)
    img_array = np.array(image)
    img_array = preprocess_input(img_array)  # Preprocess like in MobileNet
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    return img_array

def predict_soil(image):
    img_array = preprocess_image(image)
    predictions = model.predict(img_array)
    predicted_class = np.argmax(predictions[0])  # Get the class index with highest probability
    predicted_label = class_names[predicted_class]

    # You can also display the confidence scores (optional)
    confidence_scores = {class_names[i]: float(predictions[0][i]) for i in range(len(class_names))}

    # Returning both the label and confidence scores
    return f"Predicted Soil Type: {predicted_label}", confidence_scores

interface = gr.Interface(
    fn=predict_soil,
    inputs=gr.Image(type="pil"),  # Image input as a PIL image
    outputs=[
        gr.Textbox(label="Predicted Soil Type"),
        gr.Label(label="Confidence Scores")  # Confidence scores for each class
    ],
    title="Soil Type Classification",
    description="Upload an image of the soil, and the model will predict the soil type."
)

# Launch the interface
interface.launch()

