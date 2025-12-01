import streamlit as st
import src.ui.home as uihome

# Page configuration
st.set_page_config(
    page_title="My Streamlit App",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Hide sidebar collapse button
st.markdown(
    """
    <style>
        [data-testid="collapsedControl"] {
            display: none
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Title and description
st.markdown("""<h1 style='font-size: 34px; font-weight: bold;'>Pengelompokan Makanan Khas Indonesia Berbasis Analisis<br>
            Fakta Makronutrien Terkandung Menggunakan Pendekatan<br>
            Sains Data</h1>
            """, unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("Navigasi")
    page = st.radio(
        "Pilih halaman:",
        ["Home", "Data Analysis", "Visualization", "Settings"]
    )
    
    st.toast("Gunakan menu di samping untuk navigasi antar halaman.", icon="ℹ️")
        
    
    st.divider()
    
    st.header("Filters")
    filter_option = st.selectbox(
        "Choose an option:",
        ["Option 1", "Option 2", "Option 3"]
    )

# Main content area
if page == "Home":
    uihome.home()
    pass

elif page == "Data Analysis":
    st.header("Data Analysis")
    st.write("Upload and analyze your data here.")
    
    uploaded_file = st.file_uploader("Choose a file", type=["csv", "xlsx", "txt"])
    
    if uploaded_file is not None:
        st.success("File uploaded successfully!")
        # Add your data processing logic here

elif page == "Visualization":
    st.header("Data Visualization")
    st.write("Create visualizations here.")
    
    # Example: Simple chart placeholder
    import pandas as pd
    import numpy as np
    
    chart_data = pd.DataFrame(
        np.random.randn(20, 3),
        columns=['A', 'B', 'C']
    )
    
    st.line_chart(chart_data)

elif page == "Settings":
    st.header("Settings")
    st.write("Configure your application settings.")
    
    theme = st.selectbox("Select theme:", ["Light", "Dark"])
    notifications = st.checkbox("Enable notifications")
    
    if st.button("Save Settings"):
        st.success("Settings saved successfully!")

# Footer
st.divider()
st.caption("Built with Streamlit | © 2025")
