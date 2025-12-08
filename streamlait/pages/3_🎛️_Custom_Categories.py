import streamlit as st
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Custom Categories", page_icon="🎛️", layout="wide")

st.title("🎛️ Custom Category Builder")
st.markdown("Gunakan **Unsupervised Learning (K-Means)** untuk membuat kategori kualitas sendiri!")

# Load data
@st.cache_data
def load_data():
    from pathlib import Path
    # Sesuaikan path ke nutrition.csv
    csv_path = "nutrition.csv"  # ← GANTI INI
    
    try:
        df = pd.read_csv(csv_path, encoding='utf-8-sig')
        st.sidebar.success(f"✅ Data loaded: {len(df)} makanan")
        return df
    except FileNotFoundError:
        st.error(f"❌ File tidak ditemukan: {csv_path}")
        st.stop()
    except Exception as e:
        st.error(f"❌ Error loading data: {str(e)}")
        st.stop()

df = load_data()

# Tampilkan info dataset
with st.sidebar.expander("📊 Info Dataset"):
    st.write(f"**Total makanan:** {len(df)}")
    st.write(f"**Kolom:** {', '.join(df.columns.tolist())}")
    st.write("**Range nilai:**")
    st.write(f"- Kalori: {df['calories'].min():.1f} - {df['calories'].max():.1f}")
    st.write(f"- Protein: {df['proteins'].min():.1f} - {df['proteins'].max():.1f}g")
    st.write(f"- Lemak: {df['fat'].min():.1f} - {df['fat'].max():.1f}g")
    st.write(f"- Karbo: {df['carbohydrate'].min():.1f} - {df['carbohydrate'].max():.1f}g")

# Sidebar untuk pilih fitur
st.sidebar.markdown("### 📊 Pilih Fitur untuk Clustering")
use_calories = st.sidebar.checkbox("Kalori", value=True)
use_protein = st.sidebar.checkbox("Protein", value=True)
use_fat = st.sidebar.checkbox("Lemak", value=False)
use_carbs = st.sidebar.checkbox("Karbohidrat", value=False)

# Prepare features
features = []
feature_names = []
if use_calories:
    features.append(df['calories'].values)
    feature_names.append('calories')
if use_protein:
    features.append(df['proteins'].values)
    feature_names.append('proteins')
if use_fat:
    features.append(df['fat'].values)
    feature_names.append('fat')
if use_carbs:
    features.append(df['carbohydrate'].values)
    feature_names.append('carbohydrate')

if len(features) < 2:
    st.warning("⚠️ Pilih minimal 2 fitur untuk clustering!")
    st.stop()

X = np.column_stack(features)

# Standardize features untuk clustering yang lebih baik
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Clustering
st.markdown("### 🎯 Atur Jumlah Cluster")

col_cluster1, col_cluster2 = st.columns([3, 1])
with col_cluster1:
    n_clusters = st.slider("Jumlah Kategori:", 2, 6, 4)
with col_cluster2:
    st.metric("Total Data", f"{len(df):,}")

# Elbow method untuk rekomendasi jumlah cluster
with st.expander("📉 Lihat Elbow Method (Rekomendasi Jumlah Cluster)"):
    inertias = []
    K_range = range(2, 11)
    
    for k in K_range:
        kmeans_temp = KMeans(n_clusters=k, random_state=42, n_init=10)
        kmeans_temp.fit(X_scaled)
        inertias.append(kmeans_temp.inertia_)
    
    fig_elbow, ax_elbow = plt.subplots(figsize=(10, 4))
    ax_elbow.plot(K_range, inertias, 'bo-', linewidth=2, markersize=8)
    ax_elbow.axvline(x=n_clusters, color='red', linestyle='--', 
                     label=f'Pilihan saat ini (K={n_clusters})')
    ax_elbow.set_xlabel('Jumlah Cluster (K)', fontsize=12)
    ax_elbow.set_ylabel('Inertia', fontsize=12)
    ax_elbow.set_title('Elbow Method - Mencari Jumlah Cluster Optimal', 
                       fontsize=14, fontweight='bold')
    ax_elbow.grid(True, alpha=0.3)
    ax_elbow.legend()
    st.pyplot(fig_elbow)
    plt.close()
    
    st.info("💡 **Tip:** Pilih jumlah cluster di 'siku' kurva (elbow point)")

