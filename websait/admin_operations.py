import sys
import json
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.cluster import KMeans
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from scipy import stats
import time
import pickle

# Global variables
DATA_FILE = 'nutrition_data.csv'
CLEANED_DATA_FILE = 'nutrition_data_cleaned.csv'
df = None

def load_csv_data():
    global df
    try:
        df = pd.read_csv(DATA_FILE)
        return df
    except Exception as e:
        return None

def load_data():
    global df
    df = load_csv_data()
    
    if df is None:
        print(json.dumps({'error': 'Failed to load data'}))
        return
    
    # Get numeric columns only
    numeric_df = df.select_dtypes(include=[np.number])
    
    # Data types info
    dtypes_info = []
    for col in df.columns:
        dtypes_info.append({
            'column': col,
            'dtype': str(df[col].dtype),
            'non_null': int(df[col].count())
        })
    
    # Descriptive statistics
    desc_stats = numeric_df.describe().to_dict()
    
    # Skewness analysis
    skewness_data = []
    for col in numeric_df.columns:
        skewness_data.append({
            'column': col,
            'skewness': float(numeric_df[col].skew())
        })
    
    # Missing values count
    missing_count = int(df.isnull().sum().sum())
    
    # Duplicate count
    duplicate_count = int(df.duplicated().sum())
    
    result = {
        'rows': df.to_dict('records'),
        'preview': df.head(50).to_dict('records'),
        'columns': df.columns.tolist(),
        'dtypes': dtypes_info,
        'descriptive_stats': desc_stats,
        'skewness': skewness_data,
        'missing_count': missing_count,
        'duplicate_count': duplicate_count
    }
    
    print(json.dumps(result))

def clean_data():
    global df
    
    if df is None:
        df = load_csv_data()
    
    try:
        if len(sys.argv) > 2:
            if sys.argv[1] == 'clean_data_file':
                with open(sys.argv[2], 'r') as f:
                    options = json.loads(f.read())
            else:
                options = json.loads(sys.argv[2])
        else:
            options = {'remove_duplicates': False, 'handle_missing': False, 'handle_outliers': False}
    except Exception as e:
        options = {'remove_duplicates': False, 'handle_missing': False, 'handle_outliers': False}
    
    rows_before = len(df)
    duplicates_removed = 0
    outliers_removed = 0
    missing_filled = 0
    
    # Remove duplicates
    if options.get('remove_duplicates', False):
        before = len(df)
        df = df.drop_duplicates()
        duplicates_removed = before - len(df)
    
    # Handle missing values
    if options.get('handle_missing', False):
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            missing_before = df[col].isnull().sum()
            df[col].fillna(df[col].median(), inplace=True)
            missing_filled += missing_before
        
        # Fill categorical with mode
        cat_cols = df.select_dtypes(include=['object']).columns
        for col in cat_cols:
            if df[col].isnull().sum() > 0:
                df[col].fillna(df[col].mode()[0] if len(df[col].mode()) > 0 else 'Unknown', inplace=True)
    
    # Handle outliers using IQR method
    if options.get('handle_outliers', False):
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        before = len(df)
        
        for col in numeric_cols:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]
        
        outliers_removed = before - len(df)
    
    rows_after = len(df)
    
    # Save cleaned data
    df.to_csv(CLEANED_DATA_FILE, index=False)
    
    result = {
        'rows_before': rows_before,
        'rows_after': rows_after,
        'duplicates_removed': duplicates_removed,
        'outliers_removed': outliers_removed,
        'missing_filled': missing_filled
    }
    
    print(json.dumps(result))

