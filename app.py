import streamlit as st
import src.ui.home as uihome
import src.ui.data_preprocessing_modeling as uipreprocessmodeling
import pandas as pd
import numpy as np


#Session state initialization
def initialize_session_state(): 
    if 'data_preview' not in st.session_state:
        df = pd.read_csv('data/nutrition.csv')
        st.session_state['data_preview'] = df
        
    if 'slider_num_models' not in st.session_state:
        st.session_state['slider_num_models'] = 5
        
    if 'tabs_settings' not in st.session_state:
        st.session_state['tabs_settings'] = {}
    if "page" not in st.session_state:
        st.session_state.page = "Home" # Default page

# Radio Sync
def _update_from_primary():
    st.session_state.page = st.session_state.nav_primary
    st.session_state.nav_secondary = None

def _update_from_secondary():
    st.session_state.page = st.session_state.nav_secondary
    st.session_state.nav_primary = None

# Initialize session state
initialize_session_state()



# Page configuration
st.set_page_config(
    page_title="Project Akhir Data Science",
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

# Sidebar
with st.sidebar:
    st.header("Navigasi")
    primary_pages = ["Home", "Our Result"]
    secondary_pages = [
        "Data Preprocessing & Modeling",
        "Result & Visualization",
        "Settings",
    ]

    # --- PRIMARY RADIO ---
    st.radio(
        "Main Pages",
        options=primary_pages,
        key="nav_primary",
        index=0 if st.session_state.page in primary_pages else None, # Select if active, else None
        on_change=_update_from_primary
    )

    st.divider()

    # --- SECONDARY RADIO ---
    st.radio(
        "Custom Data & Tools",
        options=secondary_pages,
        key="nav_secondary",
        index=0 if st.session_state.page in secondary_pages else None, # Select if active, else None
        on_change=_update_from_secondary
    )

    page = st.session_state.page
    st.toast("Gunakan menu di samping untuk navigasi antar halaman.", icon="ℹ️")
    st.divider()

# Main content area
if page == "Home":
    uihome.home()
    pass

elif page == "Our Result":
    import src.ui.our_results as uiourresults
    uiourresults.our_results()

elif page == "Data Preprocessing & Modeling":
    uipreprocessmodeling.data_preprocessing_modeling()
    pass

elif page == "Result & Visualization":
    st.header("Data Result & Visualization")
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