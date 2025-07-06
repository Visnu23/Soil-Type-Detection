
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from flask import Flask, request, jsonify
import warnings

warnings.filterwarnings("ignore")

# Load dataset
data = pd.read_csv('Crop_recommendation.csv')

# Features and target
X = data[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']]
y = data['label']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Flask app
app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict_crop():
    data = request.json
    input_features = np.array([[data['N'], data['P'], data['K'],
                                data['temperature'], data['humidity'],
                                data['ph'], data['rainfall']]])
    prediction = model.predict(input_features)
    return jsonify({'recommended_crop': prediction[0]})

if __name__ == '__main__':
    app.run(debug=True)
