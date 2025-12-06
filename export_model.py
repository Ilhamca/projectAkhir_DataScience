import pandas as pd
import numpy as np
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Load data
df_Labeled = pd.read_csv("nutrition_labeled.csv")

# Data cleaning
df_Labeled = df_Labeled.dropna()
df_Labeled = df_Labeled.drop_duplicates()

# Remove outliers
def remove_outliers_iqr(df, columns):
    df_clean = df.copy()
    for col in columns:
        Q1 = df_clean[col].quantile(0.25)
        Q3 = df_clean[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        df_clean = df_clean[(df_clean[col] >= lower_bound) & (df_clean[col] <= upper_bound)]
    return df_clean

numeric_cols = ['calories', 'proteins', 'fat', 'carbohydrate']
df_Labeled = remove_outliers_iqr(df_Labeled, numeric_cols)

# Feature engineering
df_Labeled['total_macros'] = df_Labeled['proteins'] + df_Labeled['fat'] + df_Labeled['carbohydrate']
df_Labeled['protein_ratio'] = df_Labeled['proteins'] / (df_Labeled['total_macros'] + 0.001)
df_Labeled['fat_ratio'] = df_Labeled['fat'] / (df_Labeled['total_macros'] + 0.001)
df_Labeled['carb_ratio'] = df_Labeled['carbohydrate'] / (df_Labeled['total_macros'] + 0.001)
df_Labeled['calorie_density'] = df_Labeled['calories'] / (df_Labeled['total_macros'] + 0.001)

# Drop non-numeric columns if they exist
if 'name' in df_Labeled.columns:
    df_Labeled = df_Labeled.drop(columns=['name'])
if 'image' in df_Labeled.columns:
    df_Labeled = df_Labeled.drop(columns=['image'])

# Prepare features
feature_cols = ['calories', 'proteins', 'fat', 'carbohydrate']
X = df_Labeled[feature_cols]
y = df_Labeled['label']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train model
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train_scaled, y_train)

# Save model and scaler
with open('websait/model.pkl', 'wb') as f:
    pickle.dump(rf_model, f)

with open('websait/scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f)

# Export nutrition data with labels
df_Labeled.to_csv('websait/nutrition_data.csv', index=False)

print("Model and data exported successfully!")
print(f"Model accuracy: {rf_model.score(X_test_scaled, y_test):.4f}")
print(f"Feature columns: {feature_cols}")
print(f"Labels: {sorted(y.unique())}")
