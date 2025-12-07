# 🚀 Quick Start Guide - Streamlit Food Recommendation System

## ⚡ Cara Cepat Menjalankan

### 1. Buka Terminal PowerShell
```powershell
cd "d:\Semester 5\DataScience\Project\streamlait"
```

### 2. Install Dependencies (Hanya Sekali)
```powershell
pip install -r requirements.txt
```

### 3. Jalankan Aplikasi
```powershell
streamlit run app.py
```

### 4. Buka Browser
Aplikasi otomatis terbuka di: **http://localhost:8501**

---

## 📋 Checklist Sebelum Menjalankan

Pastikan file-file ini ada di folder `websait/` (folder parent):

### File Data (Required)
- [ ] `nutrition_data.csv` - Dataset 1,346 makanan

### File Model (Required untuk User Recommendation)
- [ ] `random_forest_model.pkl` & `random_forest_scaler.pkl`
- [ ] `naive_bayes_model.pkl` & `naive_bayes_scaler.pkl`
- [ ] `svm_model.pkl` & `svm_scaler.pkl`
- [ ] `kmeans_model.pkl` & `kmeans_scaler.pkl`

> **Catatan**: Jika model belum ada, train model dulu via Admin Panel atau Jupyter Notebook original

---

## 🎯 Panduan Penggunaan Cepat

### Untuk Mendapatkan Rekomendasi Makanan

1. **Pilih "Dapatkan Rekomendasi"** di halaman utama
2. **Pilih Model**: Random Forest (recommended - 92.59% akurasi)
3. **Pilih Preset Diet**:
   - 🏃 Turun Berat: Max 200 kcal, Min 15g protein
   - 💪 Nambah Otot: Max 400 kcal, Min 25g protein
   - 🥗 Sehat Seimbang: Max 300 kcal, Min 10g protein
   - 🔥 Rendah Kalori: Max 150 kcal, Min 5g protein
4. **Klik "Dapatkan Rekomendasi"**
5. Tunggu 3-5 detik untuk prediksi real-time
6. Browse hasil dan klik "Lihat Detail Lengkap" untuk info lengkap

### Untuk Kelola Data & Model (Admin)

1. **Pilih "Administrator"** di halaman utama
2. **Tab Data Preprocessing**:
   - Lihat stats & preview data
   - Clean data: centang opsi → klik "Bersihkan Data"
   - Transform: pilih metode → klik "Transformasi Data"
3. **Tab Model Configuration**:
   - Pilih model type
   - Atur test size (20% recommended)
   - Klik "Train Model"
   - Lihat metrics & confusion matrix
4. **Tab Data Visualization**:
   - Scroll untuk lihat berbagai grafik
   - Histogram distribusi nutrisi
   - Scatter plots & correlation heatmap

---

## 🆘 Troubleshooting Cepat

### Error: "No module named 'streamlit'"
```powershell
pip install streamlit
```

### Error: "nutrition_data.csv not found"
Pastikan file ada di: `d:\Semester 5\DataScience\Project\websait\nutrition_data.csv`

### Error: "Model files not found"
**Opsi 1**: Copy file `.pkl` dari folder PHP original
**Opsi 2**: Train model baru via Admin Panel → Model Configuration

### Prediksi Lambat (>10 detik)
- Normal untuk 1,346 makanan pertama kali
- Model akan di-cache untuk request berikutnya (lebih cepat)
- Gunakan Random Forest untuk performa terbaik

### Port 8501 Already in Use
```powershell
# Stop proses Streamlit yang masih running
Get-Process -Name streamlit -ErrorAction SilentlyContinue | Stop-Process -Force

# Atau gunakan port lain
streamlit run app.py --server.port 8502
```

---

## 🔄 Update Aplikasi

Jika ada perubahan di code:
1. **Stop server**: Ctrl+C di terminal
2. **Restart**: `streamlit run app.py`

Streamlit auto-reload saat file berubah (klik "Rerun" di browser)

---

## 📊 Perbandingan dengan PHP Version

| Fitur | PHP Version | Streamlit Version | Status |
|-------|-------------|-------------------|---------|
| Landing Page | ✅ index.php | ✅ app.py | ✅ Identik |
| User Interface | ✅ user.php | ✅ User_Recommendation.py | ✅ Identik |
| Admin Panel | ✅ admin.php | ✅ Admin_Panel.py | ✅ Identik |
| Real-time ML | ✅ predict_batch.py | ✅ predictor.py | ✅ Identik |
| Data Cleaning | ✅ admin_operations.py | ✅ data_operations.py | ✅ Identik |
| Color Theme | ✅ Green health | ✅ Green health | ✅ Identik |
| 4 ML Models | ✅ RF, NB, SVM, KM | ✅ RF, NB, SVM, KM | ✅ Identik |
| Diet Presets | ✅ 4 presets | ✅ 4 presets | ✅ Identik |
| Confidence Scores | ✅ AI % yakin | ✅ AI % yakin | ✅ Identik |

---

## 🎓 Tips & Best Practices

### Untuk Pengguna
- Gunakan **Random Forest** untuk akurasi terbaik (92.59%)
- **Preset Diet Goals** lebih cepat daripada manual filter
- **Search box** berguna untuk cari makanan spesifik
- Badge warna menunjukkan kualitas: 🟢 Sangat Baik > 🟢 Baik > 🟠 Buruk > 🔴 Sangat Buruk

### Untuk Admin
- **Clean data** dulu sebelum train model
- Gunakan **test size 20%** untuk balance training/testing
- **Save cleaned data** sebelum transform untuk backup
- Train semua 4 model untuk perbandingan performa

---

## 📞 Bantuan Lebih Lanjut

- **README.md**: Dokumentasi lengkap
- **PHP Version**: Lihat folder `websait/` untuk reference
- **Jupyter Notebook**: `ilham.ipynb` untuk training details

---

**Ready to go! 🚀 Selamat menggunakan Streamlit Food Recommendation System!**
