from sklearn.model_selection import train_test_split
import streamlit as st
import pandas as pd
import numpy as np
from scipy import stats
from sklearn.preprocessing import MinMaxScaler, StandardScaler, RobustScaler
from sklearn.ensemble import IsolationForest
from sklearn.cluster import KMeans
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from typing import Any, Dict, List, Optional, Tuple


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

def outlier_iqr(df):
    """Function to detect and remove outliers using the IQR method."""
    try:
        numerical_df = df.select_dtypes(include=[np.number])
        if numerical_df.empty:
            st.warning("No numerical columns available for IQR outlier detection.")
            return df
        Q1 = numerical_df.quantile(0.25)
        Q3 = numerical_df.quantile(0.75)
        IQR = Q3 - Q1
        mask = ~((numerical_df < (Q1 - 1.5 * IQR)) | (numerical_df > (Q3 + 1.5 * IQR))).any(axis=1)
        return df.loc[mask]
    except Exception as e:
        st.error(f"Error in outlier_iqr function: {e}")
        return df
    
def outlier_zscore(df):
    """Function to detect and remove outliers using the Z-Score method."""
    try:
        numerical_df = df.select_dtypes(include=[np.number])
        if numerical_df.empty:
            st.warning("No numerical columns available for Z-Score outlier detection.")
            return df
        z_scores = np.abs(stats.zscore(numerical_df))
        mask = (z_scores < 3).all(axis=1)
        return df.loc[mask]
    except Exception as e:
        st.error(f"Error in outlier_zscore function: {e}")
        return df
    
def outlier_isolation_forest(df):
    """Function to detect and remove outliers using the Isolation Forest method."""
    try:
        numerical_df = df.select_dtypes(include=[np.number])
        if numerical_df.empty:
            st.warning("No numerical columns available for Isolation Forest.")
            return df
        iso = IsolationForest(contamination=0.1, random_state=42)
        yhat = iso.fit_predict(numerical_df)
        mask = yhat != -1
        filtered_df = df.loc[mask]
        return filtered_df
    except Exception as e:
        st.error(f"Error in outlier_isolation_forest function: {e}")
        return df

def normalization(normalizeType):
    """Function to return the appropriate scaler based on normalization type."""
    try:
        if normalizeType == 'Min-Max Scaling':
            scaler = MinMaxScaler()
        elif normalizeType == 'Z-Score Standardization':
            scaler = StandardScaler()
        elif normalizeType == 'Robust Scaler':
            scaler = RobustScaler()
        return scaler
    except Exception as e:
        st.error(f"Error in normalization function: {e}")
        return None
    
def split_and_test(features_df, labels, train_ratio=0.8):
    if labels is None:
        raise ValueError("Labels are required for supervised algorithms.")
    if not 0 < train_ratio < 1:
        raise ValueError("train_ratio must be between 0 and 1.")
    labels = labels.loc[features_df.index]
    stratify = labels if labels.nunique() > 1 else None
    X_train, X_test, y_train, y_test = train_test_split(
        features_df,
        labels,
        test_size=1-train_ratio,
        random_state=42,
        stratify=stratify,
    )
    return X_train, X_test, y_train, y_test


def _detect_label_column(df: pd.DataFrame) -> Optional[str]:
    label_candidates = [col for col in df.columns if col.lower() == "label"]
    return label_candidates[0] if label_candidates else None


