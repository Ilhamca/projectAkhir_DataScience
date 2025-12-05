import streamlit as st
import pandas as pd
import numpy as np
import src.ml.preprocess_modeling as preprocess_modeling


TAB_STATE_DEFAULTS = {
    "remove_missing_values": False,
    "remove_duplicates": False,
    "handle_outliers": False,
    "outlier_method": "IQR Method",
    "normalize": False,
    "normalization_method": "Min-Max Scaling",
    "algorithm": "K-Means (Unsupervised)",
    "split_data": 0.8,
    "n_clusters": 3,
    "random_state": 42,
    "linkage_method": "ward",
    "eps": 0.5,
    "min_samples": 5,
    "n_components": 3,
    "covariance_type": "full",
    "n_estimators": 100,
    "max_depth": 10,
}



def _update_slider_num_models():
    """Update the number of models based on slider value"""
    st.session_state['slider_num_models'] = st.session_state['current_slider_num_models']

def _initialize_tab_settings(index):
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

def _sync_widget_state(widget_key: str, tab_state: dict, field: str):
    """Seed widget session_state with tab defaults when needed"""
    if widget_key not in st.session_state:
        st.session_state[widget_key] = tab_state[field]

def _data_information(data_preview):
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
    """
    st.header("Data Preprocessing & Modeling")
    st.write("Preview dari dataset:")
    data_preview = st.session_state.get('data_preview', None)
    if data_preview is not None:
        st.dataframe(data=data_preview, width='stretch', hide_index=True)
    else:
        st.write("No data preview available.")    

    with st.expander("Informasi Data"):
        _data_information(data_preview)
    
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
            on_change=_update_slider_num_models,
            step=1
        )

        st.write(f"Number of models to compare: {st.session_state['slider_num_models']}")
        
        """
        Sesuai dengan jumlah model yang dipilih, buat st.tab sebanyak itu
        Tabs akan memanggkil cleaning_modeling() untuk tiap tab dan menyimpan pengaturannya secara independen
        """
        # Initialize settings for all tabs that will be shown
        for i in range(st.session_state['slider_num_models']):
            _initialize_tab_settings(i)
            
        tabs = st.tabs([f"Model {i+1}" for i in range(st.session_state['slider_num_models'])])
        tabs_settings = [0] * st.session_state['slider_num_models'] # Stores settings for each tab
        for i in range(st.session_state['slider_num_models']):
            with tabs[i]:
                tabs_settings[i] = _cleaning_modeling(i)
             
        with st.expander("Current Tabs Settings"):        
            st.dataframe(tabs_settings)
        
        st.button("Mulai Proses Komparasi Model", on_click=lambda: st.write("Proses Komparasi Model Dimulai..."), type='primary')
    
    _cleaning_modeling_debug()
    if st.button("Show Tabs Settings in Session State"):
        st.write("tabs_settings:", st.session_state['tabs_settings'])
        
    st.write(tabs_settings[0])
        

def _cleaning_modeling(index):
    tab_state = st.session_state['tabs_settings'][index]
    st.subheader(f"Configuration for Model {index + 1}")
    
    # Data Cleaning Section
    st.markdown("### Data Cleaning")
    
    col1, col2 = st.columns(2)
    
    with col1:
        _sync_widget_state(f"remove_duplicates_checkbox_{index}", tab_state, "remove_duplicates")
        tab_state["remove_duplicates"] = st.checkbox(
            "Remove Duplicates",
            key=f"remove_duplicates_checkbox_{index}",
            value=tab_state["remove_duplicates"],
            help="Remove duplicate rows from the dataset",
        )
        
        _sync_widget_state(f"remove_missing_values_checkbox_{index}", tab_state, "remove_missing_values")
        tab_state["remove_missing_values"] = st.checkbox(
            "Remove Missing Values",
            key=f"remove_missing_values_checkbox_{index}",
            value=tab_state["remove_missing_values"],
            help="Remove rows with missing values from the dataset",
        )

    with col2:
        _sync_widget_state(f"handle_outliers_checkbox_{index}", tab_state, "handle_outliers")
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

        _sync_widget_state(f"outlier_method_selectbox_{index}", tab_state, "outlier_method")
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
    
    _sync_widget_state(f"normalize_checkbox_{index}", tab_state, "normalize")
    tab_state["normalize"] = st.checkbox(
        "Normalize/Standardize Data",
        key=f"normalize_checkbox_{index}",
        value=tab_state["normalize"],
        help="Apply normalization or standardization to numerical features",
    )


    _sync_widget_state(f"normalization_selectbox_{index}", tab_state, "normalization_method")
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
    
    _sync_widget_state(f"modeling_slider_{index}", tab_state, "split_data")
    tab_state["split_data"] = st.slider(
        label="Percentage of data split",
        min_value=0.1,
        max_value=0.9,
        value=st.session_state[f"modeling_slider_{index}"],
        key=f"modeling_slider_{index}",
        step=0.1
    )
    st.write(f"Data split for training: {tab_state['split_data']*100:.0f}%")
    st.write(f"Data split for testing: {(1 - tab_state['split_data'])*100:.0f}%")
    
    
    _sync_widget_state(f"modeling_selectbox_{index}", tab_state, "algorithm")
    tab_state["algorithm"] = st.selectbox(
        "Choose Algorithm",
        ["K-Means (Unsupervised)", "Naive Bayes (Supervised)", "Random Forest (Supervised)",],
        key=f"modeling_selectbox_{index}",
        help="Select the clustering algorithm to use",
    )
    algorithm = tab_state["algorithm"]
    
    
    
    # Algorithm-specific parameters
    if algorithm == "K-Means (Unsupervised)":
        col1, col2 = st.columns(2)
        with col1:
            _sync_widget_state(f"n_clusters_{index}", tab_state, "n_clusters")
            tab_state["n_clusters"] = st.number_input(
                "Number of Clusters (k)",
                min_value=2,
                max_value=20,
                key=f"n_clusters_{index}",
                help="Number of clusters to form",
            )
        with col2:
            _sync_widget_state(f"random_state_{index}", tab_state, "random_state")
            tab_state["random_state"] = st.number_input(
                "Random State",
                min_value=0,
                max_value=1000,
                key=f"random_state_{index}",
                help="Random seed for reproducibility",
            )
    
    elif algorithm == "Hierarchical Clustering (Unsupervised)":
        col1, col2 = st.columns(2)
        with col1:
            _sync_widget_state(f"n_clusters_{index}", tab_state, "n_clusters")
            tab_state["n_clusters"] = st.number_input(
                "Number of Clusters",
                min_value=2,
                max_value=20,
                key=f"n_clusters_{index}",
                help="Number of clusters to form",
            )
        with col2:
            _sync_widget_state(f"linkage_method_{index}", tab_state, "linkage_method")
            tab_state["linkage_method"] = st.selectbox(
                "Linkage Method",
                ["ward", "complete", "average", "single"],
                key=f"linkage_method_{index}",
                help="Linkage criterion to use",
            )
    
    elif algorithm == "Naive Bayes (Supervised)":
        st.info("Naive Bayes does not require additional parameters.")
        
    elif algorithm == "Random Forest (Supervised)":
        col1, col2 = st.columns(2)
        with col1:
            _sync_widget_state(f"n_estimators_{index}", tab_state, "n_estimators")
            tab_state["n_estimators"] = st.number_input(
                "Number of Estimators",
                min_value=10,
                max_value=500,
                step=10,
                key=f"n_estimators_{index}",
                help="Number of trees in the forest",
            )
        with col2:
            _sync_widget_state(f"max_depth_{index}", tab_state, "max_depth")
            tab_state["max_depth"] = st.number_input(
                "Max Depth",
                min_value=1,
                max_value=50,
                key=f"max_depth_{index}",
                help="Maximum depth of the tree",
            )
    
    elif algorithm == "DBSCAN":
        col1, col2 = st.columns(2)
        with col1:
            _sync_widget_state(f"eps_{index}", tab_state, "eps")
            tab_state["eps"] = st.number_input(
                "Epsilon (eps)",
                min_value=0.1,
                max_value=10.0,
                step=0.1,
                key=f"eps_{index}",
                help="Maximum distance between two samples",
            )
        with col2:
            _sync_widget_state(f"min_samples_{index}", tab_state, "min_samples")
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
            _sync_widget_state(f"n_components_{index}", tab_state, "n_components")
            tab_state["n_components"] = st.number_input(
                "Number of Components",
                min_value=2,
                max_value=20,
                key=f"n_components_{index}",
                help="Number of mixture components",
            )
        with col2:
            _sync_widget_state(f"covariance_type_{index}", tab_state, "covariance_type")
            tab_state["covariance_type"] = st.selectbox(
                "Covariance Type",
                ["full", "tied", "diag", "spherical"],
                key=f"covariance_type_{index}",
                help="Type of covariance parameters",
            )

    # Collect and return all settings
    return {
        "remove_missing_values": tab_state["remove_missing_values"],
        "remove_duplicates": tab_state["remove_duplicates"],
        "handle_outliers": tab_state["handle_outliers"],
        "outlier_method": tab_state["outlier_method"],
        "normalize": tab_state["normalize"],
        "normalization_method": tab_state["normalization_method"],
        "algorithm": tab_state["algorithm"],
        "split_data": tab_state["split_data"],
        "n_clusters": tab_state.get("n_clusters", None),
        "random_state": tab_state.get("random_state", None),
        "linkage_method": tab_state.get("linkage_method", None),
        "eps": tab_state.get("eps", None),
        "min_samples": tab_state.get("min_samples", None),
        "n_components": tab_state.get("n_components", None),
        "covariance_type": tab_state.get("covariance_type", None),
        "n_estimators": tab_state.get("n_estimators", None),
        "max_depth": tab_state.get("max_depth", None),
    }
    


def _cleaning_modeling_debug():
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