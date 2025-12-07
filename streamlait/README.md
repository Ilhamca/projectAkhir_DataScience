# 🥗 Sistem Rekomendasi Makanan Sehat - Streamlit Version

Platform cerdas berbasis Streamlit untuk analisis nutrisi dan rekomendasi makanan berkualitas menggunakan Machine Learning.

## 📋 Deskripsi

Sistem ini merupakan **versi Streamlit** yang identik dengan aplikasi PHP original, menyediakan:
- **Rekomendasi Personal**: Dapatkan rekomendasi makanan berdasarkan tujuan diet (turun berat, nambah otot, dll)
- **Real-time ML Prediction**: Prediksi kualitas makanan secara langsung menggunakan 4 model ML
- **Admin Panel**: Kelola data, preprocessing, dan training model
- **Visualisasi Interaktif**: Grafik dan analisis data nutrisi

## 🚀 Fitur Utama

### Untuk Pengguna
- ✅ **Preset Diet Goals**: 4 preset siap pakai (Weight Loss, Muscle Gain, Healthy Balanced, Low Calorie)
- ✅ **Custom Filtering**: Filter berdasarkan kalori, protein, dan kualitas
- ✅ **Real-time Predictions**: Prediksi kualitas makanan langsung dari model ML (.pkl files)
- ✅ **4 ML Models**: Random Forest (92.59% akurasi), Naive Bayes, SVM, K-Means
- ✅ **Confidence Scores**: Tampilan tingkat keyakinan AI untuk setiap prediksi
- ✅ **Color-coded Quality**: Badge warna untuk 4 tingkat kualitas (Sangat Baik, Baik, Buruk, Sangat Buruk)

### Untuk Admin
- ✅ **Data Preprocessing**: Cleaning, handling missing values, outlier removal
- ✅ **Data Transformation**: Standardization, Normalization, Robust Scaling
- ✅ **Model Training**: Train dan simpan model Random Forest, Naive Bayes, SVM, K-Means
- ✅ **Visualisasi Data**: Histogram, scatter plots, correlation heatmap
- ✅ **Model Evaluation**: Accuracy, precision, recall, F1-score, confusion matrix

## 📁 Struktur Folder

```
streamlait/
├── app.py                           # Main entry point (home page)
├── pages/
│   ├── 1_👤_User_Recommendation.py  # User recommendation interface
│   └── 2_⚙️_Admin_Panel.py          # Admin panel for data & models
├── utils/
│   ├── __init__.py
│   ├── predictor.py                 # ML prediction module
│   └── data_operations.py           # Data processing & model training
├── requirements.txt                 # Python dependencies
└── README.md                        # This file
```

## 🔧 Instalasi

### 1. Prerequisites
- Python 3.8 atau lebih tinggi
- Anaconda atau Python environment lainnya

### 2. Clone Repository
```bash
cd "d:\Semester 5\DataScience\Project"
```

### 3. Install Dependencies
```bash
cd streamlait
pip install -r requirements.txt
```

### 4. Pastikan File Data Tersedia
Sistem memerlukan file-file berikut di folder `websait` (folder parent):
- `nutrition_data.csv` - Dataset makanan Indonesia (1,346 items)
- Model files (`.pkl`):
  - `random_forest_model.pkl` & `random_forest_scaler.pkl`
  - `naive_bayes_model.pkl` & `naive_bayes_scaler.pkl`
  - `svm_model.pkl` & `svm_scaler.pkl`
  - `kmeans_model.pkl` & `kmeans_scaler.pkl`

> **Note**: Model files harus dilatih terlebih dahulu menggunakan Admin Panel atau Jupyter Notebook original

## 🎮 Cara Menggunakan

### Menjalankan Aplikasi
```bash
cd "d:\Semester 5\DataScience\Project\streamlait"
streamlit run app.py
```

Aplikasi akan terbuka di browser pada `http://localhost:8501`

### Workflow Pengguna

1. **Pilih Peran** di halaman utama:
   - 🥗 User Recommendation - Untuk mendapatkan rekomendasi
   - ⚙️ Admin Panel - Untuk kelola data & model

2. **User Recommendation**:
   - Pilih model ML (Random Forest recommended)
   - Pilih preset diet goal atau atur kriteria manual
   - Klik "Dapatkan Rekomendasi"
   - Sistem akan memprediksi 1,346 makanan secara real-time (3-5 detik)
   - Browse hasil dengan filter pencarian

3. **Admin Panel**:
   - **Tab Data Preprocessing**: 
     - Lihat preview & statistik data
     - Clean data (remove duplicates, handle missing values, outliers)
     - Transform data (standardization/normalization)
   - **Tab Model Configuration**:
     - Pilih model type
     - Train model dengan test size kustom
     - Lihat metrics & confusion matrix
   - **Tab Data Visualization**:
     - Histogram distribusi nutrisi
     - Scatter plots by label
     - Correlation heatmap