# Jalankan K-Means
with st.spinner(f"🔄 Menjalankan K-Means dengan {n_clusters} cluster..."):
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    clusters = kmeans.fit_predict(X_scaled)

st.success(f"✅ Clustering selesai! {n_clusters} kategori berhasil dibuat.")

# Visualisasi
st.markdown("### 📈 Visualisasi Clustering")

col1, col2 = st.columns(2)

with col1:
    # 2D Scatter dengan Matplotlib
    fig, ax = plt.subplots(figsize=(10, 6))
    scatter = ax.scatter(X[:, 0], X[:, 1], c=clusters, cmap='viridis', 
                        s=50, alpha=0.6, edgecolors='black', linewidth=0.5)
    ax.set_xlabel(feature_names[0].title(), fontsize=12)
    ax.set_ylabel(feature_names[1].title(), fontsize=12)
    ax.set_title('Hasil Clustering K-Means', fontsize=14, fontweight='bold')
    plt.colorbar(scatter, ax=ax, label='Cluster')
    
    # Add centroids
    centroids_original = scaler.inverse_transform(kmeans.cluster_centers_)
    ax.scatter(centroids_original[:, 0], centroids_original[:, 1], 
              c='red', marker='X', s=200, edgecolors='black', linewidth=2,
              label='Centroids')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    st.pyplot(fig)
    plt.close()

with col2:
    # Cluster stats
    df_temp = df.copy()
    df_temp['cluster'] = clusters
    
    st.markdown("**📊 Statistik per Cluster:**")
    for i in range(n_clusters):
        cluster_data = df_temp[df_temp['cluster'] == i]
        with st.expander(f"Cluster {i} ({len(cluster_data)} makanan)", expanded=i<2):
            col_a, col_b, col_c, col_d = st.columns(4)
            with col_a:
                st.metric("Avg Kalori", f"{cluster_data['calories'].mean():.1f}")
            with col_b:
                st.metric("Avg Protein", f"{cluster_data['proteins'].mean():.1f}g")
            with col_c:
                st.metric("Avg Lemak", f"{cluster_data['fat'].mean():.1f}g")
            with col_d:
                st.metric("Avg Karbo", f"{cluster_data['carbohydrate'].mean():.1f}g")
            
            # Tampilkan 5 contoh makanan
            st.markdown("**Contoh makanan:**")
            for idx, (_, food) in enumerate(cluster_data.head(5).iterrows(), 1):
                st.text(f"{idx}. {food['name']} ({food['calories']:.0f} kcal, {food['proteins']:.1f}g protein)")

# Distribution plot
st.markdown("### 📊 Distribusi Cluster")
fig2, ax2 = plt.subplots(figsize=(10, 4))
cluster_counts = pd.Series(clusters).value_counts().sort_index()
bars = ax2.bar(cluster_counts.index, cluster_counts.values, 
               color=plt.cm.viridis(np.linspace(0, 1, n_clusters)))
ax2.set_xlabel('Cluster', fontsize=12)
ax2.set_ylabel('Jumlah Makanan', fontsize=12)
ax2.set_title('Jumlah Makanan per Cluster', fontsize=14, fontweight='bold')
ax2.grid(axis='y', alpha=0.3)

# Add value labels on bars
for bar in bars:
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height,
            f'{int(height)}',
            ha='center', va='bottom', fontweight='bold')

st.pyplot(fig2)
plt.close()

# Assign labels
st.markdown("---")
st.markdown("### 🏷️ Beri Label pada Setiap Cluster")
st.info("💡 **Panduan:** Analisis rata-rata nutrisi setiap cluster, lalu tentukan kategori yang sesuai.")

col_labels = st.columns(min(n_clusters, 4))
cluster_labels = {}

