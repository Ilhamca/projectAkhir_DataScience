"""
Pre-classify all foods in the database using all trained ML models
This ensures the website uses actual model predictions, not just CSV labels
"""

import pandas as pd
import pickle
import numpy as np
import json

# Load the dataset
df = pd.read_csv('nutrition_data.csv')

# Model configurations
models_config = {
    'random_forest': {
        'model_file': 'random_forest_model.pkl',
        'scaler_file': 'random_forest_scaler.pkl',
        'name': 'Random Forest'
    },
    'naive_bayes': {
        'model_file': 'naive_bayes_model.pkl',
        'scaler_file': 'naive_bayes_scaler.pkl',
        'name': 'Naive Bayes'
    },
    'svm': {
        'model_file': 'svm_model.pkl',
        'scaler_file': 'svm_scaler.pkl',
        'name': 'SVM'
    },
    'kmeans': {
        'model_file': 'kmeans_model.pkl',
        'scaler_file': 'kmeans_scaler.pkl',
        'name': 'K-Means'
    }
}

def classify_with_model(model_key):
    """Classify all foods using specified model"""
    config = models_config[model_key]
    
    # Load model and scaler
    try:
        with open(config['model_file'], 'rb') as f:
            model = pickle.load(f)
        with open(config['scaler_file'], 'rb') as f:
            scaler = pickle.load(f)
    except FileNotFoundError:
        print(f"Warning: Model files for {model_key} not found. Skipping.")
        return None
    
    # Prepare features
    feature_columns = ['calories', 'proteins', 'fat', 'carbohydrate']
    X = df[feature_columns].values
    
    # Scale features
    X_scaled = scaler.transform(X)
    
    # Predict
    predictions = model.predict(X_scaled)
    
    # Get probabilities (if available)
    if hasattr(model, 'predict_proba'):
        probabilities = model.predict_proba(X_scaled)
        confidences = np.max(probabilities, axis=1) * 100
    else:
        # K-Means doesn't have probabilities
        confidences = np.full(len(predictions), 100.0)
    
    return {
        'predictions': predictions.tolist(),
        'confidences': confidences.tolist()
    }

def main():
    """Main classification function"""
    print("Starting food classification with all models...")
    
    # Store all model predictions
    all_predictions = {}
    
    for model_key in models_config.keys():
        print(f"Classifying with {models_config[model_key]['name']}...")
        result = classify_with_model(model_key)
        if result:
            all_predictions[model_key] = result
            # Add predictions to dataframe
            df[f'{model_key}_prediction'] = result['predictions']
            df[f'{model_key}_confidence'] = result['confidences']
    
    # Save enhanced dataset
    output_file = 'nutrition_data_with_predictions.csv'
    df.to_csv(output_file, index=False)
    print(f"\nClassification complete! Saved to {output_file}")
    
    # Print summary
    print("\n=== Classification Summary ===")
    for model_key in all_predictions.keys():
        predictions = all_predictions[model_key]['predictions']
        unique, counts = np.unique(predictions, return_counts=True)
        print(f"\n{models_config[model_key]['name']}:")
        for label, count in zip(unique, counts):
            print(f"  {label}: {count} foods")
    
    # Create a summary JSON for quick loading
    summary = {
        'total_foods': len(df),
        'models_used': list(models_config.keys()),
        'classification_timestamp': pd.Timestamp.now().isoformat()
    }
    
    with open('classification_summary.json', 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"\nTotal foods classified: {len(df)}")
    print("Summary saved to classification_summary.json")

if __name__ == '__main__':
    main()