def transform_data():
    global df
    
    if df is None:
        df = load_csv_data()
    
    method = sys.argv[2] if len(sys.argv) > 2 else 'standardize'
    
    # Get numeric columns (excluding id and label columns)
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
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
    
    df[numeric_cols] = scaler.fit_transform(df[numeric_cols])
    
    # Save transformed data
    df.to_csv(CLEANED_DATA_FILE, index=False)
    
    # Save scaler for later use
    with open('data_scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)
    
    result = {
        'method': method,
        'columns_transformed': len(numeric_cols)
    }
    
    print(json.dumps(result))

def train_model():
    global df
    
    if df is None:
        # Try to load cleaned data first, otherwise load original
        try:
            df = pd.read_csv(CLEANED_DATA_FILE)
        except:
            df = load_csv_data()
    
    try:
        if len(sys.argv) > 2:
            if sys.argv[1] == 'train_model_file':
                with open(sys.argv[2], 'r') as f:
                    params = json.loads(f.read())
            else:
                params = json.loads(sys.argv[2])
        else:
            params = {'model_type': 'random_forest', 'test_size': 0.2, 'random_state': 42}
    except Exception as e:
        params = {'model_type': 'random_forest', 'test_size': 0.2, 'random_state': 42}
    
    model_type = params.get('model_type', 'random_forest')
    test_size = float(params.get('test_size', 0.2))
    random_state = int(params.get('random_state', 42))
    
    # Prepare features and target
    # Use the nutrition features
    feature_cols = ['calories', 'proteins', 'fat', 'carbohydrate']
    
    # Check if label column exists
    if 'label' not in df.columns:
        print(json.dumps({'error': 'Label column not found'}))
        return
    
    X = df[feature_cols]
    
    # Encode labels
    label_map = {'Sangat Baik': 0, 'Baik': 1, 'Buruk': 2, 'Sangat Buruk': 3}
    y = df['label'].map(label_map)
    
    # Handle any missing mappings
    y = y.fillna(2)  # Default to 'Buruk'
    
    start_time = time.time()
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train model
    if model_type == 'random_forest':
        n_estimators = int(params.get('n_estimators', 100))
        max_depth = int(params.get('max_depth', 10))
        model = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth, random_state=random_state)
        model_name = 'Random Forest'
    elif model_type == 'naive_bayes':
        model = GaussianNB()
        model_name = 'Naive Bayes'
    elif model_type == 'svm':
        kernel = params.get('kernel', 'rbf')
        C = float(params.get('C', 1.0))
        model = SVC(kernel=kernel, C=C, random_state=random_state, probability=True)
        model_name = 'Support Vector Machine'
    elif model_type == 'kmeans':
        n_clusters = int(params.get('n_clusters', 4))
        max_iter = int(params.get('max_iter', 300))
        model = KMeans(n_clusters=n_clusters, max_iter=max_iter, random_state=random_state)
        model_name = 'K-Means Clustering'
    else:
        model = RandomForestClassifier(random_state=random_state)
        model_name = 'Random Forest'
    
    # Fit model
    if model_type == 'kmeans':
        model.fit(X_train_scaled)
        y_pred = model.predict(X_test_scaled)
        # For clustering, we don't have traditional accuracy
        accuracy = 0.0
        precision = 0.0
        recall = 0.0
        f1 = 0.0
    else:
        model.fit(X_train_scaled, y_train)
        y_pred = model.predict(X_test_scaled)
        
        # Calculate metrics
        accuracy = accuracy_score(y_test, y_pred) * 100
        precision = precision_score(y_test, y_pred, average='weighted', zero_division=0) * 100
        recall = recall_score(y_test, y_pred, average='weighted', zero_division=0) * 100
        f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0) * 100
    
    training_time = time.time() - start_time
    
    # Save model
    model_filename = f'{model_type}_model.pkl'
    with open(model_filename, 'wb') as f:
        pickle.dump(model, f)
    
    # Save scaler
    with open(f'{model_type}_scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)
    
    # Feature importance (for tree-based models)
    feature_importance = None
    if hasattr(model, 'feature_importances_'):
        feature_importance = {
            'features': feature_cols,
            'importance': model.feature_importances_.tolist()
        }
    
    # Confusion matrix
    conf_matrix = None
    if model_type != 'kmeans':
        conf_matrix = confusion_matrix(y_test, y_pred).tolist()
    
    result = {
        'model_name': model_name,
        'model_type': model_type,
        'accuracy': round(accuracy, 2),
        'precision': round(precision, 2),
        'recall': round(recall, 2),
        'f1_score': round(f1, 2),
        'training_time': round(training_time, 2),
        'test_size': test_size,
        'train_samples': len(X_train),
        'test_samples': len(X_test),
        'feature_importance': feature_importance,
        'confusion_matrix': conf_matrix
    }
    
    print(json.dumps(result))

# Main execution
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(json.dumps({'error': 'No action specified'}))
        sys.exit(1)
    
    action = sys.argv[1]
    
    if action == 'load_data':
        load_data()
    elif action == 'clean_data' or action == 'clean_data_file':
        clean_data()
    elif action == 'transform_data':
        transform_data()
    elif action == 'train_model' or action == 'train_model_file':
        train_model()
    else:
        print(json.dumps({'error': 'Invalid action'}))
