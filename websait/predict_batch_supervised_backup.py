"""
Real-time batch prediction using trained ML models
Receives multiple foods and returns predictions
"""

import json
import pickle
import numpy as np
import sys

def load_model(model_type):
    """Load the specified model and scaler"""
    model_files = {
        'random_forest': ('random_forest_model.pkl', 'random_forest_scaler.pkl'),
        'naive_bayes': ('naive_bayes_model.pkl', 'naive_bayes_scaler.pkl'),
        'svm': ('svm_model.pkl', 'svm_scaler.pkl'),
        'kmeans': ('kmeans_model.pkl', 'kmeans_scaler.pkl')
    }
    
    if model_type not in model_files:
        model_type = 'random_forest'
    
    model_file, scaler_file = model_files[model_type]
    
    try:
        with open(model_file, 'rb') as f:
            model = pickle.load(f)
        with open(scaler_file, 'rb') as f:
            scaler = pickle.load(f)
        return model, scaler
    except FileNotFoundError as e:
        print(json.dumps({'error': f'Model files not found: {str(e)}'}))
        sys.exit(1)

def get_label_name(prediction):
    """Convert numeric prediction to label name"""
    labels = {
        0: 'Sangat Buruk',
        1: 'Buruk',
        2: 'Baik',
        3: 'Sangat Baik'
    }
    # Handle both int and string predictions
    pred_int = int(prediction) if isinstance(prediction, (str, np.integer)) else prediction
    return labels.get(pred_int, 'Baik')

def predict_batch(model, scaler, foods_data):
    """Predict labels for multiple foods"""
    results = []
    
    for food in foods_data:
        try:
            # Extract features
            features = np.array([[
                float(food.get('calories', 0)),
                float(food.get('proteins', 0)),
                float(food.get('fat', 0)),
                float(food.get('carbohydrate', 0))
            ]])
            
            # Scale features
            features_scaled = scaler.transform(features)
            
            # Predict
            prediction = model.predict(features_scaled)[0]
            
            # Get probabilities if available
            if hasattr(model, 'predict_proba'):
                probabilities = model.predict_proba(features_scaled)[0]
                confidence = float(np.max(probabilities)) * 100
            else:
                # K-Means doesn't have probabilities
                confidence = 100.0
            
            # Get label name
            label_name = get_label_name(prediction)
            
            results.append({
                'id': food.get('id'),
                'prediction': int(prediction) if hasattr(prediction, '__int__') else str(prediction),
                'label_name': label_name,
                'confidence': round(confidence, 2)
            })
            
        except Exception as e:
            results.append({
                'id': food.get('id'),
                'error': str(e),
                'prediction': 2,
                'label_name': 'Baik',
                'confidence': 0.0
            })
    
    return results

def main():
    """Main prediction function"""
    try:
        # Read input from command line argument (file path)
        if len(sys.argv) < 3:
            print(json.dumps({'error': 'Missing arguments: model_type and input_file'}))
            sys.exit(1)
        
        model_type = sys.argv[1]
        input_file = sys.argv[2]
        
        # Read input data from file (handle BOM)
        with open(input_file, 'r', encoding='utf-8-sig') as f:
            input_data = json.load(f)
        
        # Load model
        model, scaler = load_model(model_type)
        
        # Make predictions
        results = predict_batch(model, scaler, input_data['foods'])
        
        # Output results
        print(json.dumps({
            'success': True,
            'model_used': model_type,
            'predictions': results
        }))
        
    except Exception as e:
        print(json.dumps({'error': str(e), 'success': False}))
        sys.exit(1)

if __name__ == '__main__':
    main()