def _run_single_model(df: pd.DataFrame, settings: Dict[str, Any], model_index: int) -> Tuple[Optional[pd.DataFrame], Dict[str, Any]]:
    working_df = df.copy()
    algorithm = settings.get("algorithm", "K-Means (Unsupervised)")
    split_ratio = settings.get("split_data", 0.8) or 0.8
    remove_missing_value = settings.get("remove_missing_values", False)
    remove_duplicates = settings.get("remove_duplicates", False)
    handle_outliers = settings.get("handle_outliers", False)
    outlier_method = settings.get("outlier_method", "IQR Method")
    normalize_flag = settings.get("normalize", False)
    normalization_method = settings.get("normalization_method", "Min-Max Scaling")

    if remove_missing_value:
        working_df = working_df.dropna()
        st.success(f"Model {model_index + 1}: Missing values removed.")

    if remove_duplicates:
        before = len(working_df)
        working_df = working_df.drop_duplicates()
        removed = before - len(working_df)
        st.success(f"Model {model_index + 1}: Removed {removed} duplicate rows.")

    if handle_outliers:
        st.write(f"### Model {model_index + 1} Outlier Handling")
        if outlier_method == "IQR Method":
            working_df = outlier_iqr(working_df)
        elif outlier_method == "Z-Score Method":
            working_df = outlier_zscore(working_df)
        elif outlier_method == "Isolation Forest":
            working_df = outlier_isolation_forest(working_df)

    if normalize_flag:
        scaler = normalization(normalization_method)
        if scaler:
            numeric_cols = working_df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) == 0:
                st.warning(f"Model {model_index + 1}: No numeric columns available for normalization.")
            else:
                working_df[numeric_cols] = scaler.fit_transform(working_df[numeric_cols])
                st.success(f"Model {model_index + 1}: Data normalized using {normalization_method}.")

    label_col = _detect_label_column(working_df)
    labels = working_df[label_col] if label_col else None
    numeric_features = working_df.select_dtypes(include=[np.number]).copy()
    if label_col and label_col in numeric_features.columns:
        numeric_features = numeric_features.drop(columns=[label_col])

    if numeric_features.empty:
        warning_message = f"Model {model_index + 1}: No numeric features available for modeling."
        st.warning(warning_message)
        return working_df, {
            "model_index": model_index,
            "algorithm": algorithm,
            "status": "skipped",
            "message": warning_message,
        }

    result_info: Dict[str, Any] = {
        "model_index": model_index,
        "algorithm": algorithm,
        "status": "success",
        "message": "Model trained successfully.",
    }

    try:
        if algorithm == "K-Means (Unsupervised)":
            n_clusters = settings.get("n_clusters") or 3
            random_state = settings.get("random_state") or 42
            model = KMeans(n_clusters=n_clusters, random_state=random_state)
            model.fit(numeric_features)
            result_info["details"] = {
                "n_clusters": n_clusters,
                "inertia": model.inertia_,
                "iterations": model.n_iter_,
            }
        elif algorithm == "Naive Bayes (Supervised)":
            if labels is None:
                raise ValueError("Label column not found for Naive Bayes model.")
            X_train, X_test, y_train, y_test = split_and_test(numeric_features, labels, train_ratio=split_ratio)
            model = GaussianNB()
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            result_info["details"] = {"accuracy": round(float(accuracy), 4)}
        elif algorithm == "Random Forest (Supervised)":
            if labels is None:
                raise ValueError("Label column not found for Random Forest model.")
            X_train, X_test, y_train, y_test = split_and_test(numeric_features, labels, train_ratio=split_ratio)
            n_estimators = settings.get("n_estimators") or 100
            max_depth = settings.get("max_depth") or None
            random_state = settings.get("random_state") or 42
            model = RandomForestClassifier(
                n_estimators=int(n_estimators),
                max_depth=int(max_depth) if max_depth else None,
                random_state=random_state,
            )
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            result_info["details"] = {
                "accuracy": round(float(accuracy), 4),
                "n_estimators": int(n_estimators),
                "max_depth": int(max_depth) if max_depth else None,
            }
        else:
            raise ValueError(f"Unsupported algorithm selection: {algorithm}")
    except Exception as exc:
        error_message = f"Model {model_index + 1}: {exc}"
        st.error(error_message)
        result_info["status"] = "error"
        result_info["message"] = error_message

    return working_df, result_info


def preprocess_modeling(df: pd.DataFrame, tabs_settings: List[Dict[str, Any]]):
    """Process multiple modeling configurations defined in the UI tabs."""
    if df is None or df.empty:
        st.warning("The dataset is empty. Please upload a valid dataset.")
        return [], []

    if not isinstance(tabs_settings, list) or len(tabs_settings) == 0:
        st.warning("No modeling configurations were provided.")
        return [], []

    processed_outputs: List[Dict[str, Any]] = []
    model_results: List[Dict[str, Any]] = []

    for idx, settings in enumerate(tabs_settings):
        processed_df, result_info = _run_single_model(df, settings or {}, idx)
        if processed_df is not None:
            processed_outputs.append({
                "model_index": idx,
                "algorithm": settings.get("algorithm", "K-Means (Unsupervised)"),
                "data": processed_df,
            })
        if result_info:
            model_results.append(result_info)

    st.write("### Preprocessing and Modeling Completed")
    return processed_outputs, model_results