for i in range(n_clusters):
    col_idx = i % 4
    with col_labels[col_idx]:
        cluster_data = df_temp[df_temp['cluster'] == i]
        avg_cal = cluster_data['calories'].mean()
        avg_prot = cluster_data['proteins'].mean()
        avg_fat = cluster_data['fat'].mean()
        avg_carb = cluster_data['carbohydrate'].mean()
        
        st.markdown(f"**Cluster {i}**")
        st.caption(f"📊 {len(cluster_data)} makanan")
        st.caption(f"🔥 {avg_cal:.0f} kcal | 💪 {avg_prot:.1f}g")
        st.caption(f"🥑 {avg_fat:.1f}g fat | 🍚 {avg_carb:.1f}g carb")
        
        # Auto-suggest berdasarkan kalori & protein
        if avg_cal < 200 and avg_prot > 15:
            suggested_idx = 0  # Sangat Baik
        elif avg_cal < 350 and avg_prot > 10:
            suggested_idx = 1  # Baik
        elif avg_cal < 500:
            suggested_idx = 2  # Buruk
        else:
            suggested_idx = 3  # Sangat Buruk
        
        cluster_labels[i] = st.selectbox(
            "Label:",
            ['Sangat Baik', 'Baik', 'Buruk', 'Sangat Buruk'],
            index=suggested_idx,
            key=f"label_{i}",
            label_visibility="collapsed"
        )

# ============== BAGIAN BARU: HISTOGRAM & PIE CHART ==============
st.markdown("---")
st.markdown("### 📊 Analisis Distribusi per Kategori")

# Tambahkan kategori ke dataframe
df_temp['kategori_custom'] = df_temp['cluster'].map(cluster_labels)

# PERBAIKAN: Hanya tampilkan nutrisi yang DIPILIH saat clustering
available_nutrients = []
nutrient_display = {}

if use_calories:
    available_nutrients.append('calories')
    nutrient_display['calories'] = '🔥 Kalori'
if use_protein:
    available_nutrients.append('proteins')
    nutrient_display['proteins'] = '💪 Protein'
if use_fat:
    available_nutrients.append('fat')
    nutrient_display['fat'] = '🥑 Lemak'
if use_carbs:
    available_nutrients.append('carbohydrate')
    nutrient_display['carbohydrate'] = '🍚 Karbohidrat'

# Pilihan nutrisi untuk histogram
st.info(f"💡 Fitur yang digunakan clustering: **{', '.join([nutrient_display[n] for n in available_nutrients])}**")

col_viz1, col_viz2 = st.columns([1, 3])

with col_viz1:
    nutrisi_pilihan = st.selectbox(
        "Pilih nutrisi untuk histogram:",
        options=available_nutrients,
        format_func=lambda x: nutrient_display[x],
        key='nutrisi_histogram'
    )

with col_viz2:
    st.markdown(f"Melihat distribusi **{nutrient_display[nutrisi_pilihan]}** di setiap kategori untuk memahami pola nutrisi")

# Buat tabs untuk histogram dan pie chart
tab1, tab2 = st.tabs(["📊 Histogram Distribusi", "🥧 Pie Chart Komposisi"])

with tab1:
    st.markdown(f"#### Distribusi {nutrient_display[nutrisi_pilihan]} per Kategori")
    
    # Hitung jumlah kategori unik
    unique_categories = sorted(df_temp['kategori_custom'].unique())
    n_categories = len(unique_categories)
    
    # Tentukan layout grid yang lebih baik
    if n_categories <= 2:
        n_cols = n_categories
        n_rows = 1
    elif n_categories <= 4:
        n_cols = 2
        n_rows = 2
    else:
        n_cols = 3
        n_rows = 2
    
    # Buat subplots dengan ukuran yang proporsional
    fig_hist, axes = plt.subplots(n_rows, n_cols, figsize=(6*n_cols, 4.5*n_rows))
    
    # Flatten axes untuk memudahkan iterasi
    if n_categories == 1:
        axes = [axes]
    else:
        axes = axes.flatten() if n_categories > 1 else [axes]
    
    # Color map untuk konsistensi
    colors = plt.cm.viridis(np.linspace(0, 1, n_categories))
    
    for idx, kategori in enumerate(unique_categories):
        data_kategori = df_temp[df_temp['kategori_custom'] == kategori][nutrisi_pilihan]
        
        axes[idx].hist(data_kategori, bins=20, color=colors[idx], 
                      alpha=0.7, edgecolor='black', linewidth=0.8)
        
        # Garis statistik
        mean_val = data_kategori.mean()
        median_val = data_kategori.median()
        
        axes[idx].axvline(mean_val, color='red', 
                         linestyle='--', linewidth=2.5, label=f'Mean: {mean_val:.1f}')
        axes[idx].axvline(median_val, color='orange', 
                         linestyle='--', linewidth=2.5, label=f'Median: {median_val:.1f}')
        
        axes[idx].set_title(f'{kategori}\n({len(data_kategori)} makanan)', 
                           fontweight='bold', fontsize=12)
        axes[idx].set_xlabel(nutrient_display[nutrisi_pilihan], fontsize=11)
        axes[idx].set_ylabel('Frekuensi', fontsize=11)
        axes[idx].legend(fontsize=9, loc='upper right')
        axes[idx].grid(True, alpha=0.3, linestyle='--')
    
    # Sembunyikan axes yang tidak terpakai
    for idx in range(n_categories, len(axes)):
        axes[idx].set_visible(False)
    
    plt.tight_layout()
    st.pyplot(fig_hist)
    plt.close()
    
    # Statistik deskriptif dalam format yang lebih compact
    st.markdown("**📈 Statistik Deskriptif:**")
    stats_df = df_temp.groupby('kategori_custom')[nutrisi_pilihan].describe()[['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max']].round(2)
    stats_df.columns = ['Jumlah', 'Rata-rata', 'Std Dev', 'Min', 'Q1', 'Median', 'Q3', 'Max']
    st.dataframe(stats_df, use_container_width=True)

