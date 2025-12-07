"""
Prediction Module - ML Model Loading and Prediction Functions
Handles real-time predictions for food quality classification
"""

import pickle
import numpy as np
from pathlib import Path

# Label mapping
LABEL_MAPPING = {
    0: 'Sangat Buruk',
    1: 'Buruk',
    2: 'Baik',
    3: 'Sangat Baik'
}

class FoodQualityPredictor:
    """Class for predicting food quality using trained ML models"""
    
    def __init__(self, model_path: Path, scaler_path: Path):
        """
        Initialize predictor with model and scaler
        
        Args:
            model_path: Path to trained model pickle file
            scaler_path: Path to scaler pickle file
        """
        self.model = self._load_pickle(model_path)
        self.scaler = self._load_pickle(scaler_path)
    
    @staticmethod
    def _load_pickle(file_path: Path):
        """Load pickle file"""
        try:
            with open(file_path, 'rb') as f:
                return pickle.load(f)
        except Exception as e:
            raise Exception(f"Error loading {file_path}: {str(e)}")
    
    def predict_single(self, calories: float, proteins: float, fat: float, carbohydrate: float) -> dict:
        """
        Predict quality for a single food item
        
        Args:
            calories: Calorie content
            proteins: Protein content in grams
            fat: Fat content in grams
            carbohydrate: Carbohydrate content in grams
        
        Returns:
            Dictionary with prediction, label_name, and confidence
        """
        try:
            # Prepare features
            features = np.array([[calories, proteins, fat, carbohydrate]])
            
            # Scale features
            features_scaled = self.scaler.transform(features)
            
            # Predict
            prediction = self.model.predict(features_scaled)[0]
            
            # Get confidence if available
            if hasattr(self.model, 'predict_proba'):
                probabilities = self.model.predict_proba(features_scaled)[0]
                confidence = float(np.max(probabilities)) * 100
            else:
                # K-Means doesn't have probabilities
                confidence = 100.0
            
            # Get label name
            label_name = LABEL_MAPPING.get(int(prediction), 'Baik')
            
            return {
                'prediction': int(prediction),
                'label_name': label_name,
                'confidence': round(confidence, 2)
            }
        
        except Exception as e:
            return {
                'prediction': 2,
                'label_name': 'Baik',
                'confidence': 0.0,
                'error': str(e)
            }
    
    def predict_batch(self, foods_data: list) -> list:
        """
        Predict quality for multiple food items
        
        Args:
            foods_data: List of dictionaries with keys: calories, proteins, fat, carbohydrate
        
        Returns:
            List of prediction dictionaries
        """
        results = []
        
        for food in foods_data:
            pred = self.predict_single(
                food.get('calories', 0),
                food.get('proteins', 0),
                food.get('fat', 0),
                food.get('carbohydrate', 0)
            )
            pred['id'] = food.get('id', None)
            results.append(pred)
        
        return results

def load_predictor(model_type: str, models_dir: Path) -> FoodQualityPredictor:
    """
    Load predictor for specified model type
    
    Args:
        model_type: One of 'random_forest', 'naive_bayes', 'svm', 'kmeans'
        models_dir: Directory containing model files
    
    Returns:
        FoodQualityPredictor instance
    """
    model_files = {
        'random_forest': ('random_forest_model.pkl', 'random_forest_scaler.pkl'),
        'naive_bayes': ('naive_bayes_model.pkl', 'naive_bayes_scaler.pkl'),
        'svm': ('svm_model.pkl', 'svm_scaler.pkl'),
        'kmeans': ('kmeans_model.pkl', 'kmeans_scaler.pkl')
    }
    
    if model_type not in model_files:
        raise ValueError(f"Invalid model type: {model_type}")
    
    model_file, scaler_file = model_files[model_type]
    model_path = models_dir / model_file
    scaler_path = models_dir / scaler_file
    
    return FoodQualityPredictor(model_path, scaler_path)

def get_available_models(models_dir: Path) -> list:
    """
    Get list of available trained models
    
    Args:
        models_dir: Directory containing model files
    
    Returns:
        List of available model names
    """
    models = []
    model_types = ['random_forest', 'naive_bayes', 'svm', 'kmeans']
    
    for model_type in model_types:
        model_file = models_dir / f'{model_type}_model.pkl'
        scaler_file = models_dir / f'{model_type}_scaler.pkl'
        
        if model_file.exists() and scaler_file.exists():
            models.append(model_type)
    
    return models
