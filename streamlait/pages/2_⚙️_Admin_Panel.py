"""
Admin Panel Page - Data Management and Model Configuration
Handles data preprocessing, cleaning, transformation, and model training
"""

import streamlit as st
import pandas as pd
import numpy as np
import json
import pickle
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.cluster import KMeans
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

# Page configuration
st.set_page_config(
    page_title="Admin Panel",
    page_icon="⚙️",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        background: #f5f5f5;
    }
    
    .stat-card {
        background: linear-gradient(135deg, #2E7D32 0%, #388E3C 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #2E7D32 0%, #388E3C 100%);
        color: white;
        font-weight: 600;
        border-radius: 8px;
        border: none;
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #1B5E20 0%, #2E7D32 100%);
    }
</style>
""", unsafe_allow_html=True)

# Get project root directory
PROJECT_ROOT = Path(__file__).parent.parent.parent / "websait"

# File paths
DATA_FILE = PROJECT_ROOT / 'nutrition_data.csv'
CLEANED_DATA_FILE = PROJECT_ROOT / 'nutrition_data_cleaned.csv'

@st.cache_data
def load_data():
    """Load nutrition data from CSV"""
    try:
        if CLEANED_DATA_FILE.exists():
            df = pd.read_csv(CLEANED_DATA_FILE, encoding='utf-8-sig')
            st.info("📂 Loaded cleaned data")
        else:
            df = pd.read_csv(DATA_FILE, encoding='utf-8-sig')
            st.info("📂 Loaded original data")
        return df
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None

def boost_high_quality_samples(df, target_label='Sangat Baik', min_ratio=0.25):
    """Oversample target_label rows to ensure it reaches a minimum ratio"""
    if 'label' not in df.columns:
        return df, {'before': {}, 'after': {}, 'target_label': target_label, 'boost_factor': 1}
    label_counts = df['label'].value_counts().to_dict()
    target_count = label_counts.get(target_label, 0)
    majority_count = max(label_counts.values()) if label_counts else 0
    desired_count = max(int(np.ceil(majority_count * min_ratio)), target_count)
    if target_count == 0 or desired_count <= target_count:
        return df, {'before': label_counts, 'after': label_counts, 'target_label': target_label, 'boost_factor': 1}
    repeat_factor = int(np.ceil(desired_count / target_count))
    target_df = df[df['label'] == target_label]
    boosted_df = pd.concat([df] + [target_df] * (repeat_factor - 1), ignore_index=True)
    boosted_df = boosted_df.sample(frac=1.0, random_state=42).reset_index(drop=True)
    boosted_counts = boosted_df['label'].value_counts().to_dict()
    return boosted_df, {
        'before': label_counts,
        'after': boosted_counts,
        'target_label': target_label,
        'boost_factor': repeat_factor
    }

def get_data_stats(df):
    """Calculate data statistics"""
    numeric_df = df.select_dtypes(include=[np.number])
    
    stats = {
        'total_rows': len(df),
        'total_columns': len(df.columns),
        'missing_values': int(df.isnull().sum().sum()),
        'duplicates': int(df.duplicated().sum()),
        'numeric_columns': len(numeric_df.columns),
        'categorical_columns': len(df.select_dtypes(include=['object']).columns)
    }
    
    return stats

def clean_data(df, remove_duplicates=False, handle_missing=False, handle_outliers=False):
    """Clean the dataset"""
    df_cleaned = df.copy()
    
    stats = {
        'rows_before': len(df),
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
    
    return df_cleaned, stats

def transform_data(df, method='standardize'):
    """Transform numeric data"""
    df_transformed = df.copy()
    
    # Get numeric columns (excluding id and label)
    numeric_cols = df_transformed.select_dtypes(include=[np.number]).columns.tolist()
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
    
    # Save scaler
    scaler_path = PROJECT_ROOT / 'data_scaler.pkl'
    with open(scaler_path, 'wb') as f:
        pickle.dump(scaler, f)
    
    return df_transformed, len(numeric_cols)

def train_model(df, model_type, test_size=0.2):
    """Train ML model"""
    # Prepare features and labels
    feature_cols = ['calories', 'proteins', 'fat', 'carbohydrate']
    
    # Check if label column exists
    if 'label' not in df.columns:
        st.error("Dataset tidak memiliki kolom 'label'. Pastikan data sudah dilabeli.")
        return None
    
    df_balanced, balance_info = boost_high_quality_samples(df)
    X = df_balanced[feature_cols].values
    y = df_balanced['label'].values
    
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
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train model
    if model_type == 'random_forest':
        model = RandomForestClassifier(n_estimators=100, random_state=42)
    elif model_type == 'naive_bayes':
        model = GaussianNB()
    elif model_type == 'svm':
        model = SVC(kernel='rbf', probability=True, random_state=42)
    elif model_type == 'kmeans':
        model = KMeans(n_clusters=4, random_state=42)
    else:
        model = RandomForestClassifier(n_estimators=100, random_state=42)
    
    # Fit model
    model.fit(X_train_scaled, y_train)
    
    # Predict
    y_pred = model.predict(X_test_scaled)
    
    # Calculate metrics
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
    recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
    f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
    
    # Save model and scaler
    model_path = PROJECT_ROOT / f'{model_type}_model.pkl'
    scaler_path = PROJECT_ROOT / f'{model_type}_scaler.pkl'
    
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    with open(scaler_path, 'wb') as f:
        pickle.dump(scaler, f)
    
    results = {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1_score': f1,
        'confusion_matrix': confusion_matrix(y_test, y_pred),
        'balance_info': balance_info
    }
    
    return results

def main():
    """Main admin panel"""
    
    # Header
    st.title("⚙️ Admin Panel - Analisis Gizi Makanan")
    
    if st.button("← Kembali ke Beranda"):
        st.switch_page("app.py")
    
    st.markdown("---")
    
    # Tabs
    tab1, tab2, tab3 = st.tabs(["📊 Data Preprocessing", "🤖 Model Configuration", "📈 Data Visualization"])
    
    # Tab 1: Data Preprocessing
    with tab1:
        st.header("📊 Dataset Preview")
        
        # Load data
        df = load_data()
        if df is None:
            st.error("Gagal memuat data. Pastikan file nutrition_data.csv tersedia.")
            return
        
        # Display stats
        stats = get_data_stats(df)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"""
            <div class="stat-card">
                <h3>Total Data</h3>
                <h2>{stats['total_rows']}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="stat-card">
                <h3>Kolom</h3>
                <h2>{stats['total_columns']}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="stat-card">
                <h3>Missing Values</h3>
                <h2>{stats['missing_values']}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="stat-card">
                <h3>Duplikat</h3>
                <h2>{stats['duplicates']}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Data preview
        st.subheader("Preview Data (50 baris pertama)")
        st.dataframe(df.head(50), use_container_width=True, height=400)
        
        # Data cleaning
        st.markdown("---")
        st.subheader("🧹 Data Cleaning")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            remove_duplicates = st.checkbox("Hapus Duplikat", value=False)
        with col2:
            handle_missing = st.checkbox("Tangani Missing Values", value=False)
        with col3:
            handle_outliers = st.checkbox("Tangani Outliers", value=False)
        
        if st.button("Bersihkan Data", use_container_width=True):
            with st.spinner("Membersihkan data..."):
                df_cleaned, clean_stats = clean_data(df, remove_duplicates, handle_missing, handle_outliers)
                
                # Save cleaned data
                df_cleaned.to_csv(CLEANED_DATA_FILE, index=False)
                
                st.success("✅ Data berhasil dibersihkan!")
                st.json(clean_stats)
                
                # Clear cache to reload data
                st.cache_data.clear()
                st.rerun()
        
        # Data transformation
        st.markdown("---")
        st.subheader("🔄 Data Transformation")
        
        transform_method = st.selectbox(
            "Pilih metode transformasi:",
            options=['standardize', 'normalize', 'robust'],
            format_func=lambda x: {
                'standardize': 'Standardization (Z-score)',
                'normalize': 'Normalization (Min-Max)',
                'robust': 'Robust Scaling'
            }[x]
        )
        
        if st.button("Transformasi Data", use_container_width=True):
            with st.spinner("Mentransformasi data..."):
                df_transformed, num_cols = transform_data(df, transform_method)
                
                # Save transformed data
                df_transformed.to_csv(CLEANED_DATA_FILE, index=False)
                
                st.success(f"✅ {num_cols} kolom berhasil ditransformasi dengan metode {transform_method}!")
                
                # Clear cache
                st.cache_data.clear()
                st.rerun()
    
    # Tab 2: Model Configuration
    with tab2:
        st.header("🤖 Model Configuration")
        
        # Load data
        df = load_data()
        if df is None:
            st.error("Gagal memuat data.")
            return
        
        st.markdown("### Train Machine Learning Models")
        
        col1, col2 = st.columns(2)
        
        with col1:
            model_type = st.selectbox(
                "Pilih tipe model:",
                options=['random_forest', 'naive_bayes', 'svm', 'kmeans'],
                format_func=lambda x: {
                    'random_forest': 'Random Forest',
                    'naive_bayes': 'Naive Bayes',
                    'svm': 'SVM (Support Vector Machine)',
                    'kmeans': 'K-Means Clustering'
                }[x]
            )
        
        with col2:
            test_size = st.slider("Test Size (%):", min_value=10, max_value=40, value=20, step=5) / 100
        
        if st.button("🚀 Train Model", use_container_width=True):
            with st.spinner(f"Training {model_type} model..."):
                results = train_model(df, model_type, test_size)
                
                if results:
                    st.success(f"✅ Model {model_type} berhasil dilatih!")
                    
                    # Display metrics
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Accuracy", f"{results['accuracy']*100:.2f}%")
                    with col2:
                        st.metric("Precision", f"{results['precision']*100:.2f}%")
                    with col3:
                        st.metric("Recall", f"{results['recall']*100:.2f}%")
                    with col4:
                        st.metric("F1-Score", f"{results['f1_score']*100:.2f}%")
                    
                    # Confusion matrix
                    st.markdown("### Confusion Matrix")
                    fig, ax = plt.subplots(figsize=(10, 8))
                    sns.heatmap(
                        results['confusion_matrix'],
                        annot=True,
                        fmt='d',
                        cmap='Greens',
                        xticklabels=['Sangat Buruk', 'Buruk', 'Baik', 'Sangat Baik'],
                        yticklabels=['Sangat Buruk', 'Buruk', 'Baik', 'Sangat Baik'],
                        ax=ax
                    )
                    ax.set_xlabel('Predicted')
                    ax.set_ylabel('Actual')
                    ax.set_title('Confusion Matrix')
                    st.pyplot(fig)
                    plt.close()
                    balance_info = results.get('balance_info', {})
                    if balance_info:
                        st.caption("Distribusi label setelah strategi balancing kelas:")
                        st.json(balance_info)
    
    # Tab 3: Data Visualization
    with tab3:
        st.header("📈 Data Visualization")
        
        # Load data
        df = load_data()
        if df is None:
            st.error("Gagal memuat data.")
            return
        
        # Distribution plots
        st.subheader("Distribusi Nutrisi")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.hist(df['calories'].dropna(), bins=50, color='#4CAF50', edgecolor='black', alpha=0.7)
            ax.set_title('Distribusi Kalori', fontsize=14, fontweight='bold')
            ax.set_xlabel('Calories')
            ax.set_ylabel('Frequency')
            ax.grid(axis='y', alpha=0.3)
            st.pyplot(fig)
            plt.close()
            
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.hist(df['fat'].dropna(), bins=50, color='#FF9800', edgecolor='black', alpha=0.7)
            ax.set_title('Distribusi Lemak', fontsize=14, fontweight='bold')
            ax.set_xlabel('Fat (g)')
            ax.set_ylabel('Frequency')
            ax.grid(axis='y', alpha=0.3)
            st.pyplot(fig)
            plt.close()
        
        with col2:
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.hist(df['proteins'].dropna(), bins=50, color='#2196F3', edgecolor='black', alpha=0.7)
            ax.set_title('Distribusi Protein', fontsize=14, fontweight='bold')
            ax.set_xlabel('Proteins (g)')
            ax.set_ylabel('Frequency')
            ax.grid(axis='y', alpha=0.3)
            st.pyplot(fig)
            plt.close()
            
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.hist(df['carbohydrate'].dropna(), bins=50, color='#FFC107', edgecolor='black', alpha=0.7)
            ax.set_title('Distribusi Karbohidrat', fontsize=14, fontweight='bold')
            ax.set_xlabel('Carbohydrate (g)')
            ax.set_ylabel('Frequency')
            ax.grid(axis='y', alpha=0.3)
            st.pyplot(fig)
            plt.close()
        
        # Scatter plots
        if 'label' in df.columns:
            st.subheader("Scatter Plots by Label")
            
            fig, ax = plt.subplots(figsize=(12, 8))
            
            color_map = {
                'Sangat Baik': '#4CAF50',
                'Baik': '#8BC34A',
                'Buruk': '#FF9800',
                'Sangat Buruk': '#F44336'
            }
            
            for label in df['label'].unique():
                if pd.notna(label):
                    mask = df['label'] == label
                    ax.scatter(
                        df[mask]['calories'],
                        df[mask]['proteins'],
                        label=label,
                        color=color_map.get(label, '#999999'),
                        alpha=0.6,
                        s=50
                    )
            
            ax.set_xlabel('Calories', fontsize=12)
            ax.set_ylabel('Proteins (g)', fontsize=12)
            ax.set_title('Calories vs Proteins by Label', fontsize=14, fontweight='bold')
            ax.legend()
            ax.grid(True, alpha=0.3)
            st.pyplot(fig)
            plt.close()
        
        # Correlation heatmap
        st.subheader("Correlation Heatmap")
        numeric_df = df.select_dtypes(include=[np.number])
        corr = numeric_df.corr()
        
        fig, ax = plt.subplots(figsize=(12, 10))
        sns.heatmap(
            corr,
            annot=True,
            fmt='.2f',
            cmap='RdYlGn',
            center=0,
            square=True,
            linewidths=1,
            cbar_kws={"shrink": 0.8},
            ax=ax
        )
        ax.set_title('Correlation Matrix', fontsize=14, fontweight='bold')
        plt.xticks(rotation=45, ha='right')
        plt.yticks(rotation=0)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

if __name__ == "__main__":
    main()
