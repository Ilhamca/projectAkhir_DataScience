import streamlit as st
import pandas as pd
import numpy as np
import bokeh.models.widgets as bkwidgets
import streamlit_bokeh as stb
import src.ml.preprocess_modeling as preprocess_modeling


TAB_STATE_DEFAULTS = {
    "remove_missing_values": False,
    "remove_duplicates": False,
    "handle_outliers": False,
    "outlier_method": "IQR Method",
    "normalize": False,
    "normalization_method": "Min-Max Scaling",
    "algorithm": "K-Means",
    "n_clusters": 3,
    "random_state": 42,
    "linkage_method": "ward",
    "eps": 0.5,
    "min_samples": 5,
    "n_components": 3,
    "covariance_type": "full",
}



def update_slider_num_models():
    """Update the number of models based on slider value"""
    st.session_state['slider_num_models'] = st.session_state['current_slider_num_models']

def initialize_tab_settings(index):
    """Ensure per-tab state dictionary exists"""
    if 'tabs_settings' not in st.session_state:
        st.session_state['tabs_settings'] = {}

    if index not in st.session_state['tabs_settings']:
        st.session_state['tabs_settings'][index] = TAB_STATE_DEFAULTS.copy()

# def update_tab_setting(index, field, value):
#     """Update a specific setting for a given tab"""
#     if 'tabs_settings' in st.session_state and index in st.session_state['tabs_settings']:
#         st.session_state['tabs_settings'][index][field] = value
#     else:
#         initialize_tab_settings(index)
#         st.session_state['tabs_settings'][index][field] = value

def sync_widget_state(widget_key: str, tab_state: dict, field: str):
    """Seed widget session_state with tab defaults when needed"""
    if widget_key not in st.session_state:
        st.session_state[widget_key] = tab_state[field]

def data_information(data_preview):
    """
    Shows data information such as missing values, data types, and descriptive statistics.
    """
    data_info = data_preview.isna().sum().to_frame(name='Missing Values')
    st.write(f"Missing values, data types, dan statistik deskriptif dari dataset: ")
    st.dataframe(data_info)
    st.write("Statistik Deskriptif:")
    st.dataframe(data_preview.describe())
    preprocess_modeling.check_skewness(data_preview)

def data_preprocessing_modeling():
    """
    Main function for Data Preprocessing & Modeling page.
    tab1: Dataset dari data/nutrition.csv
    tab2: Dataset sendiri yang diupload user
    """
    st.header("Data Preprocessing & Modeling")
    st.write("Preview dari dataset:")
    data_preview = st.session_state.get('data_preview', None)
    if data_preview is not None:
        st.dataframe(data=data_preview, width='stretch', hide_index=True)
    else:
        st.write("No data preview available.")    

    with st.expander("Informasi Data"):
        data_information(data_preview)
    
    st.divider()
    
    with st.container():
        """
            Setting halaman data preprocessing
            Berisi cek missing value, replacement, normalisasi, standarisasi, dll
            
        """        
        current_num_models = st.session_state.get('num_models', 5)
       
       
        st.slider(
            label="Select number of models to compare",
            min_value=2,
            max_value=10,
            value=st.session_state['slider_num_models'],
            key='current_slider_num_models',
            on_change=update_slider_num_models,
            step=1
        )

        st.write(f"Number of models to compare: {st.session_state['slider_num_models']}")
        
        """
        Sesuai dengan jumlah model yang dipilih, buat st.tab sebanyak itu
        Tabs akan memanggkil cleaning_modeling() untuk tiap tab dan menyimpan pengaturannya secara independen
        """
        # Initialize settings for all tabs that will be shown
        for i in range(st.session_state['slider_num_models']):
            initialize_tab_settings(i)
            
        tabs = st.tabs([f"Model {i+1}" for i in range(st.session_state['slider_num_models'])])
        tabs_settings = [0] * st.session_state['slider_num_models'] # Stores settings for each tab
        for i in range(st.session_state['slider_num_models']):
            with tabs[i]:
                tabs_settings[i] = cleaning_modeling(i)
             
        with st.expander("Current Tabs Settings"):        
            st.dataframe(tabs_settings)
        
        st.button("Mulai Proses Komparasi Model", on_click=lambda: st.write("Proses Komparasi Model Dimulai..."), type='primary')
    
    cleaning_modeling_debug()
    if st.button("Show Tabs Settings in Session State"):
        st.write("tabs_settings:", st.session_state['tabs_settings'])
        

