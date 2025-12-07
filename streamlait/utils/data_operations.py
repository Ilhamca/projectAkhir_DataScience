"""
Data Operations Module - Data Loading, Cleaning, and Transformation
Handles all data preprocessing operations for the admin panel
"""

import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
import pickle

class DataOperations:
    """Class for handling data operations"""
    
    def __init__(self, data_file: Path):
        """
        Initialize with data file path
        
        Args:
            data_file: Path to CSV data file
        """
        self.data_file = data_file
        self.df = None
    
    def load_data(self) -> pd.DataFrame:
        """Load data from CSV file"""
        try:
            self.df = pd.read_csv(self.data_file, encoding='utf-8-sig')
            return self.df
        except Exception as e:
            raise Exception(f"Error loading data: {str(e)}")
    
    def get_stats(self) -> dict:
        """Get data statistics"""
        if self.df is None:
            self.load_data()
        
        numeric_df = self.df.select_dtypes(include=[np.number])
        
        stats = {
            'total_rows': len(self.df),
            'total_columns': len(self.df.columns),
            'missing_values': int(self.df.isnull().sum().sum()),
            'duplicates': int(self.df.duplicated().sum()),
            'numeric_columns': len(numeric_df.columns),
            'categorical_columns': len(self.df.select_dtypes(include=['object']).columns)
        }
        
        return stats
    
    def get_descriptive_stats(self) -> dict:
        """Get descriptive statistics for numeric columns"""
        if self.df is None:
            self.load_data()
        
        numeric_df = self.df.select_dtypes(include=[np.number])
        return numeric_df.describe().to_dict()
    
    def get_skewness(self) -> list:
        """Get skewness for numeric columns"""
        if self.df is None:
            self.load_data()
        
        numeric_df = self.df.select_dtypes(include=[np.number])
        skewness_data = []
        
        for col in numeric_df.columns:
            skewness_data.append({
                'column': col,
                'skewness': float(numeric_df[col].skew())
            })
        
        return skewness_data
    
    def clean_data(self, remove_duplicates=False, handle_missing=False, handle_outliers=False) -> tuple:
        """
        Clean the dataset
        
        Args:
            remove_duplicates: Whether to remove duplicate rows
            handle_missing: Whether to fill missing values
            handle_outliers: Whether to remove outliers using IQR method
        
        Returns:
            Tuple of (cleaned_df, stats_dict)
        """
        if self.df is None:
            self.load_data()
        
        df_cleaned = self.df.copy()
        
        stats = {
            'rows_before': len(self.df),
            'duplicates_removed': 0,
            'missing_filled': 0,
            'outliers_removed': 0
        }
        
        # Remove duplicates
        if remove_duplicates:
            before = len(df_cleaned)
            df_cleaned = df_cleaned.drop_duplicates()
            stats['duplicates_removed'] = before - len(df_cleaned)
        
        # Handle missing values
        if handle_missing:
            numeric_cols = df_cleaned.select_dtypes(include=[np.number]).columns
            for col in numeric_cols:
                missing_before = df_cleaned[col].isnull().sum()
                df_cleaned[col].fillna(df_cleaned[col].median(), inplace=True)
                stats['missing_filled'] += missing_before
            
            # Fill categorical with mode
            cat_cols = df_cleaned.select_dtypes(include=['object']).columns
            for col in cat_cols:
                if df_cleaned[col].isnull().sum() > 0:
                    mode_val = df_cleaned[col].mode()[0] if len(df_cleaned[col].mode()) > 0 else 'Unknown'
                    df_cleaned[col].fillna(mode_val, inplace=True)
        
        # Handle outliers using IQR method
        if handle_outliers:
            numeric_cols = df_cleaned.select_dtypes(include=[np.number]).columns
            before = len(df_cleaned)
            
            for col in numeric_cols:
                Q1 = df_cleaned[col].quantile(0.25)
                Q3 = df_cleaned[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                df_cleaned = df_cleaned[(df_cleaned[col] >= lower_bound) & (df_cleaned[col] <= upper_bound)]
            
            stats['outliers_removed'] = before - len(df_cleaned)
        
        stats['rows_after'] = len(df_cleaned)
        
        self.df = df_cleaned
        return df_cleaned, stats
    
    def transform_data(self, method='standardize', exclude_cols=None) -> tuple:
        """
        Transform numeric columns
        
        Args:
            method: Transformation method ('standardize', 'normalize', 'robust')
            exclude_cols: List of columns to exclude from transformation
        
        Returns:
            Tuple of (transformed_df, scaler, num_columns_transformed)
        """
        if self.df is None:
            self.load_data()
        
        df_transformed = self.df.copy()
        
        # Get numeric columns
        numeric_cols = df_transformed.select_dtypes(include=[np.number]).columns.tolist()
        
        # Exclude specified columns
        if exclude_cols is None:
            exclude_cols = ['id', 'label']
        
        numeric_cols = [col for col in numeric_cols if col not in exclude_cols]
        
        # Apply transformation
        if method == 'standardize':
            scaler = StandardScaler()
        elif method == 'normalize':
            scaler = MinMaxScaler()
        elif method == 'robust':
            scaler = RobustScaler()
        else:
            scaler = StandardScaler()
        
        df_transformed[numeric_cols] = scaler.fit_transform(df_transformed[numeric_cols])
        
        self.df = df_transformed
        return df_transformed, scaler, len(numeric_cols)
    
    def save_data(self, output_file: Path):
        """Save current dataframe to CSV"""
        if self.df is None:
            raise Exception("No data to save")
        
        self.df.to_csv(output_file, index=False)
    
    def save_scaler(self, scaler, output_file: Path):
        """Save scaler to pickle file"""
        with open(output_file, 'wb') as f:
            pickle.dump(scaler, f)

class ModelTrainer:
    """Class for training ML models"""
    
    def __init__(self, df: pd.DataFrame):
        """
        Initialize with dataframe
        
        Args:
            df: DataFrame with features and labels
        """
        self.df = df
    
    def prepare_data(self, feature_cols=None, label_col='label', test_size=0.2):
        """
        Prepare data for training
        
        Args:
            feature_cols: List of feature column names
            label_col: Name of label column
            test_size: Proportion of test set
        
        Returns:
            Tuple of (X_train, X_test, y_train, y_test, scaler)
        """
        from sklearn.model_selection import train_test_split
        from sklearn.preprocessing import StandardScaler
        
        if feature_cols is None:
            feature_cols = ['calories', 'proteins', 'fat', 'carbohydrate']
        
        # Check if label column exists
        if label_col not in self.df.columns:
            raise Exception(f"Label column '{label_col}' not found in dataset")
        
        X = self.df[feature_cols].values
        y = self.df[label_col].values
        
        # Convert string labels to numeric if needed
        if y.dtype == 'object':
            label_mapping = {
                'Sangat Buruk': 0,
                'Buruk': 1,
                'Baik': 2,
                'Sangat Baik': 3
            }
            y = np.array([label_mapping.get(label, 2) for label in y])
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42
        )
        
        # Scale features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        return X_train_scaled, X_test_scaled, y_train, y_test, scaler
    
    def train_model(self, model_type, X_train, y_train, X_test, y_test):
        """
        Train a specific model type
        
        Args:
            model_type: Type of model to train
            X_train, y_train: Training data
            X_test, y_test: Test data
        
        Returns:
            Dictionary with model and metrics
        """
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.naive_bayes import GaussianNB
        from sklearn.svm import SVC
        from sklearn.cluster import KMeans
        from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
        
        # Initialize model
        if model_type == 'random_forest':
            model = RandomForestClassifier(n_estimators=100, random_state=42)
        elif model_type == 'naive_bayes':
            model = GaussianNB()
        elif model_type == 'svm':
            model = SVC(kernel='rbf', probability=True, random_state=42)
        elif model_type == 'kmeans':
            model = KMeans(n_clusters=4, random_state=42)
        else:
            raise ValueError(f"Invalid model type: {model_type}")
        
        # Train model
        model.fit(X_train, y_train)
        
        # Predict
        y_pred = model.predict(X_test)
        
        # Calculate metrics
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
        recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
        f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
        cm = confusion_matrix(y_test, y_pred)
        
        return {
            'model': model,
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1,
            'confusion_matrix': cm
        }
    
    def save_model(self, model, output_file: Path):
        """Save model to pickle file"""
        with open(output_file, 'wb') as f:
            pickle.dump(model, f)
