"""
Main Streamlit Application - Sistem Rekomendasi Makanan Sehat
Entry point with role selection (User/Admin)
"""

import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Sistem Rekomendasi Makanan Sehat",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS to match the green theme
st.markdown("""
<style>
    /* Main theme colors - green health-focused */
    .main {
        background: linear-gradient(135deg, #2E7D32 0%, #66BB6A 50%, #A5D6A7 100%);
    }
    
    /* Title styling */
    .title-header {
        text-align: center;
        color: white;
        padding: 2rem;
        background: linear-gradient(135deg, #1B5E20 0%, #2E7D32 100%);
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    
    /* Role card styling */
    .role-card {
        background: white;
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        box-shadow: 0 15px 40px rgba(0,0,0,0.3);
        margin: 1rem;
        transition: all 0.4s ease;
    }
    
    .role-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 25px 60px rgba(0,0,0,0.4);
    }
    
    /* Button styling */
    .stButton>button {
        background: linear-gradient(135deg, #2E7D32 0%, #388E3C 100%);
        color: white;
        font-weight: 600;
        border-radius: 50px;
        padding: 0.75rem 3rem;
        border: none;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #1B5E20 0%, #2E7D32 100%);
        box-shadow: 0 8px 20px rgba(46, 125, 50, 0.4);
    }
    
    /* Hide streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

def main():
    """Main application entry point"""
    
    # Header
    st.markdown("""
    <div class="title-header">
        <h1>🥗 Sistem Rekomendasi Makanan Sehat</h1>
        <p style="font-size: 1.3em; opacity: 0.95;">
            Platform Cerdas untuk Analisis Nutrisi & Rekomendasi Makanan Berkualitas
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Role selection
    st.markdown("### Pilih Peran Anda")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="role-card">
            <div style="font-size: 5em;">🥗</div>
            <h2 style="color: #2E7D32;">Dapatkan Rekomendasi</h2>
            <p style="color: #666; font-size: 1.1em;">
                Sistem AI akan merekomendasikan makanan terbaik untuk Anda
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        **Fitur Pengguna:**
        - ✓ Rekomendasi personal berdasarkan target kalori
        - ✓ Filter berdasarkan protein & kualitas nutrisi
        - ✓ Analisis dengan Random Forest ML model
        - ✓ Lihat detail lengkap setiap makanan
        """)
        
        if st.button("🎯 Dapatkan Rekomendasi", key="user_btn", use_container_width=True):
            st.switch_page("pages/1_👤_User_Recommendation.py")
    
    with col2:
        st.markdown("""
        <div class="role-card">
            <div style="font-size: 5em;">⚙️</div>
            <h2 style="color: #2E7D32;">Administrator</h2>
            <p style="color: #666; font-size: 1.1em;">
                Kelola data, preprocessing, dan model machine learning
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        **Fitur Admin:**
        - ✓ Data preprocessing & cleaning
        - ✓ Konfigurasi model ML
        - ✓ Visualisasi data & hasil
        - ✓ Perbandingan performa model
        """)
        
        if st.button("⚙️ Masuk sebagai Admin", key="admin_btn", use_container_width=True):
            st.switch_page("pages/2_⚙️_Admin_Panel.py")
    
    # Information section
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 2rem; background: white; border-radius: 15px;">
        <h3 style="color: #2E7D32;">Tentang Sistem</h3>
        <p style="color: #666;">
            Sistem ini menggunakan machine learning untuk memberikan rekomendasi makanan 
            berdasarkan nilai nutrisi. Model dilatih dengan 4 algoritma berbeda 
            (Random Forest, Naive Bayes, SVM, K-Means) untuk memberikan prediksi 
            kualitas makanan secara real-time.
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
