import streamlit as st

def home():
    """
        Penjelasan singkat mengenai latar belakang masalah dari proyek ini.
        Apa Saja Model yang digunakan dalam proyek ini.
    """
    st.markdown("""<h1 style='font-size: 34px; font-weight: bold;'>Pengelompokan Makanan Khas Indonesia Berbasis Analisis
            Fakta Makronutrien Terkandung Menggunakan Pendekatan
            Sains Data</h1>
            """, unsafe_allow_html=True)
    
    st.html("""Anggota Kelompok:<br>
            1. <br>
            2. <br>
            3. <br>
            4. 
            """)
    
    st.html("""
        <h2>Latar Belakang Masalah </h2>
        Indonesia adalah negara yang kaya akan budaya. Salah satu aspek 
        kebudayaan yang paling menonjol adalah makanan khas Indonesia. Terdapat 
        banyak sekali makanan yang berbeda dari tiap budaya di Indonesia, baik itu 
        makanan yang diadaptasi dari budaya luar, maupun makanan yang dihasilkan 
        dari kekayaan Indonesia itu sendiri. Sayangnya, makanan-makanan ini bisa 
        dikatakan tidak semuanya mencukupi kebutuhan gizi masyarakat. Oleh karena 
        itu, kami berinisiatif untuk membuat program memilah makanan berdasarkan 
        kandungan makronutriennya.
    """)
    
    if st.button("Bug test"):
        st.write("tabs_settings:", st.session_state['tabs_settings'])