## 📊 Dataset

**nutrition_data.csv** berisi 1,346 makanan Indonesia dengan kolom:
- `id`: Unique identifier
- `calories`: Kalori (kcal)
- `proteins`: Protein (gram)
- `fat`: Lemak (gram)
- `carbohydrate`: Karbohidrat (gram)
- `name`: Nama makanan
- `image`: URL gambar
- `label`: Kualitas makanan (Sangat Baik, Baik, Buruk, Sangat Buruk)
- + 15 kolom fitur engineering lainnya

## 🤖 Model Machine Learning

### Random Forest (Recommended) ⭐
- **Accuracy**: 92.59%
- **Best for**: Balanced predictions dengan confidence tinggi
- **Speed**: Fast (~2-3 seconds untuk 1,346 foods)

### Naive Bayes
- **Good for**: Probabilistic predictions
- **Speed**: Very fast (~1-2 seconds)

### SVM (Support Vector Machine)
- **Good for**: High-dimensional data
- **Speed**: Moderate (~3-4 seconds)

### K-Means Clustering
- **Good for**: Unsupervised grouping
- **Speed**: Fast (~2 seconds)
- **Note**: No confidence scores (clustering-based)

## 🎨 Design Philosophy

### Color Scheme (Health-focused Green Theme)
- **Primary**: Green (#2E7D32, #4CAF50) - represents health, freshness, nutrition
- **Quality Badges**:
  - 🟢 Sangat Baik = Green (#4CAF50)
  - 🟢 Baik = Light Green (#8BC34A)
  - 🟠 Buruk = Orange (#FF9800)
  - 🔴 Sangat Buruk = Red (#F44336)

### Key Differences from PHP Version
| Feature | PHP Version | Streamlit Version |
|---------|-------------|-------------------|
| Technology | PHP + JavaScript | Python + Streamlit |
| Server | PHP built-in server | Streamlit server |
| UI Framework | Custom HTML/CSS | Streamlit components |
| State Management | JavaScript + LocalStorage | Session State |
| Real-time Updates | AJAX fetch | Streamlit rerun |
| Deployment | Requires PHP server | Can deploy to Streamlit Cloud |

## 🔄 Real-time Prediction Flow

```
User Input (Criteria)
    ↓
Load Model & Scaler (.pkl files)
    ↓
Batch Prediction (1,346 foods)
    ↓
Scale Features (StandardScaler)
    ↓
Model.predict() + predict_proba()
    ↓
Get Label & Confidence
    ↓
Filter by Criteria
    ↓
Sort by Quality & Protein
    ↓
Display Results (20 per page)
```

## 📝 Development Notes

### Caching Strategy
- `@st.cache_resource`: Used for ML models & scalers (loaded once)
- `@st.cache_data`: Used for CSV data (reloaded when file changes)

### Session State Variables
- `max_calories`, `min_protein`, `min_quality`: Diet criteria
- `show_recommendations`: Toggle recommendations display
- `search_query`: Current search filter

### File Paths
System uses **relative paths** to find models & data:
```python
PROJECT_ROOT = Path(__file__).parent.parent.parent / "websait"
```
This assumes structure: `Project/websait/` (PHP) and `Project/streamlait/` (Streamlit)

## 🐛 Troubleshooting

### Model files not found
```
Error loading model: [Errno 2] No such file or directory: '...model.pkl'
```
**Solution**: Train models menggunakan Admin Panel atau pastikan file `.pkl` ada di folder `websait/`

### Data file not found
```
Error loading data: [Errno 2] No such file or directory: 'nutrition_data.csv'
```
**Solution**: Pastikan `nutrition_data.csv` ada di folder `websait/` (parent directory)

### Slow predictions
**Issue**: Predicting 1,346 foods takes 5-10 seconds
**Solutions**:
- Use Random Forest (fastest with high accuracy)
- Reduce dataset size for testing
- Implement pagination (already limited to 20 results)

### Warning: X does not have valid feature names
**Issue**: Sklearn warning about feature names
**Impact**: Non-blocking warning, predictions still work correctly
**Solution**: Can ignore or upgrade sklearn

## 🚀 Deployment

### Local Development
```bash
streamlit run app.py
```

### Streamlit Cloud
1. Push to GitHub repository
2. Connect to Streamlit Cloud
3. Deploy with `app.py` as main file
4. Add `requirements.txt` dependencies
5. Ensure model files are included or trained on first run

## 📞 Support

Untuk pertanyaan atau issue:
- Check `README.md` di folder `websait/` untuk context PHP version
- Review Jupyter Notebook di `ilham.ipynb` untuk model training details

## 📜 License

Project ini dibuat untuk keperluan akademis - DataScience Semester 5

---

**Built with ❤️ using Streamlit | Converted from PHP version | Real-time ML Predictions**