with tab2:
    st.markdown("#### Komposisi Rata-Rata Nutrisi per Kategori")
    
    col_pie1, col_pie2 = st.columns([1, 1])
    
    with col_pie1:
        # Pilih kategori untuk pie chart
        kategori_terpilih = st.selectbox(
            "Pilih kategori:",
            options=unique_categories,
            key='kategori_piechart'
        )
    
    with col_pie2:
        show_percentages = st.checkbox("Tampilkan persentase", value=True)
    
    # Data untuk pie chart
    data_kategori = df_temp[df_temp['kategori_custom'] == kategori_terpilih]
    
    # Layout yang lebih baik dengan 2 kolom
    col_pie_viz1, col_pie_viz2 = st.columns(2)
    
    with col_pie_viz1:
        # Pie chart 1: Komposisi Makronutrien
        st.markdown(f"**Komposisi Makronutrien**")
        st.caption(f"Kategori: {kategori_terpilih}")
        
        avg_protein = data_kategori['proteins'].mean()
        avg_fat = data_kategori['fat'].mean()
        avg_carb = data_kategori['carbohydrate'].mean()
        
        fig_pie1, ax_pie1 = plt.subplots(figsize=(7, 7))
        
        labels = ['Protein', 'Lemak', 'Karbohidrat']
        sizes = [avg_protein, avg_fat, avg_carb]
        colors_pie = ['#FF6B6B', '#4ECDC4', '#FFE66D']
        explode = (0.08, 0.08, 0.08)
        
        if show_percentages:
            autopct = '%1.1f%%'
        else:
            autopct = lambda pct: f'{pct * sum(sizes) / 100:.1f}g'
        
        wedges, texts, autotexts = ax_pie1.pie(sizes, labels=labels, colors=colors_pie,
                                                autopct=autopct, startangle=90,
                                                explode=explode, shadow=True,
                                                textprops={'fontsize': 11, 'fontweight': 'bold'})
        
        # Styling
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(11)
        
        ax_pie1.set_title(f'Rata-rata per 100g\n({len(data_kategori)} makanan)',
                         fontsize=13, fontweight='bold', pad=20)
        
        st.pyplot(fig_pie1)
        plt.close()
        
        # Info tambahan dengan metrics
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            st.metric("Kalori Rata-rata", f"{data_kategori['calories'].mean():.1f} kcal")
        with col_m2:
            st.metric("Total Makanan", f"{len(data_kategori)}")
    
    with col_pie_viz2:
        # Pie chart 2: Distribusi Makanan per Kategori
        st.markdown("**Distribusi Semua Kategori**")
        st.caption(f"Total: {len(df_temp)} makanan")
        
        category_counts = df_temp['kategori_custom'].value_counts()
        
        fig_pie2, ax_pie2 = plt.subplots(figsize=(7, 7))
        
        colors_pie2 = plt.cm.viridis(np.linspace(0, 1, len(category_counts)))
        
        # Calculate percentages for labels
        def make_autopct(values):
            def my_autopct(pct):
                total = sum(values)
                val = int(round(pct*total/100.0))
                return f'{pct:.1f}%\n({val} makanan)'
            return my_autopct
        
        wedges2, texts2, autotexts2 = ax_pie2.pie(category_counts.values, 
                                                    labels=category_counts.index,
                                                    colors=colors_pie2,
                                                    autopct=make_autopct(category_counts.values),
                                                    startangle=90,
                                                    shadow=True,
                                                    textprops={'fontsize': 10})
        
        # Highlight kategori terpilih
        for i, label in enumerate(category_counts.index):
            if label == kategori_terpilih:
                wedges2[i].set_edgecolor('red')
                wedges2[i].set_linewidth(4)
                texts2[i].set_fontweight('bold')
                texts2[i].set_fontsize(11)
        
        for autotext in autotexts2:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(9)
        
        ax_pie2.set_title(f'Perbandingan Kategori',
                         fontsize=13, fontweight='bold', pad=20)
        
        st.pyplot(fig_pie2)
        plt.close()
        
        # Persentase dalam bentuk metrics
        pct = (len(data_kategori) / len(df_temp)) * 100
        col_m3, col_m4 = st.columns(2)
        with col_m3:
            st.metric("Persentase", f"{pct:.1f}%")
        with col_m4:
            st.metric("Ranking", f"#{category_counts.index.tolist().index(kategori_terpilih) + 1}")

