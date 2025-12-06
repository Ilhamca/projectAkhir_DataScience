import json
import pickle
import numpy as np
import sys

# Load model and scaler
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

# Read input from file
with open('temp_input.json', 'r') as f:
    input_data = json.load(f)

# Prepare features
features = np.array([[
    input_data['calories'],
    input_data['proteins'],
    input_data['fat'],
    input_data['carbohydrate']
]])

# Scale features
features_scaled = scaler.transform(features)

# Predict
prediction = model.predict(features_scaled)[0]
probabilities = model.predict_proba(features_scaled)[0]
confidence = float(max(probabilities)) * 100

# Get label name
label_names = model.classes_
label_name = str(prediction) if isinstance(prediction, str) else label_names[list(label_names).index(prediction)]

# Output result
result = {
    'label': int(list(label_names).index(prediction)),
    'label_name': label_name,
    'confidence': round(confidence, 2),
    'probabilities': [round(float(p) * 100, 2) for p in probabilities]
}

print(json.dumps(result))