def cleaning_modeling(index):
    tab_state = st.session_state['tabs_settings'][index]
    st.subheader(f"Configuration for Model {index + 1}")
    
    # Data Cleaning Section
    st.markdown("### Data Cleaning")
    
    col1, col2 = st.columns(2)
    
    with col1:
        sync_widget_state(f"remove_duplicates_checkbox_{index}", tab_state, "remove_duplicates")
        tab_state["remove_duplicates"] = st.checkbox(
            "Remove Duplicates",
            key=f"remove_duplicates_checkbox_{index}",
            value=tab_state["remove_duplicates"],
            help="Remove duplicate rows from the dataset",
        )
        
        sync_widget_state(f"remove_missing_values_checkbox_{index}", tab_state, "remove_missing_values")
        tab_state["remove_missing_values"] = st.checkbox(
            "Remove Missing Values",
            key=f"remove_missing_values_checkbox_{index}",
            value=tab_state["remove_missing_values"],
            help="Remove rows with missing values from the dataset",
        )

    with col2:
        sync_widget_state(f"handle_outliers_checkbox_{index}", tab_state, "handle_outliers")
        tab_state["handle_outliers"] = st.checkbox(
            "Handle Outliers",
            key=f"handle_outliers_checkbox_{index}",
            value=tab_state["handle_outliers"],
            help="Detect and handle outliers in the dataset",
        )

        handle_outliers_enabled = st.session_state.get(
            f"handle_outliers_checkbox_{index}",
            tab_state.get("handle_outliers", False),
        )

        sync_widget_state(f"outlier_method_selectbox_{index}", tab_state, "outlier_method")
        tab_state["outlier_method"] = st.selectbox(
            "Outlier Detection Method",
            ["IQR Method", "Z-Score Method", "Isolation Forest"],
            index=["IQR Method", "Z-Score Method", "Isolation Forest"].index(tab_state["outlier_method"]),
            key=f"outlier_method_selectbox_{index}",
            disabled=not handle_outliers_enabled,
            help="Choose method for detecting outliers",
        )
    
    st.divider()
    
    # Data Transformation Section
    st.markdown("### Data Transformation")
    
    sync_widget_state(f"normalize_checkbox_{index}", tab_state, "normalize")
    tab_state["normalize"] = st.checkbox(
        "Normalize/Standardize Data",
        key=f"normalize_checkbox_{index}",
        value=tab_state["normalize"],
        help="Apply normalization or standardization to numerical features",
    )


    sync_widget_state(f"normalization_selectbox_{index}", tab_state, "normalization_method")
    tab_state["normalization_method"] = st.selectbox(
        "Transformation Method",
        ["Min-Max Scaling", "Z-Score Standardization", "Robust Scaler"],
        index=["Min-Max Scaling", "Z-Score Standardization", "Robust Scaler"].index(tab_state["normalization_method"]),        
        key=f"normalization_selectbox_{index}",
        disabled=not tab_state.get("normalize", False),
        help="Choose transformation method for scaling features",
    )
    
    st.divider()
    
    # Modeling Section
    st.markdown("### Model Configuration")
    
    sync_widget_state(f"modeling_selectbox_{index}", tab_state, "algorithm")
    tab_state["algorithm"] = st.selectbox(
        "Choose Clustering Algorithm",
        ["K-Means", "Hierarchical Clustering", "DBSCAN", "Gaussian Mixture", "Naive Bayes", "Decision Tree"],
        key=f"modeling_selectbox_{index}",
        help="Select the clustering algorithm to use",
    )
    algorithm = tab_state["algorithm"]
    
    # Algorithm-specific parameters
    if algorithm == "K-Means":
        col1, col2 = st.columns(2)
        with col1:
            sync_widget_state(f"n_clusters_{index}", tab_state, "n_clusters")
            tab_state["n_clusters"] = st.number_input(
                "Number of Clusters (k)",
                min_value=2,
                max_value=20,
                key=f"n_clusters_{index}",
                help="Number of clusters to form",
            )
        with col2:
            sync_widget_state(f"random_state_{index}", tab_state, "random_state")
            tab_state["random_state"] = st.number_input(
                "Random State",
                min_value=0,
                max_value=1000,
                key=f"random_state_{index}",
                help="Random seed for reproducibility",
            )
    
    elif algorithm == "Hierarchical Clustering":
        col1, col2 = st.columns(2)
        with col1:
            sync_widget_state(f"n_clusters_{index}", tab_state, "n_clusters")
            tab_state["n_clusters"] = st.number_input(
                "Number of Clusters",
                min_value=2,
                max_value=20,
                key=f"n_clusters_{index}",
                help="Number of clusters to form",
            )
        with col2:
            sync_widget_state(f"linkage_method_{index}", tab_state, "linkage_method")
            tab_state["linkage_method"] = st.selectbox(
                "Linkage Method",
                ["ward", "complete", "average", "single"],
                key=f"linkage_method_{index}",
                help="Linkage criterion to use",
            )
    
    elif algorithm == "DBSCAN":
        col1, col2 = st.columns(2)
        with col1:
            sync_widget_state(f"eps_{index}", tab_state, "eps")
            tab_state["eps"] = st.number_input(
                "Epsilon (eps)",
                min_value=0.1,
                max_value=10.0,
                step=0.1,
                key=f"eps_{index}",
                help="Maximum distance between two samples",
            )
        with col2:
            sync_widget_state(f"min_samples_{index}", tab_state, "min_samples")
            tab_state["min_samples"] = st.number_input(
                "Min Samples",
                min_value=1,
                max_value=50,
                key=f"min_samples_{index}",
                help="Minimum number of samples in a neighborhood",
            )
    
    elif algorithm == "Gaussian Mixture":
        col1, col2 = st.columns(2)
        with col1:
            sync_widget_state(f"n_components_{index}", tab_state, "n_components")
            tab_state["n_components"] = st.number_input(
                "Number of Components",
                min_value=2,
                max_value=20,
                key=f"n_components_{index}",
                help="Number of mixture components",
            )
        with col2:
            sync_widget_state(f"covariance_type_{index}", tab_state, "covariance_type")
            tab_state["covariance_type"] = st.selectbox(
                "Covariance Type",
                ["full", "tied", "diag", "spherical"],
                key=f"covariance_type_{index}",
                help="Type of covariance parameters",
            )
    
    elif algorithm == "Naive Bayes":
        st.info("Naive Bayes does not require additional parameters.")
        
    elif algorithm == "Decision Tree":
        st.info("Decision Tree does not require additional parameters.")

    # Collect and return all settings
    return {
        "model_index": index,
        **tab_state,
    }

def cleaning_modeling_debug():
    """
        Shows the value of each session_state variable for debugging purposes.
    """
    st.header("Debugging Cleaning & Modeling Settings")
    for key in st.session_state.keys():
        for i in range(10):
            if key.startswith((f"remove_missing_values_checkbox_{i}", 
                               f"normalize_checkbox_{i}", 
                               f"normalization_selectbox_{i}", 
                               f"modeling_selectbox_{i}")
                ):
                print(f"{key}: {st.session_state[key]}")
                
    print("-------------------------------")
    st.write("End of Debugging Information.")