# ============== AKHIR BAGIAN BARU ==============

# Save configuration
st.markdown("---")
col_save1, col_save2, col_save3 = st.columns([2, 2, 1])

with col_save1:
    st.info("💡 **Tip:** Kalori rendah + Protein tinggi = 'Sangat Baik'")

with col_save2:
    config_name = st.text_input("Nama konfigurasi:", value="Default Custom", 
                                placeholder="e.g., Diet Ketat")

with col_save3:
    if st.button("💾 Simpan", use_container_width=True, type="primary"):
        st.session_state.custom_kmeans_model = kmeans
        st.session_state.custom_kmeans_scaler = scaler
        st.session_state.custom_cluster_labels = cluster_labels
        st.session_state.custom_feature_names = feature_names
        st.session_state.use_custom_categories = True
        st.session_state.custom_config_name = config_name
        st.success(f"✅ '{config_name}' tersimpan!")
        st.balloons()
        
        # Redirect hint
        st.info("👉 Kembali ke halaman **User Recommendations** untuk menggunakan kategori custom ini!")

# Preview hasil
if st.checkbox("🔍 Preview Hasil Kategorisasi (20 makanan pertama)"):
    st.markdown("### 📋 Preview Kategorisasi")
    
    df_preview = df.copy()
    df_preview['cluster'] = clusters
    df_preview['kategori_custom'] = df_preview['cluster'].map(cluster_labels)
    
    preview_df = df_preview[['name', 'calories', 'proteins', 'fat', 'carbohydrate', 'kategori_custom']].head(20)
    
    st.dataframe(
        preview_df,
        column_config={
            "name": "Nama Makanan",
            "calories": st.column_config.NumberColumn("Kalori", format="%.1f kcal"),
            "proteins": st.column_config.NumberColumn("Protein", format="%.1f g"),
            "fat": st.column_config.NumberColumn("Lemak", format="%.1f g"),
            "carbohydrate": st.column_config.NumberColumn("Karbo", format="%.1f g"),
            "kategori_custom": st.column_config.TextColumn(
                "Kategori",
                help="Kategori berdasarkan K-Means clustering"
            )
        },
        hide_index=True,
        use_container_width=True
    )
    
    # Summary by category
    st.markdown("**📊 Ringkasan per Kategori:**")
    category_summary = df_preview.groupby('kategori_custom').agg({
        'name': 'count',
        'calories': 'mean',
        'proteins': 'mean'
    }).round(1)
    category_summary.columns = ['Jumlah', 'Avg Kalori', 'Avg Protein']
    st.dataframe(category_summary, use_container_width=True)