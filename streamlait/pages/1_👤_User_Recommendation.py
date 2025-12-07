"""
User Recommendation Page - Real-time ML Predictions
Displays food recommendations with diet goal presets and custom filtering
"""

import streamlit as st
import pandas as pd
import pickle
import numpy as np
import os
import time
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Rekomendasi Makanan",
    page_icon="🥗",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #2E7D32 0%, #66BB6A 50%, #A5D6A7 100%);
    }
    
    .quality-sangat-baik {
        background: #4CAF50;
        color: white;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
    }
    
    .quality-baik {
        background: #8BC34A;
        color: white;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
    }
    
    .quality-buruk {
        background: #FF9800;
        color: white;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
    }
    
    .quality-sangat-buruk {
        background: #F44336;
        color: white;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
    }
    
    .food-card {
        background: white;
        border-radius: 15px;
        padding: 1rem;
        box-shadow: 0 5px 20px rgba(0,0,0,0.15);
        margin-bottom: 1rem;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #2E7D32 0%, #388E3C 100%);
        color: white;
        font-weight: 600;
        border-radius: 10px;
        border: none;
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #1B5E20 0%, #2E7D32 100%);
    }
</style>
""", unsafe_allow_html=True)

# Get project root directory
PROJECT_ROOT = Path(__file__).parent.parent.parent / "websait"

# Quality ranking for filtering
QUALITY_RANK = {
    'Sangat Baik': 4,
    'Baik': 3,
    'Buruk': 2,
    'Sangat Buruk': 1
}

# Label mapping
LABEL_MAPPING = {
    0: 'Sangat Buruk',
    1: 'Buruk',
    2: 'Baik',
    3: 'Sangat Baik'
}

@st.cache_resource
def load_model(model_type):
    """Load ML model and scaler"""
    model_files = {
        'random_forest': ('random_forest_model.pkl', 'random_forest_scaler.pkl'),
        'naive_bayes': ('naive_bayes_model.pkl', 'naive_bayes_scaler.pkl'),
        'svm': ('svm_model.pkl', 'svm_scaler.pkl'),
        'kmeans': ('kmeans_model.pkl', 'kmeans_scaler.pkl')
    }
    
    model_file, scaler_file = model_files.get(model_type, model_files['random_forest'])
    
    try:
        model_path = PROJECT_ROOT / model_file
        scaler_path = PROJECT_ROOT / scaler_file
        
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        with open(scaler_path, 'rb') as f:
            scaler = pickle.load(f)
        
        return model, scaler
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        return None, None

@st.cache_data
def load_nutrition_data():
    """Load nutrition data from CSV"""
    try:
        csv_path = PROJECT_ROOT / "nutrition_data.csv"
        df = pd.read_csv(csv_path, encoding='utf-8-sig')
        return df
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None

def predict_food_quality(model, scaler, food_data):
    """Predict quality for a single food item"""
    try:
        # Extract features
        features = np.array([[
            float(food_data['calories']),
            float(food_data['proteins']),
            float(food_data['fat']),
            float(food_data['carbohydrate'])
        ]])
        
        # Scale features
        features_scaled = scaler.transform(features)
        
        # Predict
        prediction = model.predict(features_scaled)[0]
        
        # Get confidence if available
        if hasattr(model, 'predict_proba'):
            probabilities = model.predict_proba(features_scaled)[0]
            confidence = float(np.max(probabilities)) * 100
        else:
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

def predict_batch(model, scaler, foods_df):
    """Predict quality for all foods in batch"""
    predictions = []
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    total_foods = len(foods_df)
    for idx, (_, food) in enumerate(foods_df.iterrows()):
        pred = predict_food_quality(model, scaler, food)
        predictions.append(pred)
        
        # Update progress
        progress = (idx + 1) / total_foods
        progress_bar.progress(progress)
        status_text.text(f"Memprediksi makanan {idx + 1}/{total_foods}...")
    
    progress_bar.empty()
    status_text.empty()
    
    return predictions

def get_quality_badge_html(label, confidence):
    """Generate HTML for quality badge"""
    label_lower = label.lower().replace(' ', '-')
    return f"""
    <div class="quality-{label_lower}">
        {label} 🤖 AI: {confidence}% yakin
    </div>
    """

def display_food_card(food, prediction):
    """Display a single food card"""
    with st.container():
        col1, col2 = st.columns([1, 3])
        
        with col1:
            if 'image' in food and pd.notna(food['image']):
                st.image(food['image'], use_container_width=True)
            else:
                st.image("https://via.placeholder.com/200x200?text=No+Image", use_container_width=True)
        
        with col2:
            st.markdown(f"### {food['name']}")
            st.markdown(get_quality_badge_html(prediction['label_name'], prediction['confidence']), unsafe_allow_html=True)
            
            col_a, col_b, col_c, col_d = st.columns(4)
            with col_a:
                st.metric("Kalori", f"{food['calories']:.1f}")
            with col_b:
                st.metric("Protein", f"{food['proteins']:.1f}g")
            with col_c:
                st.metric("Lemak", f"{food['fat']:.1f}g")
            with col_d:
                st.metric("Karbo", f"{food['carbohydrate']:.1f}g")
            
            with st.expander("🔍 Lihat Detail Lengkap"):
                st.markdown(f"""
                **Informasi Nutrisi Lengkap:**
                - **ID:** {food.get('id', 'N/A')}
                - **Kalori:** {food['calories']:.1f} kcal
                - **Protein:** {food['proteins']:.1f} g
                - **Lemak:** {food['fat']:.1f} g
                - **Karbohidrat:** {food['carbohydrate']:.1f} g
                
                **Prediksi Model:**
                - **Kualitas:** {prediction['label_name']}
                - **Confidence:** {prediction['confidence']}%
                - **🔥 REAL-TIME PREDICTION** - Model ML dipanggil langsung
                """)

def main():
    """Main user recommendation page"""
    
    # Header
    st.title("🥗 Sistem Rekomendasi Makanan Sehat")
    st.markdown("Dapatkan rekomendasi makanan personal berdasarkan kebutuhan nutrisi Anda")
    
    if st.button("← Kembali ke Beranda"):
        st.switch_page("app.py")
    
    st.markdown("---")
    
    # Load data
    df = load_nutrition_data()
    if df is None:
        st.error("Gagal memuat data makanan. Pastikan file nutrition_data.csv tersedia.")
        return
    
    # Model selector
    st.markdown("### 🤖 Pilih Model Machine Learning")
    model_options = {
        "Random Forest (92.59% Akurasi) ⭐": "random_forest",
        "Naive Bayes": "naive_bayes",
        "SVM (Support Vector Machine)": "svm",
        "K-Means Clustering": "kmeans"
    }
    selected_model_name = st.selectbox("Model:", list(model_options.keys()))
    selected_model = model_options[selected_model_name]
    
    st.info("🔥 **REAL-TIME PREDICTION:** Model ML aktif memprediksi setiap makanan saat dimuat!")
    
    # Diet goal presets
    st.markdown("### 🎯 Pilih Tujuan Diet Anda")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🏃 Turun Berat", use_container_width=True):
            st.session_state.max_calories = 200
            st.session_state.min_protein = 15
            st.session_state.min_quality = 'Baik'
    
    with col2:
        if st.button("💪 Nambah Otot", use_container_width=True):
            st.session_state.max_calories = 400
            st.session_state.min_protein = 25
            st.session_state.min_quality = 'Baik'
    
    with col3:
        if st.button("🥗 Sehat Seimbang", use_container_width=True):
            st.session_state.max_calories = 300
            st.session_state.min_protein = 10
            st.session_state.min_quality = 'Sangat Baik'
    
    with col4:
        if st.button("🔥 Rendah Kalori", use_container_width=True):
            st.session_state.max_calories = 150
            st.session_state.min_protein = 5
            st.session_state.min_quality = 'Baik'
    
    # Criteria inputs
    st.markdown("### 📊 Kriteria Detail")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        max_calories = st.number_input(
            "Target Kalori (max):",
            min_value=0,
            value=st.session_state.get('max_calories', 300),
            step=10
        )
    
    with col2:
        min_protein = st.number_input(
            "Protein Minimum (g):",
            min_value=0,
            value=st.session_state.get('min_protein', 10),
            step=1
        )
    
    with col3:
        min_quality = st.selectbox(
            "Kualitas Minimum:",
            options=['Sangat Baik', 'Baik', 'Buruk', 'Sangat Buruk'],
            index=['Sangat Baik', 'Baik', 'Buruk', 'Sangat Buruk'].index(
                st.session_state.get('min_quality', 'Baik')
            )
        )
    
    # Search box
    search_query = st.text_input("🔎 Cari makanan spesifik (opsional):", placeholder="contoh: ayam, tahu, tempe")
    
    # Get recommendations button
    if st.button("🔍 Dapatkan Rekomendasi", use_container_width=True):
        st.session_state.show_recommendations = True
        st.session_state.search_query = search_query
    
    # Show recommendations
    if st.session_state.get('show_recommendations', False):
        st.markdown("---")
        st.markdown("### 🔥 Memproses Prediksi Real-Time")
        
        # Load model
        with st.spinner(f"Memuat model {selected_model_name}..."):
            model, scaler = load_model(selected_model)
        
        if model is None or scaler is None:
            st.error("Gagal memuat model ML. Pastikan file model tersedia.")
            return
        
        # Predict all foods
        start_time = time.time()
        predictions = predict_batch(model, scaler, df)
        prediction_time = time.time() - start_time
        
        st.success(f"✅ Prediksi selesai dalam {prediction_time:.2f} detik untuk {len(df)} makanan!")
        
        # Add predictions to dataframe
        df['label'] = [p['label_name'] for p in predictions]
        df['confidence'] = [p['confidence'] for p in predictions]
        quality_counts = df['label'].value_counts().to_dict()
        quality_summary = " | ".join([
            f"{label}: {count}" for label, count in quality_counts.items()
        ]) if quality_counts else "Tidak ada prediksi"
        
        # Filter by criteria
        min_quality_rank = QUALITY_RANK[min_quality]
        criteria_mask = (
            (df['calories'] <= max_calories) &
            (df['proteins'] >= min_protein) &
            (df['label'].map(QUALITY_RANK) >= min_quality_rank)
        )
        filtered_df = df[criteria_mask].copy()
        
        # Apply search filter
        if st.session_state.get('search_query', ''):
            search_query = st.session_state.search_query.lower()
            filtered_df = filtered_df[
                filtered_df['name'].str.lower().str.contains(search_query, na=False)
            ]
        
        # Sort by quality and protein
        filtered_df['quality_rank'] = filtered_df['label'].map(QUALITY_RANK)
        filtered_df = filtered_df.sort_values(
            by=['quality_rank', 'proteins'],
            ascending=[False, False]
        )
        
        # Display summary
        if len(filtered_df) > 0:
            avg_calories = filtered_df['calories'].mean()
            avg_protein = filtered_df['proteins'].mean()
            sangat_baik = len(filtered_df[filtered_df['label'] == 'Sangat Baik'])
            baik = len(filtered_df[filtered_df['label'] == 'Baik'])
            
            st.success(f"""
            **✅ Ditemukan {len(filtered_df)} makanan yang sesuai!**
            
            📊 Rata-rata: {avg_calories:.1f} kcal, {avg_protein:.1f}g protein
            
            🌟 Kualitas: {sangat_baik} Sangat Baik, {baik} Baik
            """)
            
            # Display recommendations
            st.markdown("### 🍽️ Rekomendasi Makanan")
            
            for idx, (_, food) in enumerate(filtered_df.iterrows()):
                pred_idx = df[df['id'] == food['id']].index[0]
                prediction = predictions[pred_idx]
                display_food_card(food, prediction)
                
                if idx >= 19:  # Limit to 20 results
                    st.info(f"Menampilkan 20 dari {len(filtered_df)} hasil. Sesuaikan kriteria untuk hasil lebih spesifik.")
                    break
        else:
            st.warning("""
            **❌ Tidak ada makanan yang memenuhi kriteria.**
            
            Coba sesuaikan kriteria Anda.
            """)
            # Explain why no rows matched so users know it's not a UI bug
            calorie_pool = df[df['calories'] <= max_calories]
            protein_pool = calorie_pool[calorie_pool['proteins'] >= min_protein]
            diagnostics = []
            if calorie_pool.empty:
                diagnostics.append(
                    f"Tidak ada makanan dengan kalori ≤ {max_calories} kcal."
                )
            elif protein_pool.empty:
                diagnostics.append(
                    f"{len(calorie_pool)} makanan lolos batas kalori, tetapi semuanya memiliki protein < {min_protein} g."
                )
            else:
                diagnostics.append(
                    f"{len(protein_pool)} makanan memenuhi batas kalori dan protein."
                )
                quality_pool = protein_pool[
                    protein_pool['label'].map(QUALITY_RANK) >= min_quality_rank
                ]
                diagnostics.append(
                    f"Model hanya memprediksi {quality_counts.get(min_quality, 0)} makanan dengan kualitas {min_quality}."
                )
                if quality_pool.empty and not protein_pool.empty:
                    best_quality_candidate = protein_pool.assign(
                        quality_rank=protein_pool['label'].map(QUALITY_RANK)
                    ).sort_values('quality_rank', ascending=False)
                    if not best_quality_candidate.empty:
                        best_quality = best_quality_candidate.iloc[0]['label']
                        diagnostics.append(
                            f"Kualitas terbaik yang tersedia untuk batas kalori/protein ini adalah {best_quality}."
                        )
            if quality_summary:
                diagnostics.append(f"Distribusi kualitas saat ini → {quality_summary}")
            for msg in diagnostics:
                st.info(msg)

if __name__ == "__main__":
    main()
