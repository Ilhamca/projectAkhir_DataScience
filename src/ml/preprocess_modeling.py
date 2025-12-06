import streamlit as st
import pandas as pd
import numpy as np
from scipy import stats
from sklearn.preprocessing import MinMaxScaler, StandardScaler, RobustScaler

def check_skewness(df):
    """
    Check skewness of numerical columns in the dataset
    Skewness interpretation:
    - Close to 0: Symmetric distribution
    - > 0: Right-skewed (positive skew)
    - < 0: Left-skewed (negative skew)
    - Absolute value > 1: Highly skewed
    """
    st.subheader("Skewness Analysis")
    
    # Select only numerical columns
    numerical_cols = df.select_dtypes(include=[np.number]).columns
    
    if len(numerical_cols) == 0:
        st.warning("No numerical columns found in the dataset.")
        return
    
    # Calculate skewness for each numerical column
    skewness_data = []
    for col in numerical_cols:
        skew_value = df[col].skew()
        
        # Determine skewness type
        if abs(skew_value) < 0.5:
            skew_type = "Symmetric (Not Skewed)"
        elif skew_value > 0:
            if skew_value > 1:
                skew_type = "Highly Right-Skewed"
            else:
                skew_type = "Moderately Right-Skewed"
        else:
            if skew_value < -1:
                skew_type = "Highly Left-Skewed"
            else:
                skew_type = "Moderately Left-Skewed"
        
        skewness_data.append({
            'Column': col,
            'Skewness': round(skew_value, 4),
            'Type': skew_type
        })
    
    # Display results
    skewness_df = pd.DataFrame(skewness_data)
    st.dataframe(skewness_df, width='stretch', hide_index=True)
    
    # Visual representation
    st.write("**Skewness Guidelines:**")
    st.write("- **-0.5 to 0.5**: Symmetric (Not Skewed)")
    st.write("- **0.5 to 1 or -0.5 to -1**: Moderately Skewed")
    st.write("- **> 1 or < -1**: Highly Skewed")
    
    return skewness_df

def normalization(normalizeType):
    """Function to return the appropriate scaler based on normalization type."""
    try:
        if normalizeType == 'MinMax':
            scaler = MinMaxScaler()
        elif normalizeType == 'Standardization':
            scaler = StandardScaler()
        elif normalizeType == 'Robust':
            scaler = RobustScaler()
        return scaler
    except Exception as e:
        st.error(f"Error in normalization function: {e}")
        return None
    