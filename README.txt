
# Crop Recommendation System

## Setup

1. Install the required Python packages:
```
pip install pandas numpy scikit-learn flask
```

2. Run the application:
```
python app.py
```

3. Use Postman or curl to make a prediction request:
```
curl -X POST http://localhost:5000/predict -H "Content-Type: application/json" -d \
'{
  "N": 90,
  "P": 42,
  "K": 43,
  "temperature": 20.5,
  "humidity": 80.0,
  "ph": 6.5,
  "rainfall": 200.0
}'
```
